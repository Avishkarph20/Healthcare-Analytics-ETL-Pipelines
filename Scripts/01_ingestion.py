# Databricks notebook source
# Databricks notebook source
# ============================================
# NOTEBOOK: 01_ingestion
# PURPOSE: Configure and verify raw data landing paths
# ============================================

RAW_PATH = "/Volumes/workspace/default/healthcare_etl/"

PATIENTS_CSV   = RAW_PATH + "patients.csv"
ADMISSIONS_CSV = RAW_PATH + "admissions.csv"
BILLING_CSV    = RAW_PATH + "billing.csv"
HOSPITAL_CSV   = RAW_PATH + "hospital.csv"

print("🔍 Inspecting raw landing volume...")
try:
    files = dbutils.fs.ls(RAW_PATH)
    display(files)
    print("✅ Ingestion source paths validated and files are accessible.")
except Exception as e:
    print(f"❌ Error accessing Volume path {RAW_PATH}. Ensure files are uploaded. Error: {e}")