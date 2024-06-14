from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django import forms
from django.urls import reverse
import markdown2
import random as rnd

from .util import list_entries, save_entry, get_entry

 
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries()
    })

def entry(request, title):
    if get_entry(title):
        html_content = markdown2.markdown_path(f"entries/{title}.md") # converts markdown file into html to be use for rendering
        return render(request, "encyclopedia/entry.html",{
            "html_content": html_content,
            "title": title
        })
    else:
        raise Http404("Error!, not found")

    
def search(request):
    if request.method == "POST":
        query = request.POST.get('q')
        if get_entry(query):
            return HttpResponseRedirect(reverse("entry", args=[query]))

        else:
            entries = list_entries()
            results = []

            for entry in entries: # wildcard or query matched 
                if query in entry.lower() or query in entry.upper():
                    results.append(entry)

            return render(request, "encyclopedia/search_results.html", {
               "results": results 
            })

def create_new(request):
    if request.method == "POST":
        title = request.POST.get('title') # fetches title for the entry
        content = request.POST.get('content')# fetches content for the entry
        entries = list_entries() # gives back list of existing entry 
        if title in entries:
            return HttpResponse("Error, File already exist!")
        else:
            content = f"# {title}"+ "\n\n" + content # inject title page into markdown content
            save_entry(title, content) # saves our entry in entries file
            return HttpResponseRedirect(reverse("entry", args=[title]))

    else:
        return render(request, "encyclopedia/create_new.html")

def edit(request, title):

    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))

    else:
        with open(f"entries/{title}.md", 'r') as file:
            markdown_content = file.read()        
        if markdown_content:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "markdown_content": markdown_content
            })
        
def random(request):
    entries = list_entries()
    return HttpResponseRedirect(reverse("entry", args=[rnd.choice(entries)]))
