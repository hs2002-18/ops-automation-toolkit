import argparse
import concurrent.futures
import time

import requests


def send_request(url):
    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=5)
        elapsed = (time.perf_counter() - start) * 1000
        return response.status_code, elapsed
    except requests.exceptions.RequestException:
        elapsed = (time.perf_counter() - start) * 1000
        return None, elapsed


def main():
    parser = argparse.ArgumentParser(description="Simple API Load Tester")
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000/users",
        help="API endpoint",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=100,
        help="Number of requests",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=10,
        help="Concurrent workers",
    )

    args = parser.parse_args()

    success = 0
    failed = 0
    response_times = []

    start = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = [
            executor.submit(send_request, args.url)
            for _ in range(args.requests)
        ]

        for future in concurrent.futures.as_completed(futures):
            status, elapsed = future.result()
            response_times.append(elapsed)

            if status == 200:
                success += 1
            else:
                failed += 1

    total_time = time.perf_counter() - start

    print("=" * 45)
    print("API Load Test Report")
    print("=" * 45)
    print(f"URL               : {args.url}")
    print(f"Total Requests    : {args.requests}")
    print(f"Successful        : {success}")
    print(f"Failed            : {failed}")
    print(f"Average Response  : {sum(response_times)/len(response_times):.2f} ms")
    print(f"Total Time        : {total_time:.2f} sec")
    print(f"Requests/Second   : {args.requests/total_time:.2f}")


if __name__ == "__main__":
    main()