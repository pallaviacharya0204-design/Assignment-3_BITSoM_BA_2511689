# ============================================================
# Part 2 - Restaurant Menu & Order Management System
# ============================================================

import copy  # needed for Task 3 deep copy

# ── Provided Data (do not modify) ────────────────────────────────────────────

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],          "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],              "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],        "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],             "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],           "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],             "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],        "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],           "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],          "total": 270.0},
    ],
}


# ============================================================
# Task 1 - Explore the Menu
# ============================================================

print("============================================================")
print("Task 1 - Explore the Menu")
print("============================================================")

# -- Part 1a: Print menu grouped by category ----------------------------------
# First collect unique categories in display order by looping the menu
categories = []
for item in menu.values():
    if item["category"] not in categories:
        categories.append(item["category"])

for category in categories:
    print(f"\n===== {category} =====")
    for item_name, details in menu.items():
        if details["category"] == category:
            # Show [Available] or [Unavailable] based on the boolean flag
            status = "[Available]" if details["available"] else "[Unavailable]"
            print(f"{item_name:<18} Rs.{details['price']:.2f}   {status}")

# -- Part 1b: Menu statistics using dictionary methods ------------------------
print()

# Total items: .keys() gives all item names, len() counts them
total_items = len(menu.keys())
print(f"Total menu items    : {total_items}")

# Available items: count only those where available is True
available_count = 0
for details in menu.values():
    if details["available"]:
        available_count += 1
print(f"Available items     : {available_count}")

# Most expensive: loop tracking the highest price seen so far
most_expensive_name  = None
most_expensive_price = 0
for item_name, details in menu.items():
    if details["price"] > most_expensive_price:
        most_expensive_price = details["price"]
        most_expensive_name  = item_name
print(f"Most expensive item : {most_expensive_name} (Rs.{most_expensive_price:.2f})")

# Items under Rs.150: loop and collect matching names
print("Items under Rs.150  :")
for item_name, details in menu.items():
    if details["price"] < 150:
        print(f"  {item_name:<18} Rs.{details['price']:.2f}")


# ============================================================
# Task 2 - Cart Operations
# ============================================================

print()
print("============================================================")
print("Task 2 - Cart Operations")
print("============================================================")

cart = []  # starts empty; each entry = {"item": ..., "quantity": ..., "price": ...}


# -- Helper: print current cart state -----------------------------------------
def print_cart(label):
    print(f"\n  Cart after: {label}")
    if not cart:
        print("  (cart is empty)")
    else:
        for entry in cart:
            print(f"    {entry['item']:<18} x{entry['quantity']}  "
                  f"Rs.{entry['price'] * entry['quantity']:.2f}")


# -- Helper: add item to cart -------------------------------------------------
def add_to_cart(item_name, quantity):
    # Check the item exists in the menu
    if item_name not in menu:
        print(f"  [ERROR] '{item_name}' does not exist in the menu.")
        return

    # Check the item is currently available
    if not menu[item_name]["available"]:
        print(f"  [ERROR] '{item_name}' is currently unavailable.")
        return

    # Check if item already in cart — if so, just increase quantity
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] += quantity
            print(f"  [UPDATED] '{item_name}' quantity updated to {entry['quantity']}")
            return

    # Item not already in cart — add a new entry
    cart.append({
        "item":     item_name,
        "quantity": quantity,
        "price":    menu[item_name]["price"],
    })
    print(f"  [ADDED] '{item_name}' x{quantity} added to cart.")


# -- Helper: remove item from cart by name ------------------------------------
def remove_from_cart(item_name):
    for i, entry in enumerate(cart):
        if entry["item"] == item_name:
            cart.pop(i)  # remove the entry at this index
            print(f"  [REMOVED] '{item_name}' removed from cart.")
            return
    # If we reach here, the item wasn't found
    print(f"  [ERROR] '{item_name}' is not in the cart.")


# -- Helper: update quantity of item already in cart --------------------------
def update_quantity(item_name, new_quantity):
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] = new_quantity
            print(f"  [UPDATED] '{item_name}' quantity set to {new_quantity}")
            return
    print(f"  [ERROR] '{item_name}' is not in the cart.")


# -- Simulate the required sequence -------------------------------------------

print("\nSimulating order sequence:")

add_to_cart("Paneer Tikka", 2)
print_cart("Add Paneer Tikka x2")

add_to_cart("Gulab Jamun", 1)
print_cart("Add Gulab Jamun x1")

add_to_cart("Paneer Tikka", 1)        # should update quantity to 3
print_cart("Add Paneer Tikka x1 (update)")

add_to_cart("Mystery Burger", 1)      # does not exist in menu
print_cart("Try Mystery Burger (invalid)")

add_to_cart("Chicken Wings", 1)       # exists but unavailable
print_cart("Try Chicken Wings (unavailable)")

remove_from_cart("Gulab Jamun")
print_cart("Remove Gulab Jamun")

# -- Print final Order Summary ------------------------------------------------
print()
print("========== Order Summary ==========")

subtotal = 0
for entry in cart:
    line_total = entry["price"] * entry["quantity"]
    subtotal  += line_total
    print(f"{entry['item']:<20} x{entry['quantity']}    Rs.{line_total:.2f}")

gst   = round(subtotal * 0.05, 2)   # 5% GST
total = round(subtotal + gst, 2)

print("------------------------------------")
print(f"{'Subtotal:':<28} Rs.{subtotal:.2f}")
print(f"{'GST (5%):':<28} Rs.{gst:.2f}")
print(f"{'Total Payable:':<28} Rs.{total:.2f}")
print("====================================")


