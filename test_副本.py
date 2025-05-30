import sqlite3

PAGE_SIZE = 50
conn = sqlite3.connect('Ice cream combo_副本.db')
cur = conn.cursor()

cur.execute("SELECT * FROM combo LIMIT 1")
cols = [desc[0] for desc in cur.description]
search_field = "combo_name"

flavors = [
    "matcha", "espresso", "mint", "strawberry", "salt", "pistachio",
    "chocolate", "caramel", "blueberry", "milk", "mango", "chestnut",
    "pineapple", "raspberries", "dragon fruit", "almonds", "hazelnut",
    "marshmallow", "peanut butter", "oreo crumbs", "lime", "black sesame",
    "ferrero rocher", "pop rocks", "grapefruit", "sakura", "whiskey",
    "rum", "soaked raisins", "brandy", "vodka", "baileys", "mojito"
]

print("\nAvailable flavors:")
for i, f in enumerate(flavors, 1):
    print(f"{i:2}. {f}")

print("\nSearch combos by flavors in combo_name.")
print("Leave input blank to skip. Use space to enter multiple keywords.")

include = input("Include (optional): ").lower().strip().split()
exclude = input("Exclude (optional): ").lower().strip().split()

# Build query
sql = f"SELECT * FROM combo WHERE 1=1"
params = []

for kw in include:
    sql += f" AND {search_field} LIKE ?"
    params.append(f"%{kw}%")

for kw in exclude:
    sql += f" AND {search_field} NOT LIKE ?"
    params.append(f"%{kw}%")

cur.execute(sql, params)
results = cur.fetchall()

# column widths
col_widths = [len(c) for c in cols]
for row in results:
    for i, val in enumerate(row):
        col_widths[i] = max(col_widths[i], len(str(val)))

def show_page(rows, start, end):
    header = "No.  | " + " | ".join(c.ljust(col_widths[i]) for i, c in enumerate(cols))
    print(header)
    print("-" * len(header))
    for idx, row in enumerate(rows[start:end], start=start + 1):
        line = f"{str(idx).rjust(4)} | " + " | ".join(str(val).ljust(col_widths[i]) for i, val in enumerate(row))
        print(line)

total = len(results)
pos = 0

if total == 0:
    print("\nNo matches found.")
else:
    while pos < total:
        end = min(pos + PAGE_SIZE, total)
        show_page(results, pos, end)
        pos = end
        if pos < total:
            input(f"\n-- Press Enter to continue ({pos}/{total}) --\n")

conn.close()