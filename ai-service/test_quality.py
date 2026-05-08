import requests

url = "http://127.0.0.1:5000/categorise"

test_cases = [
    ("Server crash caused downtime", "Operational Risk"),
    ("Fraud transaction detected", "Financial Risk"),
    ("Legal compliance violation", "Compliance Risk"),
    ("Wrong pricing strategy", "Strategic Risk"),
    ("Database outage affected users", "Operational Risk"),
    ("Money laundering issue", "Compliance Risk"),
    ("Hardware failure in production", "Operational Risk"),
    ("Bad market expansion plan", "Strategic Risk"),
    ("Financial fraud caused loss", "Financial Risk"),
    ("Policy violation by company", "Compliance Risk")
]

correct = 0

for text, expected in test_cases:
    response = requests.post(
        url,
        json={
            "text": text,
            "use_cache": False
        }
    )

    data = response.json()

    predicted = data["category"]

    is_correct = predicted == expected

    if is_correct:
        correct += 1

    print(f"\nInput: {text}")
    print(f"Expected: {expected}")
    print(f"Predicted: {predicted}")
    print(f"Correct: {is_correct}")

accuracy = (correct / len(test_cases)) * 5

print("\n====================")
print(f"Score: {accuracy:.2f}/5")
print("====================")