import requests
from datetime import datetime

# ─────────────────────────────────────────────
# LOGGING HELPER
# ─────────────────────────────────────────────
def log_error(location, error_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ERROR in {location}: {error_type} — {message}\n"
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(entry)


# ─────────────────────────────────────────────
# TASK 1 — FILE READ & WRITE
# ─────────────────────────────────────────────
print("=" * 60)
print("TASK 1 — FILE READ & WRITE")
print("=" * 60)

# Part A — Write
lines = [
    "Topic 1: Variables store data. Python is dynamically typed.",
    "Topic 2: Lists are ordered and mutable.",
    "Topic 3: Dictionaries store key-value pairs.",
    "Topic 4: Loops automate repetitive tasks.",
    "Topic 5: Exception handling prevents crashes.",
]

with open("python_notes.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line + "\n")
print("File written successfully.")

# Append two more lines
extra_lines = [
    "Topic 6: Functions help organise and reuse code.",
    "Topic 7: Modules let you split code across files.",
]
with open("python_notes.txt", "a", encoding="utf-8") as f:
    for line in extra_lines:
        f.write(line + "\n")
print("Lines appended.")

# Part B — Read, number, search
print("\n--- File Contents ---")
with open("python_notes.txt", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

for i, line in enumerate(all_lines, 1):
    print(f"{i}. {line.rstrip()}")

print(f"\nTotal lines: {len(all_lines)}")

keyword = "loops"   # simulated user input for script run
print(f'\nSearching for keyword: "{keyword}"')
matches = [l.rstrip() for l in all_lines if keyword.lower() in l.lower()]
if matches:
    for m in matches:
        print(f"  → {m}")
else:
    print("  No lines matched that keyword.")


# ─────────────────────────────────────────────
# TASK 2 — API INTEGRATION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("TASK 2 — API INTEGRATION")
print("=" * 60)

BASE = "https://dummyjson.com/products"

# Step 1 — Fetch and display 20 products
def fetch_products():
    try:
        resp = requests.get(f"{BASE}?limit=20", timeout=5)
        resp.raise_for_status()
        return resp.json().get("products", [])
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("fetch_products", "ConnectionError", "Failed to connect to dummyjson.com")
        return []
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("fetch_products", "Timeout", "Request to fetch products timed out")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("fetch_products", "Exception", str(e))
        return []

products = fetch_products()

if products:
    print(f"\n{'ID':<4} | {'Title':<30} | {'Category':<15} | {'Price':>8} | {'Rating'}")
    print(f"{'-'*4}-+-{'-'*30}-+-{'-'*15}-+-{'-'*8}-+-{'-'*6}")
    for p in products:
        print(f"{p['id']:<4} | {p['title'][:30]:<30} | {p['category'][:15]:<15} | ${p['price']:>7.2f} | {p['rating']}")

# Step 2 — Filter rating >= 4.5, sort by price descending
    print("\n--- Products with Rating ≥ 4.5 (sorted by price desc) ---")
    filtered = sorted([p for p in products if p["rating"] >= 4.5], key=lambda x: x["price"], reverse=True)
    for p in filtered:
        print(f"  {p['title'][:35]:<35} | ${p['price']:>7.2f} | Rating: {p['rating']}")

# Step 3 — Laptops category
def fetch_laptops():
    try:
        resp = requests.get(f"{BASE}/category/laptops", timeout=5)
        resp.raise_for_status()
        return resp.json().get("products", [])
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("fetch_laptops", "ConnectionError", "Failed to connect")
        return []
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("fetch_laptops", "Timeout", "Laptop category request timed out")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("fetch_laptops", "Exception", str(e))
        return []

print("\n--- Laptops ---")
laptops = fetch_laptops()
for lp in laptops:
    print(f"  {lp['title']:<40} ${lp['price']:.2f}")

# Step 4 — POST simulated product
def add_product():
    payload = {
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API",
    }
    try:
        resp = requests.post(f"{BASE}/add", json=payload, timeout=5)
        resp.raise_for_status()
        print("\n--- POST Response ---")
        print(resp.json())
    except requests.exceptions.ConnectionError:
        print("Connection failed. Please check your internet.")
        log_error("add_product", "ConnectionError", "Failed to POST new product")
    except requests.exceptions.Timeout:
        print("Request timed out. Try again later.")
        log_error("add_product", "Timeout", "POST request timed out")
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("add_product", "Exception", str(e))

add_product()


# ─────────────────────────────────────────────
# TASK 3 — EXCEPTION HANDLING
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("TASK 3 — EXCEPTION HANDLING")
print("=" * 60)

# Part A — Guarded Calculator
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\n--- safe_divide ---")
print(f"  10 / 2  = {safe_divide(10, 2)}")
print(f"  10 / 0  = {safe_divide(10, 0)}")
print(f"  'ten'/2 = {safe_divide('ten', 2)}")

# Part B — Guarded File Reader
def read_file_safe(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    finally:
        print("File operation attempt complete.")

print("\n--- read_file_safe ---")
result = read_file_safe("python_notes.txt")
if result:
    print(f"  Read {len(result)} characters from python_notes.txt")

read_file_safe("ghost_file.txt")

# Part C — already integrated into Task 2 fetch functions above.
print("\n(Part C — robust API calls are integrated into Task 2 functions.)")

# Part D — Input Validation Loop (simulated inputs for script run)
def lookup_product_loop():
    simulated_inputs = ["0", "abc", "5", "999", "quit"]
    print("\n--- Product Lookup Loop (simulated inputs) ---")
    for user_input in simulated_inputs:
        print(f'\n  > Input: "{user_input}"')
        if user_input.lower() == "quit":
            print("  Exiting lookup loop.")
            break
        try:
            pid = int(user_input)
        except ValueError:
            print("  Warning: Please enter a valid integer between 1 and 100.")
            continue
        if not (1 <= pid <= 100):
            print("  Warning: ID must be between 1 and 100.")
            continue
        try:
            resp = requests.get(f"{BASE}/{pid}", timeout=5)
        except requests.exceptions.ConnectionError:
            print("  Connection failed. Please check your internet.")
            log_error("lookup_product", "ConnectionError", f"Failed for product ID {pid}")
            continue
        except requests.exceptions.Timeout:
            print("  Request timed out. Try again later.")
            log_error("lookup_product", "Timeout", f"Timed out for product ID {pid}")
            continue
        except Exception as e:
            print(f"  Unexpected error: {e}")
            log_error("lookup_product", "Exception", str(e))
            continue

        if resp.status_code == 404:
            print(f"  Product not found.")
            log_error("lookup_product", "HTTPError", f"404 Not Found for product ID {pid}")
        elif resp.status_code == 200:
            data = resp.json()
            print(f"  Title: {data['title']}  |  Price: ${data['price']}")
        else:
            print(f"  Unexpected status: {resp.status_code}")

lookup_product_loop()


# ─────────────────────────────────────────────
# TASK 4 — LOGGING (intentional triggers)
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("TASK 4 — LOGGING TO FILE")
print("=" * 60)

# Trigger 1 — ConnectionError via unreachable URL
print("\nTriggering ConnectionError with unreachable URL…")
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError:
    print("  Caught ConnectionError — logged.")
    log_error("fetch_products", "ConnectionError", "No connection could be made to unreachable host")
except requests.exceptions.Timeout:
    print("  Caught Timeout — logged.")
    log_error("fetch_products", "Timeout", "Request to unreachable host timed out")
except Exception as e:
    log_error("fetch_products", "Exception", str(e))

# Trigger 2 — HTTP 404 for nonexistent product ID 999
print("Triggering HTTP 404 for product ID 999…")
try:
    resp = requests.get(f"{BASE}/999", timeout=5)
    if resp.status_code != 200:
        print(f"  Got status {resp.status_code} — logged.")
        log_error("lookup_product", "HTTPError", f"404 Not Found for product ID 999")
    else:
        print("  Unexpectedly got 200.")
except Exception as e:
    log_error("lookup_product", "Exception", str(e))

# Print full error log
print("\n--- error_log.txt ---")
try:
    with open("error_log.txt", "r", encoding="utf-8") as f:
        print(f.read())
except FileNotFoundError:
    print("  No log file found.")
