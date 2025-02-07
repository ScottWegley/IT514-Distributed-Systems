import os
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import time
import random

NODE_COUNT = 5


def run(rank, size):
    """Sum 1000 random numbers between 1 and 100, divided among nodes."""

    # Generate 1000 random numbers between 1 and 100
    if rank == 0:
        numbers = torch.tensor(
            [random.randint(1, 100) for _ in range(1000)], dtype=torch.int
        )
        scatter_list = list(torch.chunk(numbers, size))

    # Scatter the numbers to all nodes
    chunk_size = 1000 // size
    local_numbers = torch.zeros(chunk_size, dtype=torch.int)
    if rank == 0:
        dist.scatter(local_numbers, scatter_list, src=0)
    else:
        dist.scatter(local_numbers, src=0)

    # Calculate the local sum
    local_sum = torch.sum(local_numbers)

    # Use torch to sum across all nodes
    tensor = local_sum.clone().detach().float()
    dist.all_reduce(tensor, op=dist.ReduceOp.SUM)

    if rank == 0:
        print(f"Total sum from all nodes: {tensor.item()}")


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
