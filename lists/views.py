from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    newlist = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': newlist})


def new_list(request):
    newlist = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=newlist)
    return redirect(f'/lists/{newlist.id}/')


def add_item(request, list_id):
    newlist = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=newlist)
    return redirect(f'/lists/{newlist.id}/')


