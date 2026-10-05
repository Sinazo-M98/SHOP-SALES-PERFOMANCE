# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# DBTITLE 1,Import Libraries
import pandas as pd
import numpy as np

# COMMAND ----------

# DBTITLE 1,Ingesting Table-Orders
orders=spark.table("shop.perfomance.orders")
orders=orders.toPandas()
display(orders)

# COMMAND ----------

# DBTITLE 1,Describing statistical summary of  my data
orders.describe()

# COMMAND ----------

# DBTITLE 1,Checking the size of my data
orders.shape

# COMMAND ----------

# DBTITLE 1,Checking for null values
orders.isnull().sum()

# COMMAND ----------

# MAGIC %md
# MAGIC ###OBSERVATIONS:
# MAGIC - OrderDate has null values-35 NaN
# MAGIC - Quantity has null values- 80 NaN
# MAGIC - Discount has null values- 221 NaN
# MAGIC - Payment Method- 452 NaN
# MAGIC So before cleaning and replacing i must fisrt inspect each column to see data type and consider what am i replacing with

# COMMAND ----------

# DBTITLE 1,CHECKING FOR DUPLICATES
orders.duplicated().sum()

# COMMAND ----------

# DBTITLE 1,INSPECTING THE ORDER DATE
orders[orders["OrderDate"].isnull()]

# COMMAND ----------

orders[orders["OrderDate"].isnull()].head()

# COMMAND ----------

