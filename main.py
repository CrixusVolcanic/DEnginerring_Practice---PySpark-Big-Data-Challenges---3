from libraries.pyspark_env import PySparkEnv
from libraries.sparksql_env import SparkSql

def main():
    
    # objPyS = PySparkEnv()
    # objPyS.main()

    objSparkSql = SparkSql()
    objSparkSql.main()



if __name__=="__main__":
    main()