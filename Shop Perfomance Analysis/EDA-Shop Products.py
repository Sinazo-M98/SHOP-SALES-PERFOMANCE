# Databricks notebook source
# DBTITLE 1,Importing Libraries
#####Import libraries
import pandas as pd
import numpy as np

# COMMAND ----------

# DBTITLE 1,Ingesting my table
products=spark.table("shop.perfomance.products")
products=products.toPandas()
display(products)


# COMMAND ----------

# DBTITLE 1,Checking datatypes on my table
products.dtypes

# COMMAND ----------

# DBTITLE 1,Checking unique ProductNameand counting
counts=products["ProductName"].value_counts()
print(counts)

# COMMAND ----------

# DBTITLE 1,Checking for duplicates on my data
products.duplicated().sum()

# COMMAND ----------

# DBTITLE 1,checking for null values
products.isnull()

# COMMAND ----------

# DBTITLE 1,Describing my data in my numerical columns
products.describe()