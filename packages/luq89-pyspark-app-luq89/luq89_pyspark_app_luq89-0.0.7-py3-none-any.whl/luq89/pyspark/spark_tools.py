from pyspark.sql.session import SparkSession


def get_spark_session():
    spark = SparkSession \
        .builder \
        .appName("Spark Example") \
        .getOrCreate()
    return spark


def get_spark_version(spark_session):
    return spark_session.version


spark = get_spark_session()
print(get_spark_version(spark))

