# Wallet Credit Scoring

This project assigns a **credit score between 0 and 1000** to each wallet based on its historical transaction behavior using Aave V2 protocol data. The aim is to identify responsible users and flag risky or exploitative behavior.

---

## 🛠️ Method Chosen

We use rule-based feature engineering from user transaction data (`deposit`, `borrow`, `repay`, `redeemUnderlying`, and `liquidationCall`). These features are used to assign a credit score with transparent logic.

---

## 🧱 Architecture & Flow

1. **Extract** data from a zipped JSON file.
2. **Parse** and convert it to a DataFrame.
3. **Engineer features** per wallet:
   - Count of each action
   - Total amounts transacted
   - Liquidation status
4. **Score wallets** based on the rules below.
5. **Save results** to CSV and visualize distribution.

---

## 🧮 Scoring Logic

- **Base score**: 500
- **+2 points** for each deposit (up to 50)
- **+3 points** for each repayment (up to 50)
- **Repayment Ratio** (total repay / borrow amount):
  - < 0.5 → -100 points  
  - 0.5 to 0.8 → -50 points  
  - > 0.8 → +50 points
- **+20 points** if no borrow
- **-200 points** if liquidated, else **+30**
- **+50 bonus** for active wallets (>100 actions)
- **Clipped between 0 and 1000**

---

## 🏁 Output

- `wallet_credit_scores.csv` → Wallet and score
- `credit_score_distribution.png` → Score distribution plot

---

## ▶️ How to Run

```bash
python wallet_credit_score_generator.py
