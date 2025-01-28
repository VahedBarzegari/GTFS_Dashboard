import pandas as pd

from pathlib import Path

infile = Path(__file__).parent / "Date_Classification.csv"
Date_Classification_df = pd.read_csv(infile)

infile = Path(__file__).parent / "modified_stop_times.csv"
modified_stop_times_df = pd.read_csv(infile)

