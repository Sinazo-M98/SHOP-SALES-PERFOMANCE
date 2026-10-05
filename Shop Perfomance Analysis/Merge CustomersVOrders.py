# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "6"
# ///
# 1. Load the two processed tables from Default Catalog
customers= spark.read.table("workspace.default.customers_processed")
orders= spark.read.table("workspace.default.orders_processed")

# 2. Merge (Join) on the common column- by leftjoin
customers_orders= customers.join(orders, on="CustomerID", how="left")

# 3. Save the result back to your catalog
customers_orders.write \
    .mode("overwrite") \
    .format("delta") \
    .saveAsTable("workspace.default.customers_orders")

# COMMAND ----------

display(spark.table("workspace.default.customers_orders").limit(10))