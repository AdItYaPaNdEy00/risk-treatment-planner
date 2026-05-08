import requests
import time
import statistics

URL = "http://127.0.0.1:5000/categorise"

times = []

payload = {
    "text": "Server crash caused downtime",
    "use_cache": True
}

for i in range(50):

    start = time.time()

    response = requests.post(URL, json=payload)

    end = time.time()

    latency = (end - start) * 1000

    times.append(latency)

    print(f"Request {i+1}: {latency:.2f} ms")

# Percentiles
times.sort()

p50 = times[int(0.50 * len(times))]
p95 = times[int(0.95 * len(times))]
p99 = times[int(0.99 * len(times))]

print("\n===== PERFORMANCE REPORT =====")
print(f"P50 Latency: {p50:.2f} ms")
print(f"P95 Latency: {p95:.2f} ms")
print(f"P99 Latency: {p99:.2f} ms")
print(f"Average: {statistics.mean(times):.2f} ms")