# --- Sidebar ---
st.sidebar.header("Settings")

api_key = st.sidebar.text_input(
    "🔑 Enter your OpenAI API Key",
    type="password",
    help="Required for AI-powered insights"
)

uploaded_file = st.sidebar.file_uploader(
    "Upload transactions.csv",
    type=["csv"]
)

st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info(
    "**Smart Spending Insights**\n\n"
    "Analyze your transactions, visualize spending, and get AI-powered financial tips.\n\n"
    "Built with Streamlit, OpenAI, and pandas."
)
import streamlit as st
import pandas as pd
import streamlit as st
import pandas as pd
import altair as alt
from openai import OpenAI
from analysis import run_analysis

# ------------------------------

# --- Sidebar ---
st.sidebar.header("Settings")
api_key = st.sidebar.text_input(
    "🔑 Enter your OpenAI API Key",
    type="password",
    help="Required for AI-powered insights"
)
uploaded_file = st.sidebar.file_uploader(
    "Upload transactions.csv",
    type=["csv"]
)
st.sidebar.markdown("---")
st.sidebar.header("About")
st.sidebar.info(
    "**Smart Spending Insights**\n\n"
    "Analyze your transactions, visualize spending, and get AI-powered financial tips.\n\n"
    "Built with Streamlit, OpenAI, and pandas."
)

suggested_budgets = suggest_budgets(monthly)

budgets = {}
for category, suggested in suggested_budgets.items():
        budgets[category] = st.sidebar.number_input(
            label=f"Budget for {category}",
            min_value=0.0,
            value=round(suggested, 2),
            step=10.0,
            format="%.2f",
            key=f"budget_{category}"
        )

budget_vs_actual = pd.DataFrame({
        "Category": list(budgets.keys()),
        "Budget": list(budgets.values()),
        "Actual": [category_totals.get(cat, 0) for cat in budgets.keys()]
    })

budget_vs_actual["Status"] = budget_vs_actual.apply(
        lambda row: "Over Budget" if row["Actual"] > row["Budget"] else "Within Budget",
        axis=1
    )

st.subheader("💸 Budget vs Actual Spend")

chart = alt.Chart(budget_vs_actual.melt(id_vars=["Category", "Status"], value_vars=["Budget", "Actual"])).mark_bar().encode(
        x=alt.X('Category:N', sort='-y'),
        y='value:Q',
    color=alt.Color('variable:N', scale=alt.Scale(range=['#00B4D8', '#FF6F61'])),
        tooltip=['Category', 'variable', 'value', 'Status']
    ).properties(height=400)

st.altair_chart(chart, use_container_width=True)

over_budget = budget_vs_actual[budget_vs_actual["Status"] == "Over Budget"]
if not over_budget.empty:
        st.warning("⚠️ You are over budget in the following categories:")
        for _, row in over_budget.iterrows():
            st.write(f"- **{row['Category']}**: Spent ${row['Actual']:.2f} (Budget ${row['Budget']:.2f})")
else:
        st.success("👍 All categories are within budget!")

    # --- Spending by Category Chart ---
st.subheader("📊 Spending by Category")

chart_data = pd.DataFrame({
        "Category": category_totals.index,
        "Amount": category_totals.values
    })

category_chart = (
        alt.Chart(chart_data)
        .mark_bar(color="#00B4D8")
        .encode(
            x=alt.X("Category", sort="-y"),
            y="Amount"
        )
        .properties(height=350)
    )

st.altair_chart(category_chart, use_container_width=True)

    # --- Monthly Spend Trends ---
st.subheader("📈 Monthly Spend Trends")

monthly_chart = (
        alt.Chart(monthly)
        .mark_line(point=True)
        .encode(
            x="month:T",
            y="amount:Q",
            color="category:N",
        )
        .properties(height=350)
    )

st.altair_chart(monthly_chart, use_container_width=True)

    # --- Raw Data ---
with st.expander("📄 View Raw Transaction Data"):
        st.dataframe(df)


    # --- Dashboard Summary Cards ---
st.markdown("---")
st.subheader("📊 Overview")
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Spend", f"${insights['total_spend']:.2f}")
col2.metric("🏆 Top Category", f"{insights['biggest_category']}", f"${insights['biggest_category_amount']:.2f}")
col3.metric("🚀 Fastest Growing", f"{insights['fastest_growing_category']}")

st.markdown("---")
st.subheader("📈 Charts & Trends")

    # --- AI Insights ---
st.subheader("🤖 AI-Powered Personalized Financial Summary")

if not api_key or api_key.strip() == "":
        st.warning("Please enter your OpenAI API key in the sidebar to generate AI insights.")
else:
        client = OpenAI(api_key=api_key)

        if st.button("Generate AI Spend Insights"):
            with st.spinner("Analyzing your spending with AI..."):

                budget_text_lines = []
                for cat, budget in budgets.items():
                    actual = category_totals.get(cat, 0)
                    diff = actual - budget
                    status = "over budget" if diff > 0 else "within budget"
                    budget_text_lines.append(
                        f"- {cat}: Budgeted ${budget:.2f}, Actual ${actual:.2f} ({status})"
                    )
                budget_text = "\n".join(budget_text_lines)

                prompt = f"""
                You are a friendly financial advisor helping a user understand their spending.

                Here is their spending summary:

                Total Spend: ${insights['total_spend']:.2f}
                Biggest Category: {insights['biggest_category']} (${insights['biggest_category_amount']:.2f})
                Fastest Growing Category: {insights['fastest_growing_category']}

                Spending by Category:
                {insights['categories_ranked']}

                Budgets vs Actual Spend:
                {budget_text}

                Please provide:
                1. A high-level summary of their financial health.
                2. Identify any over-budget categories and explain why it might have happened.
                3. Suggestions for managing or reducing spending to stay within budgets.
                4. A concise 3-point action plan to improve their finances.

                Make it friendly, clear, and actionable.
                """

                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                ai_output = response.choices[0].message.content
                st.success("AI Insights Generated!")
                st.write(ai_output)

                prompt = f"""
                You are a friendly financial advisor helping a user understand their spending.

                Here is their spending summary:

                Total Spend: ${insights['total_spend']:.2f}
                Biggest Category: {insights['biggest_category']} (${insights['biggest_category_amount']:.2f})
                Fastest Growing Category: {insights['fastest_growing_category']}

                Spending by Category:
                {insights['categories_ranked']}

                Budgets vs Actual Spend:
                {budget_text}

                Please provide:
                1. A high-level summary of their financial health.
                2. Identify any over-budget categories and explain why it might have happened.
                3. Suggestions for managing or reducing spending to stay within budgets.
                4. A concise 3-point action plan to improve their finances.

                Make it friendly, clear, and actionable.
                """

                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                )
                ai_output = response.choices[0].message.content
                st.success("AI Insights Generated!")
                st.write(ai_output)
            