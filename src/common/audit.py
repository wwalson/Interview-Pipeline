from datetime import datetime

from src.common.db import get_connection


def start_pipeline_run(
    pipeline_run_id,
    pipeline_name,
    source_name,
    target_table
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit.ETL_Load_History
        (
            PipelineRunID,
            PipelineName,
            SourceName,
            TargetTable,
            StartTime,
            Status
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        pipeline_run_id,
        pipeline_name,
        source_name,
        target_table,
        datetime.now(),
        "RUNNING"
    )

    conn.commit()
    conn.close()

def complete_pipeline_run(
    pipeline_run_id,
    rows_received,
    rows_loaded,
    rows_rejected
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE audit.ETL_Load_History
        SET
            EndTime = ?,
            Status = ?,
            RowsReceived = ?,
            RowsLoaded = ?,
            RowsRejected = ?
        WHERE PipelineRunID = ?
    """,
        datetime.now(),
        "SUCCESS",
        rows_received,
        rows_loaded,
        rows_rejected,
        pipeline_run_id
    )

    conn.commit()
    conn.close()

def fail_pipeline_run(
    pipeline_run_id,
    error_message
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE audit.ETL_Load_History
        SET
            EndTime = ?,
            Status = ?,
            ErrorMessage = ?
        WHERE PipelineRunID = ?
    """,
        datetime.now(),
        "FAILED",
        str(error_message),
        pipeline_run_id
    )

    conn.commit()
    conn.close()