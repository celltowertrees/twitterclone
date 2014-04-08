import requests
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template, loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse

from models import Item
from forms import ItemForm


def index(request):
	items = Item.objects.order_by('-created')
	item_form = ItemForm()

	return render(request, 'rsblog-fork/index.html', {
		'items': items,
		'item_form': item_form,
		})


def single_item(request, post):
	try: 
		single = Item.objects.get(slug=post)
	except Item.DoesNotExist:
		raise Http404
	return HttpResponse("Single Item: %s" % item)


# def add_item()
