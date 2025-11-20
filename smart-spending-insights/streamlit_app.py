import streamlit as st
import os
from pathlib import Path
import pandas as pd
import altair as alt

# allow importing analysis.py from same folder
from analysis import run_analysis

# locate transactions.csv (repo root)
repo_root = Path(__file__).resolve().parents[1]
transactions_path = repo_root / "transactions.csv"

st.set_page_config(page_title="Smart Spending Insights", layout="wide")



st.sidebar.header("Filters & Data")
st.sidebar.write(f"Using: {transactions_path}")

# About/help section
st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info(
    "**Smart Spending Insights**\n\n"
    "Analyze your transactions, visualize spending, and get AI-powered financial tips.\n\n"
    "Built with Streamlit, OpenAI, and pandas."
)
if not transactions_path.exists():
    st.error(f"transactions.csv not found at {transactions_path}")
else:
    import streamlit as st
    import os
    from pathlib import Path
    import pandas as pd
    import altair as alt

    # allow importing analysis.py from same folder
    from analysis import run_analysis

    # locate transactions.csv (repo root)
    repo_root = Path(__file__).resolve().parents[1]
    transactions_path = repo_root / "transactions.csv"

    st.set_page_config(page_title="Smart Spending Insights", layout="wide")

    from dotenv import load_dotenv
    load_dotenv()

    import streamlit as st
    import os
    from pathlib import Path
    import pandas as pd
    import altair as alt

    # allow importing analysis.py from same folder
    from analysis import run_analysis

    # locate transactions.csv (repo root)
    repo_root = Path(__file__).resolve().parents[1]
    transactions_path = repo_root / "transactions.csv"

    st.set_page_config(page_title="Smart Spending Insights", layout="wide")



    st.sidebar.header("Data & Filters")
    st.sidebar.write(f"Using: {transactions_path}")

    if not transactions_path.exists():
        st.error(f"transactions.csv not found at {transactions_path}")
        st.stop()

    with st.spinner("Running analysis..."):
        results = run_analysis(str(transactions_path))

    insights = results["insights"]
    df = results["df"].copy()

    # --- Filters ---
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    all_categories = sorted(df["category"].unique())
    selected_categories = st.sidebar.multiselect("Categories", options=all_categories, default=all_categories)

    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    else:
        start_date, end_date = pd.to_datetime(min_date), pd.to_datetime(max_date)

    mask = (df["date"] >= start_date) & (df["date"] <= end_date) & (df["category"].isin(selected_categories))
    df_filtered = df.loc[mask].copy()

    if df_filtered.empty:
        st.warning("No transactions match the selected filters.")

    total_spend = df_filtered["amount"].sum()
    category_totals = df_filtered.groupby("category")["amount"].sum().sort_values(ascending=False)

    # --- Dashboard Summary Cards ---
    st.title("💸 Smart Spending Insights Dashboard")
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Spend", f"${total_spend:.2f}")
    col2.metric("🏆 Top Category", category_totals.index[0] if not category_totals.empty else "N/A")
    col3.metric("🧾 Transactions", len(df_filtered))
    st.markdown("---")

    st.header("Spend by category")
    if not category_totals.empty:
        cat_df = category_totals.reset_index().rename(columns={"amount": "total"})
        bar = alt.Chart(cat_df).mark_bar().encode(
            x=alt.X("total:Q", title="Total spend"),
            y=alt.Y("category:N", sort="-x", title="Category"),
            color=alt.Color("category:N", legend=None)
        )
        st.altair_chart(bar, use_container_width=True)
    else:
        st.write("No category data to display.")

    # --- Charts Section ---
    st.subheader("📊 Spend by Category")
    if not df_filtered.empty:
        df_month = df_filtered.copy()
        df_month["month"] = df_month["date"].dt.to_period("M").astype(str)
        monthly = df_month.groupby(["month"]).agg(total_amount=("amount", "sum")).reset_index()
        line = alt.Chart(monthly).mark_line(point=True).encode(
            x=alt.X("month:T", title="Month"),
            y=alt.Y("total_amount:Q", title="Total spend"),
        )
        st.altair_chart(line, use_container_width=True)
    else:
        st.write("No monthly data to show.")

    st.header("Transactions (filtered)")
    st.dataframe(df_filtered.sort_values(by="date", ascending=False).reset_index(drop=True))

    csv = df_filtered.to_csv(index=False)
    st.download_button("Download filtered CSV", data=csv, file_name="transactions_filtered.csv", mime="text/csv")

    st.info("Use the sidebar to adjust the date range and categories. Expand the app to add more charts, breakdowns, and budgets.")

    # ------------------------------
    # Natural-language insights (OpenAI)
    # ------------------------------
    from openai_utils import generate_insights_nl, get_openai_api_key

    st.header("Natural-language insights")
    api_key_present = bool(get_openai_api_key())
    if not api_key_present:
        st.warning("OPENAI_API_KEY is not set. Set the environment variable to enable natural-language insights.")

    with st.expander("Generate human-readable insights from these numbers"):
        col_a, col_b = st.columns([3, 1])
        with col_a:
            prompt_override = st.text_area("Optional: provide a short instruction for the assistant (e.g. tone or focus)", value="")
        with col_b:
            model = st.text_input("Model", value="gpt-3.5-turbo")

        if st.button("Generate insights"):
            if not api_key_present:
                st.error("OPENAI_API_KEY not found in environment. Cannot call OpenAI.")
            else:
                with st.spinner("Generating human-readable insights..."):
                    try:
                        base_insights = insights
                        text = generate_insights_nl(base_insights, model=model)
                        st.subheader("Assistant output")
                        st.write(text)
                    except Exception as e:
                        st.error(f"OpenAI request failed: {e}")
