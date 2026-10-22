"""Create a reproducible synthetic dataset for the public dashboard demo."""

from pathlib import Path

import numpy as np
import pandas as pd


RNG = np.random.default_rng(20261023)
OUTPUT = Path(__file__).resolve().parents[1] / "data" / "credit_health_demo.csv"
CUSTOMERS = 1_500
MONTHS = range(1, 9)
SCORE_LABELS = np.array(["Poor", "Standard", "Good"])
OCCUPATIONS = np.array(["Analyst", "Designer", "Engineer", "Manager", "Researcher", "Teacher"])
LOANS = np.array(["Personal Loan", "Auto Loan", "Home Loan", "Education Loan"])
PAYMENT_BEHAVIOURS = np.array(
    [
        "High_spent_Large_value_payments",
        "High_spent_Medium_value_payments",
        "High_spent_Small_value_payments",
        "Low_spent_Large_value_payments",
        "Low_spent_Medium_value_payments",
        "Low_spent_Small_value_payments",
    ]
)


def choose_score(previous):
    """Keep customer journeys stable while allowing synthetic label movement."""
    if RNG.random() >= 0.13:
        return previous
    return int(np.clip(previous + RNG.choice([-1, 1], p=[0.46, 0.54]), 0, 2))


def main():
    rows = []
    customer_states = RNG.choice([0, 1, 2], size=CUSTOMERS, p=[0.29, 0.53, 0.18])
    customer_age = RNG.integers(21, 61, size=CUSTOMERS)
    customer_income = RNG.lognormal(mean=10.65, sigma=0.42, size=CUSTOMERS)

    for customer_id in range(1, CUSTOMERS + 1):
        state = int(customer_states[customer_id - 1])
        age = int(customer_age[customer_id - 1])
        base_income = float(customer_income[customer_id - 1])

        for month in MONTHS:
            if month > 1:
                state = choose_score(state)
            score = SCORE_LABELS[state]
            health = state
            income = max(12_000, base_income * (0.75 + 0.24 * health) * RNG.normal(1, 0.035))
            monthly_income = income / 12
            debt = max(100, (3 - health) * 1_250 + RNG.normal(850, 360))
            delay = max(0, RNG.normal([29, 18, 8][health], 5))
            inquiries = max(0, int(round(RNG.normal([6, 3, 1][health], 1.2))))
            utilization = float(np.clip(RNG.normal([68, 46, 27][health], 10), 3, 98))
            mix = RNG.choice(
                ["Bad", "Standard", "Good"],
                p=[[0.50, 0.45, 0.05], [0.16, 0.62, 0.22], [0.02, 0.17, 0.81]][health],
            )
            minimum_payment = RNG.choice(
                ["Yes", "No", "NM"], p=[[0.64, 0.16, 0.20], [0.40, 0.34, 0.26], [0.15, 0.64, 0.21]][health]
            )
            payment_behaviour = RNG.choice(PAYMENT_BEHAVIOURS)
            emi = max(10, debt * RNG.uniform(0.02, 0.07))
            invested = max(0, monthly_income * RNG.uniform(0.03, 0.20))
            balance = max(0, monthly_income - emi - invested - RNG.uniform(180, 650))
            rows.append(
                {
                    "Customer_ID": customer_id,
                    "Month": month,
                    "Age": age,
                    "Occupation": RNG.choice(OCCUPATIONS),
                    "Annual_Income": round(income, 2),
                    "Monthly_Inhand_Salary": round(monthly_income, 2),
                    "Num_Bank_Accounts": int(np.clip(round(RNG.normal(4, 1.3)), 1, 10)),
                    "Num_Credit_Card": int(np.clip(round(RNG.normal([5, 4, 3][health], 1)), 1, 9)),
                    "Interest_Rate": round(max(1, RNG.normal([17, 11, 6][health], 2)), 1),
                    "Num_of_Loan": int(np.clip(round(RNG.normal([4, 3, 2][health], 1)), 0, 8)),
                    "Type_of_Loan": RNG.choice(LOANS),
                    "Delay_from_due_date": round(delay, 1),
                    "Num_of_Delayed_Payment": int(np.clip(round(delay / 4 + RNG.normal(1, 1)), 0, 20)),
                    "Changed_Credit_Limit": round(RNG.normal(8, 4), 2),
                    "Num_Credit_Inquiries": inquiries,
                    "Credit_Mix": mix,
                    "Outstanding_Debt": round(debt, 2),
                    "Credit_Utilization_Ratio": round(utilization, 2),
                    "Credit_History_Age": int(np.clip((age - 18) * 12 + RNG.normal(0, 16), 12, 480)),
                    "Payment_of_Min_Amount": minimum_payment,
                    "Total_EMI_per_month": round(emi, 2),
                    "Amount_invested_monthly": round(invested, 2),
                    "Payment_Behaviour": payment_behaviour,
                    "Monthly_Balance": round(balance, 2),
                    "Credit_Score": score,
                }
            )

    frame = pd.DataFrame(rows)
    OUTPUT.parent.mkdir(exist_ok=True)
    frame.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(frame):,} synthetic records to {OUTPUT}")


if __name__ == "__main__":
    main()
