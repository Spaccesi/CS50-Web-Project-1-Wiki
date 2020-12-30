from django.shortcuts import render
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
	if util.get_entry(title):
		return render(request, "encyclopedia/entry.html", {
			"title": title.capitalize(),
			"content": markdown2.markdown(util.get_entry(title))
			})
	else: return render(request, "encyclopedia/error.html")


