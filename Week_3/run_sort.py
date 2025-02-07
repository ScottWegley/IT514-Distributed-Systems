import os
import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import time

NODE_COUNT = 5
WORDS = [
    "apple",
    "orange",
    "banana",
    "grape",
    "cherry",
    "mango",
    "pear",
    "peach",
    "plum",
    "kiwi",
    "strawberry",
    "blueberry",
    "raspberry",
    "blackberry",
    "pineapple",
    "watermelon",
    "cantaloupe",
    "honeydew",
    "apricot",
    "nectarine",
    "pomegranate",
    "fig",
    "date",
    "persimmon",
    "papaya",
    "guava",
    "lychee",
    "passionfruit",
    "dragonfruit",
    "jackfruit",
    "durian",
    "rambutan",
    "tamarind",
    "coconut",
    "avocado",
    "olive",
    "lemon",
    "lime",
    "grapefruit",
    "tangerine",
    "clementine",
    "mandarin",
    "satsuma",
    "kumquat",
    "pomelo",
    "quince",
    "cranberry",
    "gooseberry",
    "elderberry",
    "mulberry",
    "boysenberry",
    "loganberry",
    "currant",
    "jostaberry",
    "salmonberry",
    "cloudberry",
    "huckleberry",
    "serviceberry",
    "chokeberry",
    "aronia",
    "medlar",
    "loquat",
    "soursop",
    "cherimoya",
    "sapodilla",
    "starfruit",
    "carambola",
    "longan",
    "mangosteen",
    "breadfruit",
    "ackee",
    "bilberry",
    "rowan",
    "sea-buckthorn",
    "miraclefruit",
    "jabuticaba",
    "marionberry",
    "tayberry",
    "olallieberry",
    "buffaloberry",
    "maypop",
    "feijoa",
    "ugli",
    "yuzu",
    "calamondin",
    "bergamot",
    "fingerlime",
    "kaffir",
    "buddha's hand",
    "calamansi",
    "jambul",
    "langsat",
    "pulasan",
    "santol",
    "salak",
    "snakefruit",
    "sweetsop",
    "sugar-apple",
    "custard-apple",
    "atemoya",
]


def run(rank, size, words):
    """Sort a subset of words and return the sorted list."""
    subset_size = len(words) // size
    start_index = rank * subset_size
    end_index = start_index + subset_size if rank != size - 1 else len(words)
    subset = words[start_index:end_index]
    sorted_subset = sorted(subset)
    print(f"Node {rank} sorted subset: {sorted_subset}")

    # Gather sorted subsets from all nodes
    gathered_subsets = [None] * size
    dist.all_gather_object(gathered_subsets, sorted_subset)

    if rank == 0:
        # Merge all sorted subsets
        sorted_words = merge_sorted_lists(gathered_subsets)
        print(f"Sorted words: {sorted_words}")


def merge_sorted_lists(lists):
    """Merge multiple sorted lists into a single sorted list."""
    import heapq

    return list(heapq.merge(*lists))


def init_process(rank, size, fn, words, backend="gloo"):
    """Initialize the distributed environment."""
    os.environ["MASTER_ADDR"] = "localhost"
    os.environ["MASTER_PORT"] = "8888"
    dist.init_process_group(backend, rank=rank, world_size=size)
    fn(rank, size, words)


if __name__ == "__main__":
    processes = []
    mp.set_start_method("spawn")

    start_time = time.time()

    for rank in range(NODE_COUNT):
        p = mp.Process(target=init_process, args=(rank, NODE_COUNT, run, WORDS))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Number of nodes used: {NODE_COUNT}")
    print(f"Time taken: {elapsed_time:.2f} seconds")
