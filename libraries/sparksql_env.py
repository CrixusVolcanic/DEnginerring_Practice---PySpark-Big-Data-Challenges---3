from libraries.util import setup_logger
from pyspark.sql import SparkSession

class SparkSql:

    def __init__(self) -> None:
        self.logger = setup_logger(name="SparkSql", log_file="sparksql.log")

    def main(self):

        self.logger.info("Process started")

        spark = SparkSession.builder.appName("Challenge 3").getOrCreate()

        #Load data
        clients_df = spark.read.format("csv").load("resources/clientes_reducido.csv", header=True)
        clients_df = clients_df.dropDuplicates()
        clients_df.createOrReplaceTempView("clients_raw")

        transacciones_df = spark.read.format("json").load("resources/transacciones_reducido.json")
        transacciones_df = transacciones_df.dropDuplicates()
        transacciones_df.createOrReplaceTempView("transactions_raw")

        spark.sql("""
                    create or replace temp view raw_data as
                    select *
                    from clients_raw cr
                    join transactions_raw tr using(customer_id)
                       """)

        self.logger.info(f"The data has been loaded")

        spark.sql("""
                    create or replace temp view transformed_data as
                    WITH transformed_data AS (SELECT 
                                                customer_id
                                                ,nombre
                                                ,`país` pais
                                                ,CAST(edad AS INTEGER) AS edad
                                                ,"género" genero
                                                ,CAST(amount AS FLOAT) AS amount
                                                ,currency
                                                ,product_id
                                                ,TO_TIMESTAMP(timestamp) AS timestamp
                                                ,transaction_id
                                            FROM raw_data
                                            WHERE CAST(amount AS FLOAT) > 0
                                            )
                    ,amount_usd_calculated AS (SELECT *
                                                ,ROUND(amount * CASE 
                                                                    WHEN currency = 'COP' THEN 0.00023
                                                                    WHEN currency = 'EUR' THEN 1.05
                                                                    WHEN currency = 'MXN' THEN 0.049
                                                                    ELSE 1
                                                                END, 2) AS amount_usd
                                                FROM transformed_data
                                                )
                    SELECT *
                    ,YEAR(timestamp) AS year
                    FROM amount_usd_calculated;
                    """)
        
        self.logger.info(f"The data transformation has been done")

        spark.sql("""
                  SELECT customer_id
                      ,pais
                      ,SUM(amount_usd) AS total_amount_usd
                    FROM transformed_data
                    GROUP BY customer_id , pais
                    ORDER BY customer_id
                    LIMIT 10;""").show()
        
        spark.sql("""
                  WITH customer_product_sums AS (
                    SELECT 
                        customer_id
                        , product_id
                        , SUM(amount_usd) AS total_amount_usd
                    FROM transformed_data
                    GROUP BY 
                        customer_id
                        , product_id
                    )
                    , ranked_products AS (
                    SELECT 
                        customer_id
                        , product_id
                        , total_amount_usd
                        , ROW_NUMBER() OVER (
                            PARTITION BY customer_id 
                            ORDER BY total_amount_usd DESC
                        ) AS row_number
                    FROM customer_product_sums
                    )
                    SELECT 
                    customer_id
                    , product_id
                    , total_amount_usd
                    FROM ranked_products
                    WHERE row_number = 1;""").show()
        
        self.logger.info(f"Data aggregations has been done")
        
        spark.table("transformed_data").write.mode("overwrite").format("parquet").partitionBy(["year", "pais"]).save("results/data_ss.parquet")

        self.logger.info(f"The results has been export, the format is parquet partition by Year/Country")



