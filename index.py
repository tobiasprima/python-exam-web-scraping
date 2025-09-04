import csv
from concurrent.futures import ProcessPoolExecutor
from typing import Any
from utils.config import load_config, Config
from worker import run_worker

config: Config = load_config()

def read_csv_rows(csv_path: str, delimiter: str) -> list[dict[str, Any]]:
    with open(csv_path, newline="") as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def chunkify(data: list[Any], num_chunks: int) -> list[list[Any]]:
    if num_chunks <= 1:
        return [data]
    avg = len(data) // num_chunks
    return [data[i*avg:(i+1)*avg] for i in range(num_chunks-1)] + [data[(num_chunks-1)*avg:]]

def main()-> None:
    rows = read_csv_rows(config.csv_path, config.csv_delimiter)
    chunks = chunkify(rows, config.threads)

    with ProcessPoolExecutor(max_workers=config.threads) as executor:
        futures = [
            executor.submit(run_worker, chunk, config)
            for chunk in chunks if chunk
        ]
        for f in futures:
            f.result()

if __name__ == "__main__":
    main()
