import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk,csv
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, classification_report

yelp = pd.read_csv('yelp2.csv')
q=yelp.shape
#print (q)
#print(yelp.head())
yelp['text length'] = yelp['text'].apply(len)
#print(yelp.head())
g = sns.FacetGrid(data=yelp, col='stars')
g.map(plt.hist, 'text length', bins=50)
#plt.show()
sns.boxplot(x='stars', y='text length', data=yelp)
#plt.show()

stars = yelp.groupby('stars').mean()
stars.corr()
sns.heatmap(data=stars.corr(), annot=True)
#plt.show()

yelp_class = yelp[(yelp['stars'] == 0) | (yelp['stars'] == 1)]
yelp_class.shape

X = yelp_class['text']
y = yelp_class['stars']

def text_process(text):
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

bow_transformer = CountVectorizer(analyzer=text_process).fit(X)
len(bow_transformer.vocabulary_)
X = bow_transformer.transform(X)
#print('Shape of Sparse Matrix: ', X.shape)
#print('Amount of Non-Zero occurrences: ', X.nnz)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.0, random_state=101)
nb = MultinomialNB()
nb.fit(X_train, y_train)
#review = ['Bad food quality. Bad service.']
#review = ['Bad food quality.']
#review = ['good food quality.']
#review = ['The food was mediocre too. never recommending this to anybody.']
#review = ['service is not bad. food quality is poor.']
#review = ['bad.']
#review = ['Staff is Courtois. Food is average but priced above average. Varieties of dosa is available. Coffee is good. Ambience is average']
#review = ['Had lunch here before catching the train to Delhi. Clean enough restaurant, prices very good, but service left a little to be desired. When we sat down they provided a bottle of water, but no glasses. We had to ask to have glasses brought. I ordered a veggie burger, and requested it come without lettuce or tomato, as I was concerned with any uncooked vegetables. When the burger arrived, it was covered with shredded lettuce and tomatoes and smothered with what looked like thousand island dressing. I spend 15 minutes scrapping all the dressing and shredded lettuce off the bun before I could eat it. The burger itself tasted fine.']
positive = 0
negative = 0
test = csv.reader(open('test.csv'))

for each_row in test:
	review = each_row
	review_transformed = bow_transformer.transform([review])
	xd=nb.predict(review_transformed)[0]
	if xd == 0.0:
		negative += 1
	else:
		positive +=1

print('Positive',positive)
print('Negative',negative)

#preds = nb.predict(X_test)
#print(confusion_matrix(y_test, preds))
#print('\n')\
#print(classification_report(y_test, preds))















