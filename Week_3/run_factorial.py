import os
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import time

NODE_COUNT = 10


def run(rank, size):
    """Calculate the factorial of 20, divided among nodes."""

    # Generate numbers from 1 to 20
    if rank == 0:
        numbers = torch.tensor([_ + 1 for _ in range(20)], dtype=torch.int64)
        scatter_list = list(torch.chunk(numbers, size))

    # Scatter the numbers to all nodes
    chunk_size = 20 // size
    local_numbers = torch.zeros(chunk_size, dtype=torch.int64)
    if rank == 0:
        dist.scatter(local_numbers, scatter_list, src=0)
    else:
        dist.scatter(local_numbers, src=0)

    # Calculate the local product
    local_product = torch.prod(local_numbers)

    # Use torch to multiply across all nodes
    tensor = local_product.clone().detach()
    dist.all_reduce(tensor, op=dist.ReduceOp.PRODUCT)

    if rank == 0:
        print(f"Factorial from all nodes: {tensor.item()}")


def init_process(rank, size, fn, backend="gloo"):
    """Initialize the distributed environment."""
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "8888"
    dist.init_process_group(backend, rank=rank, world_size=size)
    fn(rank, size)


if __name__ == "__main__":
    processes = []
    mp.set_start_method("spawn")

    start_time = time.time()

    for rank in range(NODE_COUNT):
        p = mp.Process(target=init_process, args=(rank, NODE_COUNT, run))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Number of nodes used: {NODE_COUNT}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
