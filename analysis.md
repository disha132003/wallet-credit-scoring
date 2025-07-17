# Wallet Score Analysis

After assigning credit scores to all user wallets based on their transaction behaviors, we analyzed their distribution and behavior patterns.

---

## 📈 Credit Score Distribution

The scores were grouped into the following 10 buckets:

- 0–99  
- 100–199  
- 200–299  
- 300–399  
- 400–499  
- 500–599  
- 600–699  
- 700–799  
- 800–899  
- 900–1000

The plot below shows the number of wallets in each score range:

🖼️ **Refer to**: `credit_score_distribution.png`

This graph reveals how most users fall between the **400–800 range**, with only a few in the extreme low (0–199) or high (900–1000) ends.

---

## 🔴 Behavior of Wallets in the Lower Score Range (0–199)

Wallets in this range typically show:

- **High number of borrows**
- **Very low repayment ratios**
- **Frequent liquidations**
- Often have little or no deposits
- Risky patterns indicating potential bad actors or mismanagement

**Example insights:**

| Wallet | # Borrows | Repay Ratio | Liquidated |
|--------|-----------|-------------|------------|
| 0x123  | 12        | 0.3         | Yes        |
| 0x456  | 8         | 0.2         | Yes        |

---

## 🟢 Behavior of Wallets in the Higher Score Range (800–1000)

These high-scoring wallets are responsible and consistent:

- **Frequent deposits**
- **High repayment ratios** (often >0.9)
- **No liquidations**
- **Active usage** with balanced borrow-repay patterns
- Appear to be long-term users or bots with well-managed strategies

**Example insights:**

| Wallet | # Deposits | Repay Ratio | Liquidated |
|--------|------------|-------------|------------|
| 0xABC  | 22         | 1.0         | No         |
| 0xDEF  | 30         | 0.95        | No         |

---

## 📌 Conclusion

The credit scoring method successfully distinguishes risky wallets from healthy ones:

- **Low scores** correlate with borrowing without repaying and liquidations.
- **High scores** correlate with strong financial behavior and long-term activity.

These insights can help DeFi platforms offer custom risk-based interest rates or flag suspicious activity proactively.