orders[orders["OrderDate"].isnull()]["Status"].value_counts(dropna=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ###OBSERVATIONS-OrderDate
# MAGIC Order Date: 35 missing values. No alternative date field available for recovery. Records retained; missing dates will be excluded only from date-dependent analysis

# COMMAND ----------

# DBTITLE 1,INSPECTING QUANTITY
orders[orders["Quantity"].isnull()]["Status"].value_counts(dropna=False)

# COMMAND ----------

# DBTITLE 1,INSPECTING QUANTITY COLUMN
orders["Quantity"].value_counts(dropna=False)

# COMMAND ----------

# DBTITLE 1,CHECKING NEGATIVE VALUES ON QTY
orders[orders["Quantity"] < 0]["Status"].value_counts(dropna=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ###Cleaning Log for Quantity Column
# MAGIC - Data-quality issues: 80 missing values, 19 negative values, and 6 zero values were identified.
# MAGIC
# MAGIC - Action taken: No values were modified or deleted at this stage. Missing quantities were retained as missing, while negative and zero quantities were flagged for further investigation.
# MAGIC
# MAGIC - Reason: The available evidence is insufficient to determine the correct quantities or confirm that the negative and zero values are invalid. Modifying these values without supporting evidence could distort the dataset.
# MAGIC
# MAGIC - Status: Pending further investigation and validation against the dataset's business rules

# COMMAND ----------

# MAGIC %md
# MAGIC ###Checking data on the rows where quantity = zero or less than 0
# MAGIC -This is to help identify any patterns to understand if these entries are valid or data entry problems

# COMMAND ----------

# DBTITLE 1,22: CHECKING ZERO VALUE QTY CHECKING ZERO VALUE QTY
orders[orders["Quantity"] == 0]["Status"].value_counts(dropna=False)


# COMMAND ----------

# DBTITLE 1,INSPECTING THE 25 RECORDS LESS THAN OR EQUAL TO 0
orders[orders["Quantity"] <= 0]

# COMMAND ----------

# MAGIC %md
# MAGIC ####FINAL DECISION ON QUANTITY COLUMN CLEANING
# MAGIC
# MAGIC Quantity – Cleaning Decision
# MAGIC
# MAGIC The Quantity column contains 80 missing values, 19 negative values, and 6 zero values.
# MAGIC
# MAGIC The 25 records with zero or negative quantities were investigated using the Order Status field. Of these, 24 records were marked as Completed and 1 was marked as Cancelled. None were marked as Returned.
# MAGIC
# MAGIC Because there is insufficient information to determine whether the negative and zero quantities represent valid business adjustments or data-entry errors, these values were not modified or deleted. The 80 missing values were also retained because their correct values cannot be determined from the available data.
# MAGIC
# MAGIC These records should be flagged for further business validation and excluded from quantity-based analysis where appropriate.

# COMMAND ----------

# DBTITLE 1,INSPECTING DISOUNT COLUMN
####checking data type and unique counts
orders["Discount"].value_counts(dropna=False)


# COMMAND ----------

orders[orders["Discount"].isnull()]["Status"].value_counts(dropna=False)

# COMMAND ----------

# DBTITLE 1,Inspecting where discount is ZERO
orders[orders["Discount"]==0].head()

# COMMAND ----------

# DBTITLE 1,Checking for Null Values
orders[orders["Discount"].isnull()].head()

# COMMAND ----------

# MAGIC %md
# MAGIC ###Discount=Zero vs Discount is null or missing (NaN)
# MAGIC Comparing the status distribution for all records with Discount = 0 versus the status distribution for all missing discounts.

# COMMAND ----------

###Checking where discount=0, status and counting values 
orders[orders["Discount"] == 0]["Status"].value_counts(dropna=False)

# COMMAND ----------

###Checking where Discount is null and counting values
orders[orders["Discount"].isnull()]["Status"].value_counts(dropna=False)

# COMMAND ----------

# DBTITLE 1,REPLACING MISSING DISCOUNT WITH ZERO
orders["Discount"]= orders["Discount"].fillna(0)

# COMMAND ----------

# DBTITLE 1,Checking null values on DISCOUNT
orders["Discount"].isnull().sum()

# COMMAND ----------

# MAGIC %md
# MAGIC ###Discount Column Cleaning Decision
# MAGIC Column: Discount
# MAGIC
# MAGIC Data-quality issue: 221 missing Discount values were identified.
# MAGIC
# MAGIC Investigation: The 221 missing Discount records consisted of 207 Completed, 11 Cancelled, and 3 Returned orders. Records with an explicitly recorded Discount of 0 also occur across Completed, Cancelled, and Returned statuses.
# MAGIC
# MAGIC Cleaning decision: Missing Discount values will be replaced with 0, assuming that a missing discount represents no discount applied.
# MAGIC
# MAGIC Reason: The dataset contains 0 as a valid discount value, and the status distribution does not indicate that missing discounts represent a specific transaction status. Treating missing discounts as 0 allows the field to be used consistently in discount and revenue analysis.
# MAGIC
# MAGIC Assumption: This treatment assumes that blank Discount values mean no discount. The assumption should be stated in the project documentation and validated against the business definition if available.

# COMMAND ----------

# MAGIC %md
# MAGIC ###PAYMENT METHOD CLEANING

# COMMAND ----------

# DBTITLE 1,INSPECTING PAYMENT METHOD
orders["PaymentMethod"].value_counts(dropna=False)

# COMMAND ----------

# DBTITLE 1,FIND THE STATUS OF THE 452 MISSING PAYMENTS
orders[orders["PaymentMethod"].isnull()]["Status"].value_counts(dropna=False)

# COMMAND ----------

# DBTITLE 1,REPLACING THE MISSING METHOD WITH UNKNOWN
orders["PaymentMethod"]=orders["PaymentMethod"].fillna("Unknown")

# COMMAND ----------

# DBTITLE 1,Verifying null Payment Methods
orders["PaymentMethod"].isnull().sum()

# COMMAND ----------

# DBTITLE 1,Verifying Payment Methods and Value Counts
orders["PaymentMethod"].value_counts(dropna=False)

# COMMAND ----------

# MAGIC %md
# MAGIC ###Payment Method Column Cleaning
# MAGIC Column: Payment Method
# MAGIC
# MAGIC Data-quality issue: 452 missing values were identified.
# MAGIC
# MAGIC Investigation: The 452 records with missing Payment Method consisted of 426 Completed, 14 Cancelled, and 12 Returned orders. Therefore, the missing values could not be attributed to a particular order status or payment outcome.
# MAGIC
# MAGIC Cleaning decision: The 452 missing values were replaced with "Unknown".
# MAGIC
# MAGIC Reason: The actual payment method cannot be determined from the available data. Using "Unknown" preserves the records while clearly distinguishing missing information from known payment methods such as cash, wallet, gateway, and cardtocard.
# MAGIC
# MAGIC Verification: Missing Payment Method values were checked after cleaning and the null count was reduced to 0.

# COMMAND ----------

orders.info()

# COMMAND ----------

orders.isnull().sum()

# COMMAND ----------

# DBTITLE 1,CHECKING FOR DUPLICATES
orders.duplicated().sum()

# COMMAND ----------

orders[orders.duplicated()]

# COMMAND ----------

orders[orders.duplicated()][["OrderID", "CustomerID"]].head(50)

# COMMAND ----------

orders.duplicated(subset=["OrderID", "CustomerID"]).sum()

# COMMAND ----------

orders[orders["OrderID"].duplicated(keep=False)].sort_values("OrderID")

# COMMAND ----------

# DBTITLE 1,DROPPING DUPLICATES
orders=orders.drop_duplicates()

# COMMAND ----------

orders.duplicated().sum()

# COMMAND ----------

orders.info()

# COMMAND ----------

# DBTITLE 1,CREATING/SAVING THE PROCESSED TABLE
####Convert the pandas DataFrame back to a spark DataFrame
spark_orders=spark.createDataFrame(orders)

spark_orders.write \
    .mode("overwrite") \
    .format("delta") \
    .option("overwriteSchema","true") \
    .saveAsTable("workspace.default.orders_processed")

print("Table 'workspace.default.orders_processed' saved successfully.")

print(f"Successfully created table: {'workspace.default.orders_processed'}")

# COMMAND ----------

display(spark.table("workspace.default.orders_processed"))

# COMMAND ----------

orders['CustomerID'].duplicated().sum()