# ============================================================
# Task 3 - Inventory Tracker with Deep Copy
# ============================================================

print()
print("============================================================")
print("Task 3 - Inventory Tracker with Deep Copy")
print("============================================================")

# -- Step 1: Deep copy inventory before making any changes --------------------
# copy.deepcopy creates a completely independent copy — changes to inventory
# will NOT affect inventory_backup (unlike a shallow copy or simple assignment)
inventory_backup = copy.deepcopy(inventory)

# Demonstrate that the backup is independent:
print("\nDemonstrating deep copy independence:")
print(f"  inventory['Garlic Naan']['stock'] before change : {inventory['Garlic Naan']['stock']}")
inventory["Garlic Naan"]["stock"] = 999   # temporary change to inventory
print(f"  inventory['Garlic Naan']['stock'] after change  : {inventory['Garlic Naan']['stock']}")
print(f"  inventory_backup['Garlic Naan']['stock']        : {inventory_backup['Garlic Naan']['stock']}")
print("  (backup is unaffected - deep copy works correctly)")

# Restore inventory to original before continuing
inventory["Garlic Naan"]["stock"] = 30
print(f"  inventory['Garlic Naan']['stock'] restored to   : {inventory['Garlic Naan']['stock']}")

# -- Step 2: Deduct cart quantities from inventory ----------------------------
print("\nFulfilling order from cart:")

for entry in cart:
    item_name   = entry["item"]
    qty_ordered = entry["quantity"]
    current_stock = inventory[item_name]["stock"]

    if current_stock >= qty_ordered:
        # Enough stock — deduct normally
        inventory[item_name]["stock"] -= qty_ordered
        print(f"  {item_name:<18} deducted {qty_ordered}, "
              f"stock: {current_stock} -> {inventory[item_name]['stock']}")
    else:
        # Insufficient stock — deduct only what is available (floor at 0)
        print(f"  [WARNING] '{item_name}' — ordered {qty_ordered} but only "
              f"{current_stock} in stock. Deducting {current_stock}.")
        inventory[item_name]["stock"] = 0

# -- Step 3: Print reorder alerts for low-stock items -------------------------
print("\nReorder Alerts:")
alert_found = False
for item_name, details in inventory.items():
    if details["stock"] <= details["reorder_level"]:
        print(f"  [ALERT] Reorder: {item_name} - Only {details['stock']} unit(s) left "
              f"(reorder level: {details['reorder_level']})")
        alert_found = True
if not alert_found:
    print("  No items currently need reordering.")

# -- Step 4: Confirm inventory and backup differ ------------------------------
print("\nInventory vs Backup comparison (items that changed):")
for item_name in inventory:
    live_stock   = inventory[item_name]["stock"]
    backup_stock = inventory_backup[item_name]["stock"]
    if live_stock != backup_stock:
        print(f"  {item_name:<18} live stock: {live_stock}   backup stock: {backup_stock}")


# ============================================================
# Task 4 - Daily Sales Log Analysis
# ============================================================

print()
print("============================================================")
print("Task 4 - Daily Sales Log Analysis")
print("============================================================")

# -- Part 1: Total revenue per day --------------------------------------------
print("\nRevenue per day (original data):")

daily_revenue = {}   # date -> total revenue for that day
for date, orders in sales_log.items():
    day_total = 0
    for order in orders:
        day_total += order["total"]
    daily_revenue[date] = day_total
    print(f"  {date}  Rs.{day_total:.2f}")

# -- Part 2: Best-selling day -------------------------------------------------
best_day     = None
best_revenue = 0
for date, revenue in daily_revenue.items():
    if revenue > best_revenue:
        best_revenue = revenue
        best_day     = date
print(f"\nBest-selling day    : {best_day}  (Rs.{best_revenue:.2f})")

# -- Part 3: Most ordered item ------------------------------------------------
# Count how many individual orders each item appears in
item_order_count = {}   # item_name -> number of orders it appears in

for date, orders in sales_log.items():
    for order in orders:
        for item in order["items"]:
            if item not in item_order_count:
                item_order_count[item] = 0
            item_order_count[item] += 1

# Find the item with the highest count
most_ordered_item  = None
most_ordered_count = 0
for item_name, count in item_order_count.items():
    if count > most_ordered_count:
        most_ordered_count = count
        most_ordered_item  = item_name
print(f"Most ordered item   : {most_ordered_item} (in {most_ordered_count} orders)")

# -- Part 4: Add new day and reprint stats ------------------------------------
print("\nAdding 2025-01-05 to sales log...")

sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"],                     "total": 260.0},
]

# Recompute revenue per day with the new entry included
print("\nRevenue per day (updated):")
daily_revenue = {}
for date, orders in sales_log.items():
    day_total = sum(order["total"] for order in orders)
    daily_revenue[date] = day_total
    print(f"  {date}  Rs.{day_total:.2f}")

# Recompute best-selling day
best_day     = None
best_revenue = 0
for date, revenue in daily_revenue.items():
    if revenue > best_revenue:
        best_revenue = revenue
        best_day     = date
print(f"\nBest-selling day    : {best_day}  (Rs.{best_revenue:.2f})")

# -- Part 5: Numbered list of all orders using enumerate ----------------------
print("\nAll orders (numbered):")

order_number = 1
for date, orders in sales_log.items():
    for order in orders:
        items_str = ", ".join(order["items"])   # join list into readable string
        print(f"{order_number:>2}.  [{date}] Order #{order['order_id']:<3} "
              f"-- Rs.{order['total']:.2f} -- Items: {items_str}")
        order_number += 1
