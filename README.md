Healthcare Analytics ETL Pipeline 
A data engineering ecosystem built on Databricks utilizing a Medallion Architecture to process transactional healthcare records. The pipeline transforms, validates, and reorganizes raw medical, clinical, and financial datasets into an optimized relational Star Schema tailored for executive BI dashboards.

Architecture
![This is Overall Architeture](https://github.com/Avishkarph20/Healthcare-Analytics-ETL-Pipelines/blob/main/Architecture.png)


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


Complete Walkthrough Video:-
(https://youtu.be/cWQ79-oX5f0)


## 🚀 Databricks Setup & Run Instructions

This pipeline processes healthcare data through a Medallion Architecture (Bronze -> Silver -> Gold) using Auto Loader and Delta Live Tables (DLT).

### 📋 Prerequisites
* Active Databricks Workspace with DLT and Cluster compute access.
* Raw data files uploaded to a DBFS path or Unity Catalog Volume.
* Power BI Desktop for consuming the final analytical views.

---

### 📂 Step 1: Stage Raw Data
Upload the following CSV source files to your Databricks landing directory or Volume path:
* `patients.csv`
* `admissions.csv`
* `billing.csv`
* `hospital.csv`

### 📂 Step 2: Import Project Scripts
1. Navigate to your Databricks Workspace.
2. Go to **Repos** -> **Add Repo**.
3. Paste this repository URL to sync the workspace notebooks.

### ⚙️ Step 3: Configure and Run the DLT Pipeline
1. Navigate to **Delta Live Tables** in Databricks and click **Create Pipeline**.
2. Apply the following pipeline settings:
   * **Pipeline Name:** `Healthcare-Analytics-ETL`
   * **Source Code:** Select the workspace paths for the `01_ingestion`, `02_bronze`, and `03_silver` notebooks.
   * **Target Schema:** Specify your destination database schema (e.g., `main.healthcare`).
3. Click **Save** and then click **Start** to run the pipeline.
*(This triggers Auto Loader to stream raw logs into the Bronze layer, executes cleaning and feature engineering, and materializes the combined Silver master table).*

### 📊 Step 4: Execute Gold Analytical Layer
1. Open a Databricks SQL Warehouse or a fresh SQL notebook.
2. Execute the queries inside the `Gold.sql` script.
*(This creates the aggregated, business-level materialized views optimized for analytical reporting).*

### 🔌 Step 5: Connect and Refresh Power BI
1. Go to your Databricks SQL Warehouse connection details and copy the **Server Hostname** and **HTTP Path**.
2. Open **Power BI Desktop** -> **Get Data** -> **Azure Databricks**.
3. Paste your connection details, authenticate with your access token, and load the Gold materialized views to update your dashboard layout.
