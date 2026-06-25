from src.common.db import get_connection


def execute_fred_merge():

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "EXEC staging.usp_merge_fred_data"
        )

        conn.commit()

        print(
            "FRED MERGE completed successfully"
        )

    except Exception as e:

        conn.rollback()

        print(
            f"MERGE failed: {e}"
        )

        raise

    finally:

        conn.close()