from pysputil import Review
from pyspark.sql import SQLContext
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark.ml.feature import StopWordsRemover
from pyspark.sql.functions import udf, col
from pyspark.sql.types import FloatType
from sklearn.preprocessing import MinMaxScaler
import numpy as np

conf = SparkConf()
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")
sqlContext = SQLContext(sc)

reviews = sqlContext.read.json("data.json",multiLine=True)

remover = StopWordsRemover(inputCol='review_text',outputCol='Filtered', stopWords=StopWordsRemover.loadDefaultStopWords('english'))
filtered_reviews = remover.transform(reviews)
#filtered_reviews.show(truncate=False)
join_udf = udf(lambda x: " ".join(x))
filtered_reviews.withColumn("Filtered", join_udf(col("Filtered")))

users_objs = filtered_reviews.rdd.map(lambda entry: Review(entry))
value = users_objs.map(lambda entry: Review.get_score(entry))

df2 = sqlContext.createDataFrame(value,FloatType())

mvv_list = [row['value'] for row in df2.collect()]

scaler = MinMaxScaler(feature_range=(0, 1))

mvv_list=np.asarray(mvv_list).reshape(-1,1)
mvvv_list = scaler.fit_transform(mvv_list)
mvvv_list=mvvv_list.ravel().tolist()
print(mvvv_list)
