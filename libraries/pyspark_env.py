from libraries.util import setup_logger
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType, FloatType
from pyspark.sql.functions import to_timestamp, when, year, row_number, desc
from pyspark.sql.window import Window

class PySparkEnv:

    def __init__(self) -> None:
        self.logger = setup_logger(name="PySpark", log_file="pyspark.log")


    def main():
        spark = SparkSession.builder.appName("Challenge 3").getOrCreate()

        #Load data
        clients_df = spark.read.format("csv").load("resources/clientes_reducido.csv", header=True)
        clients_df = clients_df.dropDuplicates()

        transacciones_df = spark.read.format("json").load("resources/transacciones_reducido.json")
        transacciones_df = transacciones_df.dropDuplicates()

        #Join Data
        df = clients_df.join(transacciones_df, "customer_id")

        #Data Transformation
        df = df.withColumn("edad", df["edad"].cast(IntegerType())) \
                .withColumn("amount", df["amount"].cast(FloatType())) \
                .withColumn("timestamp", to_timestamp(df["timestamp"]))
        
        df = df.filter(df["amount"] > 0)

        df = df.withColumn("amount_usd", round(df["amount"] * when(df["currency"] == "COP", 0.00023)
                                                                .when(df["currency"] == "EUR", 1.05)
                                                                .when(df["currency"] == "MXN", 0.049)
                                                                .otherwise(1)
                                                , 2))
        
        df = df.withColumn("year", year(df["timestamp"]))

        #Data Aggregations
        df.groupby("customer_id", "país").sum("amount_usd").orderBy("customer_id").show(10)

        df_customer_product = df.groupby("customer_id", "product_id").sum("amount_usd")
        df_customer_product = df_customer_product.withColumn("row_number", row_number().over(Window.partitionBy("customer_id").orderBy(desc('sum(amount_usd)'))))
        df_customer_product = df_customer_product.filter(df_customer_product["row_number"] == 1)
        df_customer_product.show()

        df.write.mode("overwrite").format("parquet").partitionBy("year", "país").save("results/data.parquet")