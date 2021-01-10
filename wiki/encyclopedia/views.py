from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

class newForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"rows":0.1, "cols":80, 'style': 'height: 20em;'}))


def index(request, entries = 0):
    if entries == 0:
        entries = util.list_entries()
    return render(request, "encyclopedia/index.html", { 
        'entries': entries
        })

def entry(request, title):
	#  1. get the content of the encyclopedia entry
	#  2. If an entry is requested that does not exist, the user should be presented with an error page
	#  3. If the entry does exist, the user should be presented with a page that displays the content of the entry. The title of the page should include the name of the entry.
	if util.get_entry(title) is not None:
		return render(request, "encyclopedia/entry.html", {
			"title": title,
			"content": markdown2.markdown(util.get_entry(title))
			})
	else: return render(request, "encyclopedia/error.html", {
        'error': "Sorry, requested page was not found."
        })

def search(request):
    #   1. get the value from the search bar
    #   2. if the value is found return the entry
    #   3. if is not return the posibilities and/or create new one
    q = request.GET.get('q', '')
    if util.get_entry(q) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'title': q }))
    else:
        posibilities = []
        for i in util.list_entries():
            if q.upper() in i.upper():
                posibilities.append(i)
        return render(request, "encyclopedia/index.html", { 
        'entries': posibilities,
        'search': True,
        'q': q
        })

def add(request):
    #   1. Users should be able to enter a title for the page and, in a textarea, should be able to enter the Markdown content for the page.
    #                     !!! util.py was modified. Now the Title of the form is saved as Markdown title on the file. 
    #   2. Users should be able to click a button to save their new page.
    #   3. When the page is saved, if an encyclopedia entry already exists with the provided title, the user should be presented with an error message.
    #   4. Otherwise, the encyclopedia entry should be saved to disk, and the user should be taken to the new entry’s page.
    if request.method == "POST":
        form = newForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry_add(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
            else: 
                return render(request, "encyclopedia/error.html", {
                'error': "Sorry, encyclopedia entry already exists."
                })
    else:
        return render(request, "encyclopedia/add.html", {
            "form": newForm()
        })  

def edit(request, title):
    #   1. The textarea should be pre-populated with the existing Markdown content of the page. (i.e., the existing content should be the initial value of the textarea).
    #   2. The user should be able to click a button to save the changes made to the entry.
    #   3. Once the entry is saved, the user should be redirected back to that entry’s page.
    if request.method == "POST":
        form = newForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    else:
        entryPage = util.get_entry(title)
        form = newForm()
        form.fields["title"].initial = title
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        return render(request, "encyclopedia/edit.html", {
            "form": form
        })  


def randomEntry(request):
    entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", kwargs={'title': entry}))      


