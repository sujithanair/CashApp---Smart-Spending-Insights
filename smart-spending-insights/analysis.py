import pandas as pd

# ------------------------------
# LOAD + CLEAN DATA
# ------------------------------
def load_data(path="transactions.csv"):
    df = pd.read_csv(path)

    # Normalize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Standard expected columns:
    # date, merchant, amount, category (optional)
    df["date"] = pd.to_datetime(df["date"])
    df["amount"] = df["amount"].astype(float)

    return df


# ------------------------------
# CATEGORY ASSIGNMENT
# ------------------------------
CATEGORY_KEYWORDS = {
    "Groceries": ["grocery", "market", "whole foods", "trader joe", "kroger", "heb"],
    "Dining": ["restaurant", "cafe", "coffee", "grill", "bar", "eatery"],
    "Shopping": ["amazon", "store", "mall", "clothes", "retail"],
    "Transport": ["uber", "lyft", "gas", "shell", "exxon"],
    "Travel": ["airlines", "hotel", "lyft", "uber", "airbnb"],
    "Health": ["pharmacy", "clinic", "hospital", "walgreens", "cvs"],
    "Entertainment": ["movie", "netflix", "disney", "ticket", "theater"],
}

def assign_category(merchant):
    merchant_lower = merchant.lower()
    for cat, keys in CATEGORY_KEYWORDS.items():
        if any(k in merchant_lower for k in keys):
            return cat
    return "Other"


def categorize(df):
    if "category" not in df.columns:
        df["category"] = df["merchant"].apply(assign_category)
    return df


# ------------------------------
# AGGREGATIONS
# ------------------------------
def aggregate_by_category(df):
    return df.groupby("category")["amount"].sum().sort_values(ascending=False)


def aggregate_by_month(df):
    df["month"] = df["date"].dt.to_period("M").astype(str)
    return (
        df.groupby(["month", "category"])["amount"]
        .sum()
        .reset_index()
    )


def aggregate_by_merchant(df):
    return df.groupby("merchant")["amount"].sum().sort_values(ascending=False)


# ------------------------------
# INSIGHTS
# ------------------------------
def extract_insights(df):
    category_totals = aggregate_by_category(df)
    monthly = aggregate_by_month(df)

    biggest_category = category_totals.idxmax()
    biggest_category_amount = category_totals.max()

    # Fastest-growing category
    monthly_pivot = monthly.pivot(index="month", columns="category", values="amount").fillna(0)
    monthly_changes = monthly_pivot.diff().fillna(0).sum().sort_values(ascending=False)
    fastest_growing_category = monthly_changes.idxmax()

    insights = {
        "biggest_category": biggest_category,
        "biggest_category_amount": float(biggest_category_amount),
        "fastest_growing_category": fastest_growing_category,
        "total_spend": float(df["amount"].sum()),
        "categories_ranked": category_totals.to_dict(),
    }

    return insights


# ------------------------------
# MASTER FUNCTION
# ------------------------------
def run_analysis(path="transactions.csv"):
    df = load_data(path)
    df = categorize(df)

    category_totals = aggregate_by_category(df)
    monthly = aggregate_by_month(df)
    merchant_totals = aggregate_by_merchant(df)
    insights = extract_insights(df)

    return {
        "df": df,
        "category_totals": category_totals,
        "monthly": monthly,
        "merchant_totals": merchant_totals,
        "insights": insights,
    }
if __name__ == "__main__":
    result = run_analysis("transactions.csv")
    print("Analysis complete!")
    print(result["insights"])

def suggest_budgets(monthly_df):
    # Calculate average monthly spend per category over available months
    avg_spend = (
        monthly_df.groupby("category")["amount"]
        .mean()
        .sort_values(ascending=False)
        .to_dict()
    )
    return avg_spend
