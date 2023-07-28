from pathlib import Path

import pandas as pd


def load_data(data_file: Path) -> pd.DataFrame:
    return pd.read_csv(data_file)
