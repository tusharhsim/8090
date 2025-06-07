import sys


def calculate_reimbursement(trip_duration_days: int,
                            miles_traveled: float,
                            total_receipts_amount: float) -> float:
    d, m, r = trip_duration_days, miles_traveled, total_receipts_amount

    # 1. Mileage
    mileage = (
            1.05 * min(m, 100) +
            0.75 * max(0, min(m, 1000) - 100) +
            0.25 * max(0, m - 1000)
    )

    # 2. Receipts (diminishing-return ladder)
    receipts = (
            1.00 * min(r, 600) +
            0.45 * max(0, min(r, 1600) - 600) +
            0.10 * max(0, r - 1600)
    )

    # 3. Base per-diem
    per_diem = 30 * d
    if d == 5:
        per_diem *= 1.25
    elif 6 <= d <= 7:
        per_diem *= 1.10
    else:
        per_diem *= 0.85  # short or very long

    # subtotal
    total = mileage + receipts + per_diem

    # 4. Efficiency / vacation tweaks
    pace = m / d  # miles per day
    if 180 <= pace <= 220:  total += 200  # efficiency bonus
    if pace > 400:          total -= 150  # over-drive penalty
    if d >= 8 and r / d > 100:  # vacation
        total *= 0.70

    return round(total, 2)


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py <distance> <rate_per_unit> <additional_fees>")
        sys.exit(1)

    try:
        distance = float(sys.argv[1])
        rate_per_unit = float(sys.argv[2])
        additional_fees = float(sys.argv[3])
    except ValueError:
        print("All arguments must be numeric.")
        sys.exit(1)

    print(calculate_reimbursement(distance, rate_per_unit, additional_fees))


if __name__ == "__main__":
    main()
