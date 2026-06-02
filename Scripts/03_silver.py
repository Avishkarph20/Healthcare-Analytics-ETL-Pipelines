# Databricks notebook source
# DBTITLE 1,Cell 1
# Databricks notebook source
# ============================================
# NOTEBOOK: 03_silver
# PURPOSE: Data cleansing, standardization, joins, and feature engineering
# ============================================

from pyspark import pipelines as dp
from pyspark.sql.functions import (
    col, upper, trim, when, to_date, datediff, 
    round as spark_round, month, year, dayofweek
)
from pyspark.sql.types import IntegerType, DoubleType

# Silver layer: Integrated and enriched healthcare master table

@dp.materialized_view(
    name="main.healthcare_silver.healthcare_master",
    comment="Integrated and enriched healthcare data with analytical features"
)
def healthcare_master():
    # Clean patients data
    patients_clean = (
        spark.read.table("main.healthcare_bronze.patients")
        .drop("_rescued_data")
        .dropDuplicates(["patient_id"])
        .dropna(subset=["patient_id", "name"])
        .withColumn("name", trim(upper(col("name"))))
        .withColumn("gender", upper(trim(col("gender"))))
        .withColumn("blood_type", trim(col("blood_type")))
        .withColumn("medical_condition", trim(upper(col("medical_condition"))))
        .withColumn("age", col("age").cast(IntegerType()))
        .filter((col("age") > 0) & (col("age") < 120))
    )
    
    # Clean admissions data
    admissions_clean = (
        spark.read.table("main.healthcare_bronze.admissions")
        .drop("_rescued_data")
        .dropDuplicates(["admission_id"])
        .dropna(subset=["admission_id", "patient_id"])
        .withColumn("date_of_admission", to_date(col("date_of_admission"), "yyyy-MM-dd"))
        .withColumn("discharge_date", to_date(col("discharge_date"), "yyyy-MM-dd"))
        .withColumn("admission_type", upper(trim(col("admission_type"))))
        .withColumn("room_number", col("room_number").cast(IntegerType()))
        .filter(col("discharge_date") >= col("date_of_admission"))
    )
    
    # Clean billing data
    billing_clean = (
        spark.read.table("main.healthcare_bronze.billing")
        .drop("_rescued_data")
        .dropDuplicates(["bill_id"])
        .dropna(subset=["bill_id", "patient_id", "billing_amount"])
        .withColumn("billing_amount", col("billing_amount").cast(DoubleType()))
        .filter(col("billing_amount") > 0)
        .withColumn("billing_amount", spark_round(col("billing_amount"), 2))
        .withColumn("insurance_provider", upper(trim(col("insurance_provider"))))
    )
    
    # Clean hospital data
    hospital_clean = (
        spark.read.table("main.healthcare_bronze.hospital")
        .drop("_rescued_data")
        .dropDuplicates(["hospital_id"])
        .dropna(subset=["hospital_id", "patient_id"])
        .withColumn("hospital", trim(col("hospital")))
        .withColumn("doctor", trim(upper(col("doctor"))))
        .withColumn("medication", trim(upper(col("medication"))))
        .withColumn("test_results", upper(trim(col("test_results"))))
    )
    
    # Join all datasets
    healthcare_joined = (
        patients_clean
        .join(admissions_clean, on="patient_id", how="inner")
        .join(billing_clean, on="patient_id", how="left")
        .join(hospital_clean, on="patient_id", how="left")
    )
    
    # Add analytical features and return the enriched DataFrame
    return (
        healthcare_joined
        .withColumn("length_of_stay_days", datediff(col("discharge_date"), col("date_of_admission")))
        .withColumn("age_group", 
            when(col("age") < 18, "Child (0-17)")
            .when(col("age") < 35, "Young Adult (18-34)")
            .when(col("age") < 55, "Middle Age (35-54)")
            .when(col("age") < 70, "Senior (55-69)")
            .otherwise("Elderly (70+)")
        )
        .withColumn("billing_category", 
            when(col("billing_amount") < 5000, "Low (<5K)")
            .when(col("billing_amount") < 20000, "Medium (5K-20K)")
            .when(col("billing_amount") < 50000, "High (20K-50K)")
            .otherwise("Very High (50K+)")
        )
        .withColumn("cost_per_day", 
            when(col("length_of_stay_days") > 0, spark_round(col("billing_amount") / col("length_of_stay_days"), 2))
            .otherwise(col("billing_amount"))
        )
        .withColumn("admission_month", month(col("date_of_admission")))
        .withColumn("admission_year", year(col("date_of_admission")))
        .withColumn("day_of_week", dayofweek(col("date_of_admission")))
        .withColumn("admission_timing", when(col("day_of_week").isin([1, 7]), "Weekend").otherwise("Weekday"))
        .withColumn("risk_level", 
            when(col("test_results") == "ABNORMAL", "High Risk")
            .when(col("test_results") == "INCONCLUSIVE", "Medium Risk")
            .otherwise("Low Risk")
        )
    )