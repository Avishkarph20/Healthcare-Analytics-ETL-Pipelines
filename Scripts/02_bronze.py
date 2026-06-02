# Databricks notebook source
# DBTITLE 1,Cell 1
# Databricks notebook source
# ============================================
# NOTEBOOK: 02_bronze
# PURPOSE: Extract raw CSVs and load into Bronze Delta Tables
# ============================================

from pyspark import pipelines as dp

RAW_PATH = "/Volumes/workspace/default/healthcare_etl/"

# Bronze layer: Ingest raw CSV files using Auto Loader
# Each table uses streaming ingestion with schema inference

@dp.table(
    name="main.healthcare_bronze.patients",
    comment="Raw patient data ingested from CSV"
)
def patients():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("pathGlobFilter", "patients.csv")
        .load(RAW_PATH)
    )

@dp.table(
    name="main.healthcare_bronze.admissions",
    comment="Raw admissions data ingested from CSV"
)
def admissions():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("pathGlobFilter", "admissions.csv")
        .load(RAW_PATH)
    )

@dp.table(
    name="main.healthcare_bronze.billing",
    comment="Raw billing data ingested from CSV"
)
def billing():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("pathGlobFilter", "billing.csv")
        .load(RAW_PATH)
    )

@dp.table(
    name="main.healthcare_bronze.hospital",
    comment="Raw hospital data ingested from CSV"
)
def hospital():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("header", "true")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("pathGlobFilter", "hospital.csv")
        .load(RAW_PATH)
    )