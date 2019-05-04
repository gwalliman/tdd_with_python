from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Item, List
from .forms import ItemForm


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    newlist = List.objects.get(id=list_id)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(data=request.POST)
        if form.is_valid():
            Item.objects.create(text=request.POST['text'], list=newlist)
            return redirect(newlist)
    return render(request, 'list.html', {'list': newlist, 'form': form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        newlist = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=newlist)
        return redirect(newlist)
    else:
        return render(request, 'home.html', {"form": form})
