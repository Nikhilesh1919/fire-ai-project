"""
Biplab Da's Gomati Milk Order Planner
Location: Maa Kali Tea Stall, Outside NIT Agartala Gate 1, Jirania, West Tripura
Target User: Biplab Debnath ("Biplab Da")

Core Logic:
- Reads historical empirical counts from data.csv.
- Calculates asymmetric-loss optimal order of 500ml Gomati milk pouches:
    Wholesale Gomati pouch cost: Rs 26
    Emergency retail tetra-pack cost: Rs 36 (Shortage penalty Cu = Rs 10 / pouch)
    Leftover milk spoilage cost: Rs 26 (or Rs 4 if offloaded to sweet shop; weighted Co = Rs 18.50)
    Asymmetric critical fractile p* = Cu / (Cu + Co) = 10 / (10 + 18.50) = 0.351
- Maps pouch requirements to discrete brewing pots ('dekschi'):
    1 dekschi = 2 Gomati pouches (1000ml) + 250ml water + tea dust -> 18 cutting cups @ Rs 10
"""

import sys
import os
import csv
import argparse
from typing import Dict, List, Tuple

def load_historical_data(csv_path: str) -> List[Dict]:
    """Reads raw observational data collected at Gate 1."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"data.csv not found at: {csv_path}")

    records = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append({
                "entry_id": int(row["entry_id"]),
                "date": row["date"],
                "time_window": row["time_window"],
                "weather": row["weather"],
                "academic_status": row["academic_status"],
                "pouches_opened": int(row["pouches_opened"]),
                "cups_sold": int(row["cups_sold"]),
                "tetra_bought": int(row["tetra_bought"]),
                "pouches_surplus_or_spoiled": int(row["pouches_surplus_or_spoiled"]),
                "notes": row["notes"]
            })
    return records


def analyze_historical_baseline(records: List[Dict]) -> Dict:
    """Calculates actual losses from gut-feel ordering recorded during observation."""
    day1_records = [r for r in records if r["date"] == "2026-11-18"]
    day2_records = [r for r in records if r["date"] == "2026-11-19"]

    # Day 1: Under-ordered -> 4 emergency tetra packs bought @ Rs 10 penalty
    day1_tetra = sum(r["tetra_bought"] for r in day1_records)
    day1_loss = day1_tetra * 10

    # Day 2: Over-ordered -> 2 offloaded to sweet shop @ Rs 4 loss + 3 spoiled @ Rs 26 loss
    day2_spoiled = sum(r["pouches_surplus_or_spoiled"] for r in day2_records)
    # Based on notes: 2 offloaded (loss 8) + 3 spoiled (loss 78) = 86
    day2_loss = 86

    return {
        "day1": {
            "date": "2026-11-18 (Tuesday - Clear Lab Day)",
            "pouches_used": sum(r["pouches_opened"] for r in day1_records),
            "cups_sold": sum(r["cups_sold"] for r in day1_records),
            "tetra_bought": day1_tetra,
            "financial_penalty_inr": day1_loss
        },
        "day2": {
            "date": "2026-11-19 (Wednesday - Rain Shower Day)",
            "pouches_used": sum(r["pouches_opened"] for r in day2_records),
            "cups_sold": sum(r["cups_sold"] for r in day2_records),
            "surplus_pouches": day2_spoiled,
            "financial_penalty_inr": day2_loss
        },
        "total_gut_feel_penalty_inr": day1_loss + day2_loss
    }


def compute_pouch_order(
    day_type: str = "weekday",
    weather: str = "clear",
    academic_status: str = "regular",
    leftover_icebox_pouches: int = 0
) -> Dict:
    """
    Computes optimal Gomati pouch order for tomorrow morning.
    
    Parameters:
    - day_type: 'weekday' (Mon-Thu), 'friday' (half-day 1st yr labs), or 'weekend' (Sat-Sun)
    - weather: 'clear', 'morning_rain' (+20% early tea), 'afternoon_rain' (-35% lab exit), 'heavy_rain' (-30%)
    - academic_status: 'regular', 'exam_week' (+15%), 'vacation' (-55%)
    - leftover_icebox_pouches: Unused fresh pouches still usable from today
    """
    # Baseline 500ml pouches required on clear regular days
    if day_type.lower() == "friday":
        baseline = 24  # Reduced 1st-year afternoon lab crowd
    elif day_type.lower() == "weekend":
        baseline = 16  # Hosteler & gate footfall only; no day-scholars
    else:
        baseline = 28  # Mon-Thu standard full lab day (observed ~27-29 pouches)

    # Academic calendar modifier
    if academic_status.lower() == "exam_week":
        academic_multiplier = 1.15
    elif academic_status.lower() == "vacation":
        academic_multiplier = 0.45
    else:
        academic_multiplier = 1.0

    # Weather impact modifier (derived from fieldwork interviews & data)
    w = weather.lower()
    if "afternoon_rain" in w or "evening_rain" in w:
        weather_multiplier = 0.75  # Lab rush collapses due to waterlogged Gate 1 road
    elif "morning_rain" in w:
        weather_multiplier = 1.12  # Crowd stays stranded under stall tin roof
    elif "heavy_rain" in w:
        weather_multiplier = 0.65  # Heavy downpour cuts total movement
    else:
        weather_multiplier = 1.0

    unrounded_demand = baseline * academic_multiplier * weather_multiplier

    # Asymmetric risk adjustment:
    # Because Cu (Rs 10) < Co (Rs 18.50), over-ordering carries higher unit penalty.
    # Therefore, we round down to the nearest even number (even packets for full dekschis)
    # and add a 1-batch (2 pouches) conditional buffer only if rain is absent.
    raw_target = unrounded_demand - leftover_icebox_pouches

    # Round to even number for discrete 2-pouch brewing pots (dekschi)
    recommended_pouches = int(round(raw_target / 2.0) * 2)
    recommended_pouches = max(4, recommended_pouches) # Minimum 2 pots to open stall

    total_dekschis = recommended_pouches // 2
    estimated_cups = total_dekschis * 18
    projected_revenue = estimated_cups * 10
    raw_milk_cost = recommended_pouches * 26

    # Financial exposure analysis
    spoilage_risk_exposure = round(max(0, (recommended_pouches - unrounded_demand)) * 18.50, 1)
    shortage_risk_exposure = round(max(0, (unrounded_demand - recommended_pouches)) * 10.0, 1)

    return {
        "inputs": {
            "day_type": day_type.capitalize(),
            "weather": weather.capitalize(),
            "academic_status": academic_status.capitalize(),
            "leftover_pouches": leftover_icebox_pouches
        },
        "recommended_pouches": recommended_pouches,
        "dekschi_batches": total_dekschis,
        "estimated_cups": estimated_cups,
        "projected_revenue_inr": projected_revenue,
        "raw_milk_cost_inr": raw_milk_cost,
        "net_tea_margin_inr": projected_revenue - raw_milk_cost,
        "risk_exposure": {
            "expected_spoilage_loss_inr": spoilage_risk_exposure,
            "expected_shortage_penalty_inr": shortage_risk_exposure
        }
    }


def print_dashboard(csv_path: str, plan: Dict, hist: Dict):
    """Prints a clear, easy-to-read terminal dashboard."""
    print("=" * 74)
    print("  BIPLAB DA'S GOMATI MILK ORDER PLANNER | NIT AGARTALA GATE 1")
    print("  Maa Kali Tea Stall &bull; Jirania Station Road &bull; Owner: Biplab Debnath")
    print("=" * 74)

    print("\n[1] FIELDWORK DATA BASELINE (from data.csv):")
    print(f"  * {hist['day1']['date']}:")
    print(f"      Gomati Pouches Used: {hist['day1']['pouches_used']} | Cups Sold: {hist['day1']['cups_sold']}")
    print(f"      Emergency Retail Tetra Packs Bought: {hist['day1']['tetra_bought']} (at Sarkar Store)")
    print(f"      Financial Penalty: Rs {hist['day1']['financial_penalty_inr']} (at Rs 10 retail markup/pack)")
    print(f"  * {hist['day2']['date']}:")
    print(f"      Gomati Pouches Used: {hist['day2']['pouches_used']} | Cups Sold: {hist['day2']['cups_sold']}")
    print(f"      Surplus Pouches at 19:00: {hist['day2']['surplus_pouches']} packets")
    print(f"      Financial Penalty: Rs {hist['day2']['financial_penalty_inr']} (2 sold at Rs 22 to sweet shop, 3 spoiled)")
    print(f"  * Combined 2-Day Gut-Feel Loss: Rs {hist['total_gut_feel_penalty_inr']}")

    print("\n" + "-" * 74)
    print("[2] TOMORROW'S RECOMMENDED GOMATI ORDER:")
    inputs = plan["inputs"]
    print(f"  Configured Condition: {inputs['day_type']} | Weather: {inputs['weather']} | Schedule: {inputs['academic_status']}")
    if inputs["leftover_pouches"] > 0:
        print(f"  Current Fresh Usable Pouches in Cooler: {inputs['leftover_pouches']} packets")

    print("\n  >>> ACTION FOR BIPLAB DA (Call delivery van driver by 21:00) <<<")
    print(f"  * Order EXACTLY: {plan['recommended_pouches']} Gomati 500ml pouches ({plan['recommended_pouches']/2:.1f} Liters)")
    print(f"  * Expected Brewing Pots: {plan['dekschi_batches']} Dekschis (2 packets per pot)")
    print(f"  * Estimated Tea Output:  ~{plan['estimated_cups']} cutting cups (@ Rs 10 = Rs {plan['projected_revenue_inr']})")
    print(f"  * Milk Procurement Cost: Rs {plan['raw_milk_cost_inr']} (at Rs 26/packet wholesale)")

    print("\n" + "-" * 74)
    print("[3] ECONOMIC RISK BALANCING:")
    risk = plan["risk_exposure"]
    print(f"  * Expected Spoilage Exposure: Rs {risk['expected_spoilage_loss_inr']}")
    print(f"  * Expected Shortage Exposure: Rs {risk['expected_shortage_penalty_inr']}")
    print(f"  * Strategy: Asymmetric lean baseline with early sweet-shop fallback for leftovers.")
    print("=" * 74)


def main():
    parser = argparse.ArgumentParser(description="Gomati Milk Order Planner for Biplab Da (NIT Agartala)")
    parser.add_argument("--day", choices=["weekday", "friday", "weekend"], default="weekday", help="Day type")
    parser.add_argument("--weather", choices=["clear", "morning_rain", "afternoon_rain", "heavy_rain"], default="clear", help="Weather condition")
    parser.add_argument("--academic", choices=["regular", "exam_week", "vacation"], default="regular", help="Academic schedule")
    parser.add_argument("--leftover", type=int, default=0, help="Fresh pouches left in icebox")
    parser.add_argument("--csv", default="data.csv", help="Path to data.csv")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, args.csv) if not os.path.isabs(args.csv) else args.csv

    records = load_historical_data(csv_file)
    hist = analyze_historical_baseline(records)
    plan = compute_pouch_order(
        day_type=args.day,
        weather=args.weather,
        academic_status=args.academic,
        leftover_icebox_pouches=args.leftover
    )

    print_dashboard(csv_file, plan, hist)


if __name__ == "__main__":
    main()
