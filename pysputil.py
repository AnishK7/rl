import json
from nltk.sentiment.vader import SentimentIntensityAnalyzer
		
class Review:
	def __init__(self, review):
		self.text = str(' '.join(review['review_text']))
		self.rating = float(review['review_rating'])
		self.text_weight = 0.7
		self.rating_weight = 0.3

	def get_text_score(self):
		sid = SentimentIntensityAnalyzer()
		ss = sid.polarity_scores(self.text)
		self.text_score = self.text_weight * ss['compound']
		
		return self.text_score
		
	def get_rating_score(self):
		self.rating_score = self.rating_weight * self.rating
		return self.rating_score
		
	def get_score(self):
		self.get_text_score()
		self.get_rating_score()
		#print(self.text_score + self.rating_score)
		return self.text_score + self.rating_score
'''
if __name__ == '__main__':
	data = json.loads(open('guestbook/data.json').read())
	for product in data:
		review = Review(product)
		print(review.get_score())
'''
