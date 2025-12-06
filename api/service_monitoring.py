import os
import pandas as pd
import requests
from datetime import datetime

from evidently import Report
from evidently.presets import DataDriftPreset
from evidently.ui.workspace import RemoteWorkspace

# --- Evidently setup ---
EVIDENTLY_URL = "http://evidently:8000"   # Docker service name
PROJECT_ID = "019aeec9-bca8-76bf-8664-db17237a0e87"

# Lazy-loaded globals
_evidently_report = None
_workspace = None
_reference_data = None

prediction_buffer = []
BATCH_SIZE = 1


# -------------------------------
#  SAFE INITIALIZATION FUNCTIONS
# -------------------------------
def get_workspace():
    """
    Initialize RemoteWorkspace only when needed.
    Prevents connection during import (pytest-safe).
    """
    global _workspace

    if _workspace is None:
        try:
            _workspace = RemoteWorkspace(EVIDENTLY_URL)
        except Exception as e:
            print(f"[WARNING] Could not connect to Evidently: {e}")
            _workspace = None  # allow tests to run without failing

    return _workspace


def get_reference_data():
    """
    Lazy-load reference dataset only when needed.
    """
    global _reference_data

    if _reference_data is None:
        _reference_data = pd.read_csv("reference_data/reference_data_appart_lille.csv")

    return _reference_data


def get_report():
    """
    Build the Evidently report only when needed.
    """
    global _evidently_report

    if _evidently_report is None:
        _evidently_report = Report(metrics=[DataDriftPreset()])

    return _evidently_report


# -------------------------------
#  MAIN FUNCTION
# -------------------------------
def log_prediction_for_evidently(house_dict: dict, prediction_value: float):
    """
    Collect predictions, generate drift report and push to Evidently if available.
    """
    entry = {**house_dict, "prix_m2": prediction_value}
    prediction_buffer.append(entry)

    if len(prediction_buffer) < BATCH_SIZE:
        return  # Nothing to do yet

    df = pd.DataFrame(prediction_buffer)

    report = get_report()
    reference_data = get_reference_data()

    run = report.run(df, reference_data)

    # ◼ Save HTML locally
    today = datetime.today().strftime('%B_%Y')
    report_name = f"evidently_reports/evidently_report_{today}.html"
    run.save_html(report_name)
    print(f"Saved HTML → {report_name}")

    # ◼ Try pushing to Evidently server
    workspace = get_workspace()
    if workspace is not None:
        try:
            workspace.add_run(PROJECT_ID, run)
            print("Pushed run to Evidently UI ✓")
        except Exception as e:
            print("Failed pushing to Evidently:", e)

    prediction_buffer.clear()
