import time

import requests

URL = "http://127.0.0.1:8000/health"

def check_health():
    try:
        start = time.perf_counter()
        response = requests.get(URL, timeout=5)
        elapsed = (time.perf_counter() - start)*1000

        print("="*40)
        print("API Health Check")
        print("="*40)
        print(f"Status        : {'Healthy' if response.status_code == 200 else 'Unhealthy'}")
        print(f"Status Code   : {response.status_code}")
        print(f"Response Time : {elapsed:.2f} ms")
    
    except requests.exceptions.RequestException as error:
        print("=" * 40)
        print("API Health Check")
        print("=" * 40)
        print("Status : Unreachable")
        print(f"Error  : {error}")

if __name__ == "__main__":
    check_health()