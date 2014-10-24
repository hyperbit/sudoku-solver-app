from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


from django import forms

import sudoku
import csv

class UploadFileForm(forms.Form):
    file = forms.FileField()

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)


def index(request):
    '''latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)'''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UploadFileForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #data = { 'form': NameForm(),
                     #'data': form.cleaned_data['your_name'] }
            solution = handle_uploaded_file(request.FILES['file'])

            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadFileForm()

    return render(request, 'sudoku/index.html', {'form': form})

# Helper method
def handle_uploaded_file(f):
    board = []
    reader = csv.reader(f)
    for row in reader:
        board.append(map(int, row))

    solution = sudoku.solveSudoku(board)
    return solution
    #with open('some/file/name.txt', 'wb+') as destination:
    #    for chunk in f.chunks():
    #        destination.write(chunk)
