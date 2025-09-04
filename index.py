import csv
import asyncio
from concurrent.futures import ProcessPoolExecutor
from utils.config import load_config
from worker import run_worker

config = load_config()

def read_csv_rows(csv_path, delimiter):
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def chunkify(data, num_chunks):
    if num_chunks <= 1:
        return [data]
    avg = len(data) // num_chunks
    return [data[i*avg:(i+1)*avg] for i in range(num_chunks-1)] + [data[(num_chunks-1)*avg:]]

def main():
    rows = read_csv_rows(config.csv_path, config.csv_delimiter)
    chunks = chunkify(rows, config.threads)

    with ProcessPoolExecutor(max_workers=config.threads) as executor:
        futures = [
            executor.submit(asyncio.run, run_worker(chunk, config))
            for chunk in chunks if chunk
        ]
        for f in futures:
            f.result()

if __name__ == "__main__":
    main()
