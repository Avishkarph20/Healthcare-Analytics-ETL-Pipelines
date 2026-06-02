-- ============================================
-- FILE: 04_gold.sql
-- PURPOSE: Compute and materialize all 8 analytical queries for dashboards
-- ============================================

-- ============================================
-- QUERY 1: Patient Demographics Summary Table
-- ============================================
CREATE OR REFRESH MATERIALIZED VIEW main.healthcare_gold.query1_demographics_summary
AS
SELECT gender, age_group, COUNT(*) AS patient_count, ROUND(AVG(age), 1) AS avg_age
FROM main.healthcare_silver.healthcare_master
GROUP BY ALL
ORDER BY gender, age_group;

-- ============================================
-- QUERY 2: Most Common Medical Conditions
-- ============================================
CREATE OR REFRESH MATERIALIZED VIEW main.healthcare_gold.query2_medical_conditions
AS
SELECT medical_condition, COUNT(*) AS total_patients, ROUND(AVG(billing_amount), 2) AS avg_billing, ROUND(AVG(length_of_stay_days), 1) AS avg_stay_days
FROM main.healthcare_silver.healthcare_master
GROUP BY medical_condition
ORDER BY total_patients DESC;

-- ============================================
-- QUERY 3: Revenue by Insurance Provider
-- ============================================
CREATE OR REFRESH MATERIALIZED VIEW main.healthcare_gold.query3_insurance_revenue
AS
SELECT insurance_provider, COUNT(*) AS total_claims, ROUND(SUM(billing_amount), 2) AS total_revenue, ROUND(AVG(billing_amount), 2) AS avg_claim_amount, MAX(billing_amount) AS max_claim
FROM main.healthcare_silver.healthcare_master
GROUP BY insurance_provider
ORDER BY total_revenue DESC;

-- ============================================
-- QUERY 4: Hospital Performance Analysis
-- ============================================
CREATE OR REFRESH MATERIALIZED VIEW main.healthcare_gold.query4_hospital_performance
AS
SELECT hospital, COUNT(*) AS total_patients, ROUND(AVG(length_of_stay_days), 1) AS avg_stay_days, ROUND(AVG(billing_amount), 2) AS avg_billing, ROUND(AVG(CASE WHEN test_results = 'ABNORMAL' THEN 1 ELSE 0 END)*100, 1) AS abnormal_test_pct
FROM main.healthcare_silver.healthcare_master
GROUP BY hospital
ORDER BY total_patients DESC;

-- ============================================
-- QUERY 5: Monthly Admission Trends
-- ============================================
CREATE OR REFRESH MATERIALIZED VIEW main.healthcare_gold.query5_monthly_trends
AS
SELECT admission_year, admission_month, COUNT(*) AS total_admissions, ROUND(SUM(billing_amount), 2) AS monthly_revenue, ROUND(AVG(length_of_stay_days), 1) AS avg_stay
FROM main.healthcare_silver.healthcare_master
GROUP BY ALL
ORDER BY admission_year, admission_month;

-- ============================================
-- QUERY 6: Risk Level Distribution
-- ============================================
CREATE OR REFRESH MATERIALIZED VIEW main.healthcare_gold.query6_risk_distribution
AS
SELECT risk_level, medical_condition, COUNT(*) AS patient_count, ROUND(AVG(billing_amount), 2) AS avg_cost, ROUND(AVG(length_of_stay_days), 1) AS avg_stay
FROM main.healthcare_silver.healthcare_master
GROUP BY ALL
ORDER BY risk_level, patient_count DESC;

-- ============================================
-- QUERY 7: Doctor Performance
-- ============================================
CREATE OR REFRESH MATERIALIZED VIEW main.healthcare_gold.query7_doctor_performance
AS
SELECT doctor, hospital, COUNT(*) AS patients_treated, ROUND(AVG(length_of_stay_days), 1) AS avg_stay_days, COUNT(CASE WHEN test_results = 'NORMAL' THEN 1 END) AS normal_results, COUNT(CASE WHEN test_results = 'ABNORMAL' THEN 1 END) AS abnormal_results
FROM main.healthcare_silver.healthcare_master
GROUP BY ALL
ORDER BY patients_treated DESC;

-- ============================================
-- QUERY 8: Weekend vs Weekday Admissions
-- ============================================
CREATE OR REFRESH MATERIALIZED VIEW main.healthcare_gold.query8_admission_timing
AS
SELECT admission_timing, admission_type, COUNT(*) AS total_admissions, ROUND(AVG(billing_amount), 2) AS avg_billing, ROUND(AVG(length_of_stay_days), 1) AS avg_stay
FROM main.healthcare_silver.healthcare_master
GROUP BY ALL
ORDER BY admission_timing, total_admissions DESC;