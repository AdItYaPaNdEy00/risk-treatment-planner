import requests

url = "http://127.0.0.1:5000/categorise"

inputs = [
    "Server crash caused downtime",
    "Fraud led to financial loss",
    "Company violated compliance rules",
    "Poor strategy caused market loss",
    "Database outage affected users",
    "Insider trading issue",
    "System latency increased",
    "Legal violation by company",
    "Wrong pricing strategy",
    "Hardware failure in production"
]

for text in inputs:
    response = requests.post(url, json={"text": text})
    print("\nInput:", text)
    print("Output:", response.json())