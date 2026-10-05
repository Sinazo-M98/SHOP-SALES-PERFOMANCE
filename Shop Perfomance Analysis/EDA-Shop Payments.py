# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# DBTITLE 1,Importing Libraries
import pandas as pd
import numpy as np

# COMMAND ----------

# DBTITLE 1,Ingesting Payments Table
payments=spark.table('shop.perfomance.payments')
payments=payments.toPandas()
display(payments)

# COMMAND ----------

# DBTITLE 1,Checking my table
payments.shape

# COMMAND ----------

payments.head

# COMMAND ----------

payments.info()

# COMMAND ----------

payments.isnull().sum()

# COMMAND ----------

# MAGIC %md
# MAGIC ###Observations
# MAGIC Im observing on payment dates we have 35 nulls, which we also had 35 null orderdates on the orders table and for both tables we have 50000 rows-Tables could be related?

# COMMAND ----------

payments[payments["PaymentDate"].isnull()].head(10)