from pathlib import Path
import pandas as pd

def fact_sale_quantity():
    root_dir = Path(__file__).parent.parent.parent
    csv_path = root_dir / 'data' / 'sale.csv'

    df = pd.read_csv(csv_path)

    time_diff = df.groupby(['member_id','product_id'])['timestamp_utc'].diff()

    # vi kan ændre dette hvis vi gerne vil have en mindre eller større thresshold.
    thresshold = pd.Timedelta(seconds=10)
    

    print(df)
    return df



if __name__ == "__main__":
    fact_sale_quantity()

    