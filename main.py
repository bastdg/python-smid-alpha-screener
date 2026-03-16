import os
import pandas as pd

from data_loader import get_us_stock_universe
from scoring import apply_scoring
from excel_formatter import format_excel
from russell2000_tickers import RUSSELL_2000_TICKERS


def main():

    print("🚀 Starting Python SMID Alpha Screener...")

    # --------------------------
    # Load universe
    # --------------------------

    df = get_us_stock_universe(RUSSELL_2000_TICKERS)

    if df.empty:
        print("⚠️ No data retrieved. Exiting.")
        return

    print(f"📊 {len(df)} stocks loaded")

    # --------------------------
    # Filter Small & Mid Caps
    # --------------------------

    df = df[(df["marketCap"] >= 300) & (df["marketCap"] <= 10000)]

    print(f"📉 {len(df)} stocks after SMID filter")

    # --------------------------
    # Apply scoring model
    # --------------------------

    scored_df = apply_scoring(df)

    # Format market cap
    scored_df["marketCap"] = scored_df["marketCap"].round(0).astype(int)

    # --------------------------
    # Investment pillars
    # --------------------------

    scored_df["quality_score"] = (
        scored_df["score_roe"] +
        scored_df["score_debt_equity"]
    )

    scored_df["valuation_score"] = (
        scored_df["score_pe"] +
        scored_df["score_ev_ebitda"]
    )

    scored_df["growth_score"] = (
        scored_df["score_revenue_growth"]
    )

    # --------------------------
    # Total score
    # --------------------------

    scored_df["total_score"] = (
        scored_df["quality_score"] +
        scored_df["valuation_score"] +
        scored_df["growth_score"]
    )

    # --------------------------
    # Ranking
    # --------------------------

    scored_df = scored_df.sort_values("total_score", ascending=False)

    scored_df["score_rank"] = range(1, len(scored_df) + 1)

    # --------------------------
    # Size bucket
    # --------------------------

    scored_df["size_bucket"] = scored_df["marketCap"].apply(
        lambda x: "Small Cap" if x < 2000 else "Mid Cap"
    )

    # --------------------------
    # Columns for Excel
    # --------------------------

    display_columns = [
        "symbol",
        "sector",
        "size_bucket",
        "marketCap",
        "pe",
        "ev_ebitda",
        "roe",
        "debt_equity",
        "revenue_growth",
        "quality_score",
        "valuation_score",
        "growth_score",
        "total_score",
        "score_rank"
    ]

    scored_df_display = scored_df[display_columns]

    scored_df_display = scored_df_display.rename(
        columns={"marketCap": "Market Cap (M$)"}
    )

    # --------------------------
    # Watchlist
    # --------------------------

    watchlist = scored_df_display.head(10)

    print(f"⭐ {len(watchlist)} stocks selected for watchlist")

    # --------------------------
    # Export Excel
    # --------------------------

    os.makedirs("output", exist_ok=True)

    output_path = "output/python_smid_alpha_screener.xlsx"

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        watchlist.to_excel(
            writer,
            sheet_name="Watchlist",
            index=False
        )

        scored_df_display.to_excel(
            writer,
            sheet_name="Full Scoring",
            index=False
        )

        # --------------------------
        # Methodology sheet
        # --------------------------

        methodology_rows = [

            ["PYTHON SMID ALPHA SCREENER"],
            [""],

            ["Author"],
            ["Bastien Degeest"],
            ["LinkedIn: https://www.linkedin.com/in/bastiendegeest/"],

            [""],
            ["Overview"],

            ["The Python SMID Alpha Screener is a rule-based fundamental model designed to identify potentially undervalued small and mid-cap companies within the U.S. equity market."],

            ["The objective is to systematically reduce a large universe of companies into a shortlist of potential investment ideas that may deserve deeper fundamental analysis."],

            [""],
            ["Investment Framework"],

            ["The model evaluates companies across three core pillars:"],

            ["Valuation – how attractively a company is priced relative to its fundamentals."],
            ["Quality – the financial strength and profitability of the company."],
            ["Growth – the company's ability to expand revenues over time."],

            [""],
            ["Metrics Used"],

            ["Valuation"],
            ["• Price-to-Earnings (P/E)"],
            ["• EV / EBITDA"],

            [""],
            ["Quality"],
            ["• Return on Equity (ROE)"],
            ["• Debt-to-Equity"],

            [""],
            ["Growth"],
            ["• Revenue Growth"],

            [""],
            ["Scoring Model"],

            ["Each metric receives a score based on predefined thresholds."],

            ["The final score combines:"],
            ["• Valuation Score"],
            ["• Quality Score"],
            ["• Growth Score"],

            ["Companies are then ranked based on their total score."],

            [""],
            ["Universe"],

            ["The screener focuses on companies with market capitalizations between approximately $300M and $10B, inspired by the Russell 2000 universe."],

            [""],
            ["Disclaimer"],

            ["This screener is provided for educational purposes only."],

            ["It does not constitute financial or investment advice."],

            ["All investment decisions should be based on independent financial analysis."]
        ]

        methodology_df = pd.DataFrame(methodology_rows, columns=["Methodology"])

        methodology_df.to_excel(
            writer,
            sheet_name="Methodology",
            index=False
        )

    # --------------------------
    # Format Excel
    # --------------------------

    format_excel(output_path)

    print("✅ Excel generated successfully")


if __name__ == "__main__":
    main()