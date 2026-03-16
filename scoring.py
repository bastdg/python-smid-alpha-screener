def score_pe(pe):
    if pe <= 12:
        return 20
    elif pe <= 18:
        return 10
    elif pe <= 25:
        return 5
    return 0


def score_ev_ebitda(ev):
    if ev <= 8:
        return 20
    elif ev <= 12:
        return 10
    elif ev <= 18:
        return 5
    return 0


def score_roe(roe):
    if roe >= 0.20:
        return 15
    elif roe >= 0.12:
        return 10
    elif roe >= 0.06:
        return 5
    return 0


def score_debt_equity(de):
    if de <= 0.4:
        return 15
    elif de <= 0.8:
        return 10
    elif de <= 1.5:
        return 5
    return 0


def score_revenue_growth(g):
    if g >= 0.12:
        return 15
    elif g >= 0.05:
        return 10
    elif g >= 0:
        return 5
    return 0


def apply_scoring(df):

    df["score_pe"] = df["pe"].apply(score_pe)
    df["score_ev_ebitda"] = df["ev_ebitda"].apply(score_ev_ebitda)
    df["score_roe"] = df["roe"].apply(score_roe)
    df["score_debt_equity"] = df["debt_equity"].apply(score_debt_equity)
    df["score_revenue_growth"] = df["revenue_growth"].apply(score_revenue_growth)

    df["total_score"] = (
        df["score_pe"]
        + df["score_ev_ebitda"]
        + df["score_roe"]
        + df["score_debt_equity"]
        + df["score_revenue_growth"]
    )

    return df