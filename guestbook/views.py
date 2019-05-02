from django.shortcuts import render

from .models import Comment

from .forms import TodoForm
from .ama import ReadAsin
import subprocess,json

def convert_score_to_sentiment(score):
	score = float(score)
	if score < 0.5:
		return 'Negative'

	else:
		return 'Positive'

# Create your views here.
def index(request):
	#SScomments = Comment.objects.order_by('-date_added')
	#form = TodoForm()	
	print("INdex")
	if request.method == 'GET':
		form = TodoForm() 
	else:
		form = TodoForm(request.POST)
		print("Post")
		name1 = request.POST['txt1']
		
		output = ReadAsin(name1)  #Amazon extraction
			#context = {'comments' : comments, 'form' : newtodoform}

		#process =  subprocess.Popen(['spark-submit', 'pysptest2.py'], stdout=subprocess.PIPE)  #Pyspark code
		process = subprocess.check_output(['spark-submit', 'pysptest2.py'], shell=False)
		#val = process.wait()
		#out = process.communicate()
		return_code = 67
		#lst = ast.literal_eval(process.decode("ascii"))
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

		#process.kill()
		#line = process.stdout.readline()
		print('DONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!')
		print(sentiment_count)
		#print('OUT: ',out)
		print(decoded_list[-1])

		context = {
        'labels' : json.dumps(list(sentiment_count.keys())),
        'data' : json.dumps(list(sentiment_count.values()))
    }

		return render(request,'guestbook/chart.html',context=context)

	return render(request, 'guestbook/try1.html', {
    'form': form,
  })
	

'''
def addtodo(request):
	#form = TodoForm(request.POST)
	newtodoform = NewTodoForm(request.POST)

	if newtodoform.isvalid():
		#new_todo = Comment(text=form.cleaned_data['name'])
		#new_todo.save()
		new_todo = newtodoform.save()
		return redirect('index')

'''