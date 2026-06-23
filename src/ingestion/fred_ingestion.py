print("SCRIPT IS RUNNING")

import requests
import pandas as pd
import uuid

from datetime import datetime
from src.common.config import FRED_API_KEY
from src.common.db import get_connection

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

SERIES = {
    "FEDFUNDS": "interest_rate",
    "UNRATE": "unemployment_rate",
    "CPIAUCSL": "inflation_index"
}


def get_fred_data():

    pipeline_run_id = str(uuid.uuid4())
    batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    load_timestamp = datetime.now()

    all_data = []

    print(f"Pipeline Run ID: {pipeline_run_id}")
    print(f"Batch ID: {batch_id}")

    for series_id, metric_name in SERIES.items():

        print(f"\nPulling data for: {metric_name}")

        params = {
            "series_id": series_id,
            "api_key": FRED_API_KEY,
            "file_type": "json"
        }

        try:

            response = requests.get(
                BASE_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            if "observations" not in data:
                raise ValueError(f"{metric_name} missing observations")

            df = pd.DataFrame(data["observations"])

            if df.empty:
                raise ValueError(f"{metric_name} returned zero rows")

            df = df[["date", "value"]]

            df.rename(columns={"value": "metric_value"}, inplace=True)

            df["metric_name"] = metric_name
            df["source_system"] = "FRED_API"
            df["batch_id"] = batch_id
            df["pipeline_run_id"] = pipeline_run_id
            df["load_timestamp"] = load_timestamp

            df["metric_value"] = pd.to_numeric(
                df["metric_value"],
                errors="coerce"
            )

            if df["metric_value"].isnull().all():
                raise ValueError(f"{metric_name} all null values")

            print(f"{metric_name}: {len(df)} rows")

            all_data.append(df)

        except Exception as e:
            print(f"ERROR loading {metric_name}: {e}")

    if not all_data:
        raise ValueError("Pipeline failed: no data loaded")

    final_df = pd.concat(all_data, ignore_index=True)

    print("\nPipeline completed")
    print(f"Total rows: {len(final_df)}")

    return final_df


def load_to_sql(df):

    import pandas as pd

    # ------------------------------------------------------------
    # 1. Connect to SQL Server
    # ------------------------------------------------------------
    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------------------------------
    # 2. Loop through each row in the DataFrame
    #    (each row = one observation from FRED)
    # ------------------------------------------------------------
    for _, row in df.iterrows():

        # --------------------------------------------------------
        # 3. SAFE DATA CLEANING (CRITICAL FOR SQL SERVER)
        # --------------------------------------------------------

        # Convert metric_value:
        # - NaN -> None (becomes SQL NULL)
        # - valid numbers -> float
        metric_value = row["metric_value"]
        if pd.isna(metric_value):
            metric_value = None
        else:
            metric_value = float(metric_value)

        # Ensure date is SQL-safe (avoid pandas Timestamp issues)
        date_value = pd.to_datetime(row["date"]).date()

        # Convert timestamps safely
        load_timestamp = row["load_timestamp"]
        if hasattr(load_timestamp, "to_pydatetime"):
            load_timestamp = load_timestamp.to_pydatetime()

        # Force all ID / text fields to strings (prevents type mismatch)
        metric_name = str(row["metric_name"])
        source_system = str(row["source_system"])
        batch_id = str(row["batch_id"])
        pipeline_run_id = str(row["pipeline_run_id"])

        # --------------------------------------------------------
        # 4. DEBUG OPTION (uncomment if you need to troubleshoot)
        # --------------------------------------------------------
        # print({
        #     "date": date_value,
        #     "metric_value": metric_value,
        #     "metric_name": metric_name,
        #     "source_system": source_system,
        #     "batch_id": batch_id,
        #     "pipeline_run_id": pipeline_run_id,
        #     "load_timestamp": load_timestamp
        # })

        # --------------------------------------------------------
        # 5. INSERT INTO SQL
        #    Using parameterized query (prevents SQL injection &
        #    avoids formatting issues)
        # --------------------------------------------------------
        cursor.execute("""
            INSERT INTO raw.raw_fred_data (
                date,
                metric_value,
                metric_name,
                source_system,
                batch_id,
                pipeline_run_id,
                load_timestamp
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            date_value,
            metric_value,
            metric_name,
            source_system,
            batch_id,
            pipeline_run_id,
            load_timestamp
        )

    # ------------------------------------------------------------
    # 6. Commit transaction (saves all inserted rows)
    # ------------------------------------------------------------
    conn.commit()
    conn.close()

if __name__ == "__main__":

    df = get_fred_data()

    print("\nPreview:")
    print(df.head())

    print("\nRow Count:", len(df))

    load_to_sql(df)

    print("Loaded into SQL successfully")