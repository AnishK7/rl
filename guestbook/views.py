from django.shortcuts import render
from .forms import TodoForm,NewTodoForm
from .ama import ReadAsin
import subprocess,json

def convert_score_to_sentiment(score):
	score = float(score)
	if score < 0.5:
		return 'Negative'

	else:
		return 'Positive'


name1 = ''

def index(request):
	global name1
	print("Index")
	if request.method == 'GET':
		form = TodoForm() 
	else:
		form = TodoForm(request.POST)
		name1 = request.POST['txt1']
		return render(request,'guestbook/details.html',context={'name1':name1})
	return render(request,'guestbook/try1.html')


def algo(request):
	global name1
	if request.method == 'GET':
		form = NewTodoForm() 
	else:
		form = NewTodoForm(request.POST)
		print("Post")
		graph_option = request.POST.get('Graph_type')
		print('Graph: ',graph_option)

		
		if graph_option == 'pie_chart':
			#Amazon code
			output = ReadAsin(name1,1,5)  
			#Pyspark subprocess
			process = subprocess.check_output(['spark-submit', 'pysptest2.py'], shell=False)
			
			decoded_string = process.decode("unicode_escape").rstrip()
			decoded_list = [lines for lines in decoded_string.split("\n")]

			labels = [i for i in range(len(decoded_list[-1]))]
			data = list(map(float, decoded_list[-1].replace('[', '').replace(']', '').replace(', ', ',').split(',')))

			sentiments = [convert_score_to_sentiment(score) for score in data]

			sentiment_count = {
				'Negative': 0,
				'Neutral': 0,
				'Positive': 0
			}

			for sentiment in sentiments:
				sentiment_count[sentiment] += 1

			context = {
	        	'labels' : json.dumps(list(sentiment_count.keys())),
	        	'data' : json.dumps(list(sentiment_count.values()))
	    		}

			return render(request,'guestbook/chart.html',context=context)
		
		elif graph_option=='positive_reviews':
			score_per_page = []
			label = []
			sentiment_count_previous_page = {'Negative': 0,
					'Neutral': 0,
					'Positive': 0,
					'Total':0 }
			
			for i in range(6,30,5):
				label.append(i)
				
				output = ReadAsin(name1,i-5,i)  #Amazon extraction
				
				process = subprocess.check_output(['spark-submit', 'pysptest2.py'], shell=False)
				
				decoded_string = process.decode("unicode_escape").rstrip()
				decoded_list = [lines for lines in decoded_string.split("\n")]

				labels = [i for i in range(len(decoded_list[-1]))]
				data = list(map(float, decoded_list[-1].replace('[', '').replace(']', '').replace(', ', ',').split(',')))

				sentiments = [convert_score_to_sentiment(score) for score in data]

				sentiment_count = {
					'Negative': 0,
					'Neutral': 0,
					'Positive': 0,
					'Total':0
				}
				
				total = 0
				for sentiment in sentiments:
					sentiment_count[sentiment] += 1
					total+=1

				sentiment_count['Total']=total

				total_sentiments = sentiment_count['Total']+sentiment_count_previous_page['Total']
				percent = ((sentiment_count['Positive']+sentiment_count_previous_page['Positive'])/total_sentiments)*100			

				score_per_page.append(percent)
				sentiment_count_previous_page = sentiment_count

			context = {
		        'labels' : json.dumps(label),
		        'data' : json.dumps(score_per_page),
	    	    'legend' : json.dumps('Positive Percentage')
	    		}

			return render(request,'guestbook/no_of_reviews.html',context=context)



		else:
			score_per_page = []
			label = []
			sentiment_count_previous_page = {'Negative': 0,
					'Neutral': 0,
					'Positive': 0,
					'Total':0 }
			
			for i in range(6,30,5):
				label.append(i)
				output = ReadAsin(name1,i-5,i)  #Amazon extraction
				process = subprocess.check_output(['spark-submit', 'pysptest2.py'], shell=False)
				
				decoded_string = process.decode("unicode_escape").rstrip()
				decoded_list = [lines for lines in decoded_string.split("\n")]

				labels = [i for i in range(len(decoded_list[-1]))]
				data = list(map(float, decoded_list[-1].replace('[', '').replace(']', '').replace(', ', ',').split(',')))

				sentiments = [convert_score_to_sentiment(score) for score in data]

				sentiment_count = {
					'Negative': 0,
					'Neutral': 0,
					'Positive': 0,
					'Total':0
				}

				total = 0
				for sentiment in sentiments:
					sentiment_count[sentiment] += 1
					total+=1

				sentiment_count['Total']=total

				total_sentiments = sentiment_count['Total']+sentiment_count_previous_page['Total']
				percent = ((sentiment_count['Negative']+sentiment_count_previous_page['Negative'])/total_sentiments)*100			

				score_per_page.append(percent)
				sentiment_count_previous_page = sentiment_count

			context = {
		        'labels' : json.dumps(label),
		        'data' : json.dumps(score_per_page),
	    	    'legend' :json.dumps('Negative Percentage')
	    		}

			return render(request,'guestbook/no_of_reviews.html',context=context)



	return render(request, 'guestbook/try1.html', {
    'form': form,
  })
	