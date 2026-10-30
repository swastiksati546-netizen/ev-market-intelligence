"""Generates a SYNTHETIC EV market dataset (for coursework use only).
Values are randomly generated to look plausible; they are NOT real market data.
Run:  python data/generate_dataset.py
"""
import random, csv, os
random.seed(42)

MAKERS = {  # manufacturer: (country, weight)
    "Tesla": ("USA", 10), "BYD": ("China", 12), "Volkswagen": ("Germany", 7),
    "Hyundai": ("South Korea", 6), "Kia": ("South Korea", 5), "BMW": ("Germany", 4),
    "Mercedes-Benz": ("Germany", 4), "Nissan": ("Japan", 4), "Tata Motors": ("India", 5),
    "MG Motor": ("China", 4), "Ford": ("USA", 4), "Rivian": ("USA", 2),
    "NIO": ("China", 3), "Mahindra": ("India", 3), "Ola Electric": ("India", 3),
    "Ather Energy": ("India", 2),
}
CATS = {  # category: (base_sales, price_range, range_km, kWh)
    "Hatchback": (900, (15000, 32000), (200, 420), (30, 60)),
    "Sedan": (1100, (28000, 85000), (350, 650), (50, 100)),
    "SUV": (1600, (30000, 110000), (300, 600), (55, 110)),
    "Bus": (150, (120000, 350000), (180, 350), (200, 400)),
    "Truck": (120, (90000, 250000), (200, 500), (150, 350)),
    "Two-Wheeler": (2500, (1000, 7000), (80, 220), (2, 8)),
}
BATTERIES = ["LFP", "NMC", "NCA", "Sodium-Ion", "Solid-State"]
YEARS = list(range(2019, 2026))
growth = {y: 1 + 0.38 * (y - 2019) for y in YEARS}

names = list(MAKERS)
weights = [MAKERS[m][1] for m in names]
rows = []
for rid in range(1, 2201):
    m = random.choices(names, weights)[0]
    cat = random.choice(list(CATS))
    if cat == "Two-Wheeler" and m not in ("Ola Electric", "Ather Energy", "Tata Motors", "BYD", "NIO", "Mahindra"):
        cat = random.choice(["Hatchback", "Sedan", "SUV"])
    if cat in ("Bus", "Truck") and m not in ("BYD", "Tata Motors", "Mercedes-Benz", "Volkswagen", "Ford", "Mahindra"):
        cat = "SUV"
    base, pr, rg, kw = CATS[cat]
    y = random.choice(YEARS)
    pool = BATTERIES[:3] if y < 2023 else BATTERIES[:4] if y < 2025 else BATTERIES
    bw = [5, 4, 2, 1, 0.3][:len(pool)]
    batt = random.choices(pool, bw)[0]
    cap = round(random.uniform(*kw), 1)
    eff = random.uniform(5.0, 7.5) if cat != "Two-Wheeler" else random.uniform(25, 40)
    rng = int(min(max(cap * eff * random.uniform(0.9, 1.1), rg[0] * 0.8), rg[1] * 1.15))
    sales = int(base * growth[y] * (MAKERS[m][1] / 5) * random.uniform(0.4, 1.6))
    price = round(random.uniform(*pr), 2)
    rating = round(min(5, max(2.5, random.gauss(4.0, 0.45) + (0.15 if batt in ("NMC", "Solid-State") else 0))), 1)
    rows.append([rid, m, f"{m} {cat[:3].upper()}-{random.randint(100, 999)}", cat, y, sales,
                 price, batt, cap, rng, MAKERS[m][0], rating])

out = os.path.join(os.path.dirname(__file__), "ev_market_data.csv")
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "manufacturer", "model", "vehicle_category", "year", "annual_sales", "price",
                "battery_type", "battery_capacity_kwh", "range_km", "manufacturing_country", "customer_rating"])
    w.writerows(rows)
print(f"Wrote {len(rows)} rows -> {out}")
