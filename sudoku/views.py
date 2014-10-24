from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render



from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

def index(request):
    '''latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return render(request, 'sudoku/index.html', {'form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'sudoku/index.html', {'form': form})
