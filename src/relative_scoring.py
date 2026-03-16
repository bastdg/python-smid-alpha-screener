import pandas as pd


def compute_sector_percentiles(df, column, ascending=True):
    """
    Compute percentile ranks within each sector.
    ascending=True means lower values are better (e.g. PE)
    """
    return df.groupby("sector")[column].rank(pct=True, ascending=ascending)


def apply_relative_scoring(df):

    # valuation metrics (lower = better)
    df["pe_percentile"] = compute_sector_percentiles(df, "pe", ascending=False)
    df["ev_ebitda_percentile"] = compute_sector_percentiles(df, "ev_ebitda", ascending=False)

    # quality metrics (higher = better)
    df["roe_percentile"] = compute_sector_percentiles(df, "roe", ascending=True)

    # leverage (lower = better)
    df["de_percentile"] = compute_sector_percentiles(df, "debt_equity", ascending=False)

    # growth (higher = better)
    df["growth_percentile"] = compute_sector_percentiles(df, "revenue_growth", ascending=True)

    # convert percentiles to scores
    df["score_pe_rel"] = df["pe_percentile"] * 20
    df["score_ev_rel"] = df["ev_ebitda_percentile"] * 20
    df["score_roe_rel"] = df["roe_percentile"] * 15
    df["score_de_rel"] = df["de_percentile"] * 15
    df["score_growth_rel"] = df["growth_percentile"] * 15

    return df
