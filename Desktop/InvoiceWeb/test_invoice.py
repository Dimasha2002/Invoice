import json
import urllib.request
import urllib.error

url = "http://localhost:8000/api/invoices"

# Test Case 1: Advance Payment
print("=" * 50)
print("TEST 1: Advance Invoice")
print("=" * 50)
payload_advance = {
    "customer_name": "Ahmed Mohamed",
    "phone": "0768833626",
    "description": "Website Development Project - Phase 1",
    "total_amount": 5000,
    "advance_paid": 2000,
    "payment_type": "advance"
}

try:
    data = json.dumps(payload_advance).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"✓ Success! Invoice ID: {result.get('id')}")
        print(f"  PDF File: invoice_{result.get('id')}.pdf")
        print(f"  Type: {result.get('type')}")
        print(f"  Total: ${result.get('total_amount'):.2f} | Paid: ${result.get('advance_paid'):.2f} | Balance: ${result.get('balance'):.2f}")
except urllib.error.HTTPError as e:
    print(f"✗ HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test Case 2: Rest Payment
print("\n" + "=" * 50)
print("TEST 2: Rest Invoice")
print("=" * 50)
payload_rest = {
    "customer_name": "Fatima Khan",
    "phone": "+94721234567",
    "description": "Software License - Annual Subscription",
    "total_amount": 3000,
    "advance_paid": 3000,
    "payment_type": "rest"
}

try:
    data = json.dumps(payload_rest).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"✓ Success! Invoice ID: {result.get('id')}")
        print(f"  PDF File: invoice_{result.get('id')}.pdf")
        print(f"  Type: {result.get('type')}")
        print(f"  Total: ${result.get('total_amount'):.2f} | Paid: ${result.get('advance_paid'):.2f} | Balance: ${result.get('balance'):.2f}")
except urllib.error.HTTPError as e:
    print(f"✗ HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test Case 3: Full Payment
print("\n" + "=" * 50)
print("TEST 3: Full Invoice")
print("=" * 50)
payload_full = {
    "customer_name": "John Doe",
    "phone": "+94711234567",
    "description": "Consulting Services - Complete Project",
    "total_amount": 4500,
    "advance_paid": 4500,
    "payment_type": "full"
}

try:
    data = json.dumps(payload_full).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(f"✓ Success! Invoice ID: {result.get('id')}")
        print(f"  PDF File: invoice_{result.get('id')}.pdf")
        print(f"  Type: {result.get('type')}")
        print(f"  Total: ${result.get('total_amount'):.2f} | Paid: ${result.get('advance_paid'):.2f} | Balance: ${result.get('balance'):.2f}")
except urllib.error.HTTPError as e:
    print(f"✗ HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 50)
print("All tests completed!")
print("=" * 50)
