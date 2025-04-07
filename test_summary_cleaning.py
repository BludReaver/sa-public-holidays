import re

def clean_event_name(summary):
    return re.sub(r"\s*\([^)]*\)", "", summary).strip()

test_cases = [
    "Adelaide Cup (Regional Holiday)",
    "Easter Saturday (Regional Holiday)",
    "King's Birthday (Regional Holiday)",
    "Mother's Day (Not a Public Holiday)"
]

print("Original vs Cleaned:")
print("-" * 40)
for test in test_cases:
    cleaned = clean_event_name(test)
    print(f"Original: {test}")
    print(f"Cleaned : {cleaned}")
    print("-" * 40) 