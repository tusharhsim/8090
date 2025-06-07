import sys


def calculate_reimbursement(days: int, miles: float, receipts: float) -> float:
    """
    Estimate reimbursement for a business trip.

    Parameters
    ----------
    days : int
        Total trip duration in whole days.
    miles : float
        Total ground-travel mileage for the trip.
    receipts : float
        Dollar amount of submitted receipts.

    Returns
    -------
    float
        Predicted refund, rounded to two decimals.
    """

    # ------------------------------------------------------------------
    # 1.  Base daily allowance (per-diem) – simple flat rate
    # ------------------------------------------------------------------
    BASE_PER_DIEM = 100.0           # $/day
    base_per_diem = BASE_PER_DIEM * days

    # ------------------------------------------------------------------
    # 2.  Mileage reimbursement – tiered + cumulative
    # ------------------------------------------------------------------
    mileage_reimb = 0.0
    remaining = miles
    for tier_miles, rate in ((100, 0.58), (400, 0.45), (float("inf"), 0.35)):
        take = min(remaining, tier_miles)
        mileage_reimb += take * rate
        remaining -= take
        if remaining <= 0:
            break

    # ------------------------------------------------------------------
    # 3.  Receipts reimbursement – piece-wise diminishing-returns curve
    # ------------------------------------------------------------------
    def receipt_rate(total: float) -> float:
        if total < 50:       return 0.40
        if total < 300:      return 0.60
        if total < 600:      return 0.75
        if total <= 800:     return 0.85      # sweet spot
        if total <= 1000:    return 0.65
        return 0.55

    receipt_reimb = receipts * receipt_rate(receipts)

    # ------------------------------------------------------------------
    # 4.  Interaction bonuses / penalties
    # ------------------------------------------------------------------
    def duration_adj(d: int) -> float:
        if d == 5:            return 0.15     # +15 %
        if 4 <= d <= 6:       return 0.10     # +10 %
        if d <= 3:            return -0.05    # −5 %
        if d >= 9:            return -0.10    # −10 %
        return 0.0

    def efficiency_adj(eff: float) -> float:
        # eff = miles per day
        if 180 <= eff <= 220:               return 0.10   # +10 %
        if 150 <= eff < 180 or 220 < eff <= 260:  return 0.05   # +5 %
        if 100 <= eff < 150 or 260 < eff <= 300:  return 0.0
        return -0.05                                   # −5 %

    bonus_factor = 1.0 + duration_adj(days) + efficiency_adj(miles / days)

    # Optional light randomization to mimic system noise (±5 %)
    # import random; bonus_factor *= (1 + random.uniform(-0.05, 0.05))

    # ------------------------------------------------------------------
    # 5.  Final predicted refund
    # ------------------------------------------------------------------
    refund = (base_per_diem + mileage_reimb + receipt_reimb) * bonus_factor
    return round(refund, 2)


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

    total = calculate_reimbursement(distance, rate_per_unit, additional_fees)
    print(f"{total:.2f}")


if __name__ == "__main__":
    main()
