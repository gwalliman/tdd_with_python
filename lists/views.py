from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    newlist = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=newlist)
            item.full_clean()
            item.save()
            return redirect(f'/lists/{newlist.id}/')
        except ValidationError:
            error = "You can't have an empty list item"
    return render(request, 'list.html', {'list': newlist, 'error': error})


def new_list(request):
    newlist = List.objects.create()
    item = Item(text=request.POST['item_text'], list=newlist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        newlist.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {"error": error})
    return redirect(f'/lists/{newlist.id}/')
