import requests
import threading
import time
import random
import json

URL = "http://localhost:5000/score"
NUM_REQUESTS = 200      # 总请求数
CONCURRENCY = 20        # 并发数

results = []
lock = threading.Lock()

def send_request(idx):
    sample_data = {
        "ip": f"192.168.1.{random.randint(1,255)}",
        "userAgent": random.choice(["curl/7.68.0", "Mozilla/5.0", "python-requests/2.25.1"]),
        "requestCountLastMinute": random.randint(1,30),
        "userId": f"user{random.randint(1,1000)}",
        "productId": random.randint(1000,2000),
        "timestamp": int(time.time()*1000)
    }
    start_time = time.time()
    try:
        resp = requests.post(URL, json=sample_data, timeout=5)
        latency = time.time() - start_time
        status_code = resp.status_code
        decision = resp.json().get("decision")
    except Exception as e:
        latency = None
        status_code = None
        decision = None

    with lock:
        results.append({
            "index": idx,
            "latency": latency,
            "status_code": status_code,
            "decision": decision,
            "input": sample_data
        })

threads = []
start_overall = time.time()
for i in range(NUM_REQUESTS):
    t = threading.Thread(target=send_request, args=(i,))
    threads.append(t)
    t.start()
    # 控制并发数，等待部分线程结束再继续
    if (i+1) % CONCURRENCY == 0:
        for tt in threads:
            tt.join()
        threads = []

# 等待剩余线程结束
for tt in threads:
    tt.join()
total_time = time.time() - start_overall

# 统计结果
success_count = sum(1 for r in results if r["status_code"] == 200)
fail_count = NUM_REQUESTS - success_count
latencies = [r["latency"] for r in results if r["latency"] is not None]

print(f"总请求数: {NUM_REQUESTS}")
print(f"成功请求数: {success_count}")
print(f"失败请求数: {fail_count}")
print(f"平均响应时间: {sum(latencies)/len(latencies):.3f}s")
print(f"最大响应时间: {max(latencies):.3f}s")
print(f"最小响应时间: {min(latencies):.3f}s")
print(f"总耗时: {total_time:.3f}s")
print(f"吞吐量（QPS）: {NUM_REQUESTS/total_time:.2f}")