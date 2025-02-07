import os
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import time

NODE_COUNT = 5


def run(rank, size):
    """Simple print statement."""
    print(f"Hello from node {rank}")


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
