Healthcare Analytics ETL Pipeline 
A data engineering ecosystem built on Databricks utilizing a Medallion Architecture to process transactional healthcare records. The pipeline transforms, validates, and reorganizes raw medical, clinical, and financial datasets into an optimized relational Star Schema tailored for executive BI dashboards.

Architecture



Technologies Used
Programming Languages: Python and SQL
Databricks: Unified analytics platform for cluster compute orchestration and pipeline management.
Apache Spark: Distributed engine utilized for parallel data transformations, feature engineering, and aggregations.
Delta Lake: Storage layer providing ACID transactions, schema enforcement, and optimized data compaction.
Unity Catalog: Centralized governance tool for data lineage auditing and secure asset tracking.

Datasets Used
patients.csv: Baseline operational registry tracking demographics, ages, genders, and genetic blood profiles.
hospital.csv: Clinical note logs mapping patient-to-clinician pathways, medications, and test outcomes.
billing.csv: Financial transaction ledger containing claim amounts and insurance network distribution metadata.
admissions.csv: Administrative tracking facility records documenting check-in and check-out boundaries and room configurations.


Complete Tutorial Video


