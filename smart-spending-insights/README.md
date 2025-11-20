# Smart Spending Insights

Minimal scaffold to analyze transaction CSV data.

Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Files

- `app.py` - CLI entrypoint
- `analysis.py` - small pandas-based summary of `data/transactions.csv`
- `data/transactions.csv` - sample data

