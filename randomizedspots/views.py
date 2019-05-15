from django.shortcuts import render
import random
def show_randomized_tools(request):
    from .models import Recoverytoolsbulk
    mylist = []
    allthetools = Recoverytoolsbulk.objects.in_bulk()
    # in_bulk produces a standard Python dictionary


    for tool in allthetools.values():
        mylist.append(str(tool))
    random.shuffle(mylist, random.random)
    thefirsttool=mylist[0]
    return(render(request, 'show_randomized_tools.html', {'thefirsttool':  thefirsttool}))


