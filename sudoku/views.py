from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from django import forms

import sudoku
import csv

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'accept':'.csv'}))

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
            board, solution = handle_uploaded_file(request.FILES['file'])
            request.session['solution'] = solution
            request.session['board'] = board

            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadFileForm()

        data = {}
        data['form'] = form
        data['solution'] = None
        data['board'] = None

        try:
            data['solution'] = load_board_from_session(request.session['solution'])
        except KeyError, TypeError:
            data['solution'] = None

        try:
            data['board'] = load_board_from_session(request.session['board'])
        except KeyError, TypeError:
            data['board'] = None

        request.session['solution'] = None

        if data['solution'] == -1:
            data['error'] = "Oh no! Something was wrong with your input :("

    return render(request, 'sudoku/index.html', data)

# Helper methods
def handle_uploaded_file(f):

    board, solution = [],[]
    reader = csv.reader(f)

    for row in reader:
        try:
            board.append(map(int, row))
            solution.append(map(int, row))
        except ValueError:
            return (-1, -1)

    sudoku.solveSudoku(solution)
    return board, solution
    #with open('some/file/name.txt', 'wb+') as destination:
    #    for chunk in f.chunks():
    #        destination.write(chunk)

def load_board_from_session(board):
    ret = []
    if board != None:
        try:
            for i in range(len(board)):
                ret.append([])
                for j in range(len(board)):
                    ret[i].append(board[i][j])
        except TypeError:
            return -1
    else:
        ret = None
    #data['solution'] = request.session['solution']
    return ret
