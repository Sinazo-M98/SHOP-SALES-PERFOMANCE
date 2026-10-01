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

# DBTITLE 1,INSPECTING DISOUNT COLUMN
####checking data type and unique counts
orders["Discount"].value_counts(dropna=False)


# COMMAND ----------

# DBTITLE 1,INSPECTING QUANTITY COLUMN
orders["Quantity"].value_counts(dropna=False)

# COMMAND ----------

# DBTITLE 1,INSPECTING PAYMENT METHOD
orders["PaymentMethod"].value_counts(dropna=False)