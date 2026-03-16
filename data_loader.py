import pandas as pd
import os

def get_us_stock_universe(tickers):

    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "russell2000_demo.csv")

    df = pd.read_csv(file_path)

    # TEMPORAIRE : on ignore la liste complète Russell
    # pour continuer à tester le screener
    return df