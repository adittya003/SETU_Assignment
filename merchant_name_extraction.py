import json

INPUT_FILE = "sample_events.json"
OUTPUT_FILE = "seed/merchants.json"

# Read the payload
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    events = json.load(f)

# Extract unique merchants
merchants = {}

for event in events:
    merchant_id = event.get("merchant_id")
    merchant_name = event.get("merchant_name")

    if merchant_id and merchant_name:
        merchants[merchant_id] = {
            "merchant_id": merchant_id,
            "merchant_name": merchant_name
        }

# Sort by merchant_id (optional)
merchant_list = sorted(merchants.values(), key=lambda x: x["merchant_id"])

# Save to merchants.json
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(merchant_list, f, indent=4)

print(f"Found {len(merchant_list)} unique merchants.")
print(f"Saved to '{OUTPUT_FILE}'.")