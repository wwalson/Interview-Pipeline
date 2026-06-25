from src.common.db import get_connection


def load_fred_to_staging():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO staging.stg_fred_data
            (
                raw_fred_id,
                date,
                metric_value,
                metric_name,
                source_system,
                batch_id,
                pipeline_run_id,
                load_timestamp
            )
            SELECT
                raw_fred_id,
                date,
                metric_value,
                metric_name,
                source_system,
                batch_id,
                pipeline_run_id,
                load_timestamp
            FROM raw.raw_fred_data;
        """)

        rows_loaded = cursor.rowcount

        conn.commit()

        print(f"Loaded {rows_loaded} rows into staging")

        return rows_loaded

    except Exception as e:

        conn.rollback()

        print(f"Error loading staging table: {e}")

        raise

    finally:

        conn.close()


if __name__ == "__main__":

    load_fred_to_staging()
