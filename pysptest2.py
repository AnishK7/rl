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
#val sqlContext = new SQLContext(sc)
reviews = sqlContext.read.json("data.json",multiLine=True)

#tokenizer = Tokenizer(inputCol="sentence", outputCol="words")

remover = StopWordsRemover(inputCol='review_text',outputCol='Filtered', stopWords=StopWordsRemover.loadDefaultStopWords('english'))
filtered_reviews = remover.transform(reviews)
#filtered_reviews.show(truncate=False)
join_udf = udf(lambda x: " ".join(x))
filtered_reviews.withColumn("Filtered", join_udf(col("Filtered")))


users_objs = filtered_reviews.rdd.map(lambda entry: Review(entry))
#print('users_objs')
value = users_objs.map(lambda entry: Review.get_score(entry))
#print("Values")
#print(type(value))

df2 = sqlContext.createDataFrame(value,FloatType())
#df2.show()
mvv_list = [row['value'] for row in df2.collect()]


scaler = MinMaxScaler(feature_range=(0, 1))
mvv_list=np.asarray(mvv_list).reshape(-1,1)
mvvv_list = scaler.fit_transform(mvv_list)
mvvv_list=mvvv_list.ravel().tolist()
print(mvvv_list)



#return df2
#sample2 = sample.rdd.map(lambda x: (x.name, x.age, x.city))
#val = sys.exit(run_process())
#val.show()

#reviews = [Review(r) for r in reviews]

#products = text_df.filter(lambda rows: stop_words not in rows.collect())
#print(text_df)

#products = products.select('reviews').collect()
#print(products[0]['reviews']):Review for each object
#products = [Product(p) for p in products]
#products : List of Product objects
#for product in products:
 #   print(product.reviews[2].text)
  #  print(product.get_scores())
    

