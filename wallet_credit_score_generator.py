
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict

import os

# Get the current directory where the script is located
current_dir = os.path.dirname(os.path.abspath(__file__))

# Full path to the JSON file
json_path = os.path.join(current_dir, "wallet_transactions.json")
print("Looking for JSON file at:", json_path)
with open(json_path, "r", encoding="utf-8") as file:
    data = json.load(file)


# Step 3: Convert to DataFrame
df = pd.DataFrame(data)

# Step 4: Extract Features Per Wallet
wallet_features = defaultdict(lambda: {
    'num_deposits': 0,
    'num_borrows': 0,
    'num_repayments': 0,
    'num_withdrawals': 0,
    'num_liquidations': 0,
    'total_deposit_amount': 0,
    'total_borrow_amount': 0,
    'total_repay_amount': 0,
    'total_withdraw_amount': 0,
    'was_liquidated': 0
})

for _, row in df.iterrows():
    wallet = row['userWallet']
    action = row['action'].lower()
    action_data = row.get('actionData', {})
    amount_str = action_data.get('amount', '0')

    try:
        amount = int(amount_str) / 1e18
    except:
        amount = 0

    if action == 'deposit':
        wallet_features[wallet]['num_deposits'] += 1
        wallet_features[wallet]['total_deposit_amount'] += amount
    elif action == 'borrow':
        wallet_features[wallet]['num_borrows'] += 1
        wallet_features[wallet]['total_borrow_amount'] += amount
    elif action == 'repay':
        wallet_features[wallet]['num_repayments'] += 1
        wallet_features[wallet]['total_repay_amount'] += amount
    elif action == 'redeemunderlying':
        wallet_features[wallet]['num_withdrawals'] += 1
        wallet_features[wallet]['total_withdraw_amount'] += amount
    elif action == 'liquidationcall':
        wallet_features[wallet]['num_liquidations'] += 1
        wallet_features[wallet]['was_liquidated'] = 1

features_df = pd.DataFrame.from_dict(wallet_features, orient='index')
features_df.reset_index(inplace=True)
features_df.rename(columns={'index': 'wallet'}, inplace=True)

# Step 5: Score Each Wallet
def compute_credit_score(row):
    score = 500

    score += min(row['num_deposits'], 50) * 2
    score += min(row['num_repayments'], 50) * 3

    if row['total_borrow_amount'] > 0:
        repay_ratio = row['total_repay_amount'] / row['total_borrow_amount']
        if repay_ratio < 0.5:
            score -= 100
        elif repay_ratio < 0.8:
            score -= 50
        else:
            score += 50
    else:
        score += 20

    if row['was_liquidated']:
        score -= 200
    else:
        score += 30

    total_actions = row['num_deposits'] + row['num_borrows'] + row['num_repayments'] + row['num_withdrawals']
    if total_actions > 100:
        score += 50

    return max(0, min(1000, int(score)))

features_df['credit_score'] = features_df.apply(compute_credit_score, axis=1)

# Step 6: Save Credit Scores to CSV
features_df[['wallet', 'credit_score']].to_csv("wallet_credit_scores.csv", index=False)
print("✅ Scores saved to wallet_credit_scores.csv")

# Step 7: Visualize Score Distribution
plt.figure(figsize=(10,6))
sns.histplot(features_df['credit_score'], bins=10, kde=True, color='skyblue', edgecolor='black')
plt.title("Credit Score Distribution of Wallets")
plt.xlabel("Credit Score")
plt.ylabel("Number of Wallets")
plt.grid(True)
plt.savefig("credit_score_distribution.png")
plt.show()

# Step 8: Group by Score Bands
def score_band(score):
    return f"{(score//100)*100}-{(score//100)*100+99}"

features_df['score_band'] = features_df['credit_score'].apply(score_band)
band_counts = features_df['score_band'].value_counts().sort_index()
print(band_counts)

# Step 9: Analyze High vs Low Score Wallets
low_score_wallets = features_df[features_df['credit_score'] < 200]
high_score_wallets = features_df[features_df['credit_score'] > 800]

print("\n🔴 Low Score Wallet Sample:")
print(low_score_wallets[['wallet', 'num_borrows', 'total_borrow_amount', 'num_liquidations']].head())

print("\n🟢 High Score Wallet Sample:")
print(high_score_wallets[['wallet', 'num_deposits', 'total_repay_amount', 'was_liquidated']].head())
