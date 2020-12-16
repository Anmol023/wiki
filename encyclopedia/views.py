from django.shortcuts import render,HttpResponse,redirect
import re
from . import util
from markdown2 import Markdown
from django import forms
from random import choice

class NewForm(forms.Form):
	title = forms.CharField(label='Title', widget=forms.TextInput(attrs = {'class' : 'form-control col-md-3 col-lg-3'}))
	content = forms.CharField(widget=forms.Textarea(attrs = {'class' : 'form-control col-md-7 col-lg-7', 'rows':10}))
	edit = forms.BooleanField(widget=forms.HiddenInput(), initial='False', required=False)
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def title(request, name):
	entry = util.get_entry(name)
	if entry:
		markdowner = Markdown()
		return render(request, "encyclopedia/subject.html", {
			"subj": markdowner.convert(entry),
			"heading": name
			})
	else:
		return render(request, "encyclopedia/error.html", {
			"heading": name
			})
def search(request):
	if request.method == 'POST':
		value = request.POST['q']
		entry = util.list_entries()
		result = [i for i in entry if re.search(value, i, re.I)]
		if result:
			return render(request, "encyclopedia/index.html",{
				"entries": result,
				"search": True,
				"value": value
				})
		else:
			return render(request, "encyclopedia/error.html",{
				"heading" : value
				})
	else:
		return render(request, "encyclopedia/index.html",{
			"entries": result
			})
def new(request):
	if request.method == "POST":
		form = NewForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			content = form.cleaned_data["content"]
			if (util.get_entry(title) is None) or (form.cleaned_data["edit"]==True):
				util.save_entry(title, content)
				return redirect('title',title)
			else:
				return render(request, 'encyclopedia/new_page.html',{
					"title": title.upper(),
					"form": form,
					"present": True
					})
		else:
			return render(request, 'encyclopedia/new_page.html', {
				"form" : form,
				"present" : False
				})
	else:
		return render(request, 'encyclopedia/new_page.html',{
			"form": NewForm(),
			"present": False
			})

def edit(request, name):
	entryPage = util.get_entry(name)
	if entryPage is None:
		return render(request, "encyclopedia/error.html", {
    		"heading": name    
			})
	else:
		form = NewForm()
		form.fields["title"].initial = name     
		form.fields["title"].widget = forms.HiddenInput()
		form.fields["content"].initial = entryPage
		form.fields["edit"].initial = True
		return render(request, "encyclopedia/new_page.html", {
    		"form": form,
    		"edit": form.fields["edit"].initial,
    		"title": form.fields["title"].initial
			})
def random(request):
	c = util.list_entries()
	x = choice(c)
	return redirect('title', x)