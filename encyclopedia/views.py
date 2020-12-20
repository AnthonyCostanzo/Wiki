import random

from django import forms
from django.shortcuts import render

from . import util
import markdown2

markdowner = markdown2.Markdown()


class Search(forms.Form):
    entry = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search Encyclopedia'}))

class Post(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
    entries = util.list_entries()
    searched = []
    if request.method == "POST":
        form = Search(request.POST)
        if form.is_valid():
            entry = form.cleaned_data["entry"]
            for i in entries:
                if entry in entries:
                    entry = util.get_entry(entry)
                    entry_converted = markdowner.convert(entry)
                    
                    content = {
                        'entry': entry_converted,
                        'title': entry,
                        'form': Search()
                    }

                    return render(request, "encyclopedia/show.html", content)
                if entry.lower() in i.lower(): 
                    searched.append(i)
                    content = {
                        'searched': searched, 
                        'form': Search()
                    }
            return render(request, "encyclopedia/search.html", content)

        else:
            return render(request, "encyclopedia/index.html", {"form": form})
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(), "form":Search()
        })

def show(request, title):
    entries = util.list_entries()
    if title in entries:
        entry = util.get_entry(title)
        entry_converted = markdowner.convert(entry) 

        content = {
            'entry': entry_converted,
            'title': title,
            'form': Search()
        }

        return render(request, "encyclopedia/show.html", content)
    else:
        return render(request, "encyclopedia/error.html", {"message": "entry not found.", "form":Search()})


def new(request):
    if request.method == 'POST':
        form = Post(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html", {"form": Search(), "message": "entry already exist"})
            else:
                util.save_entry(title,textarea)
                entry = util.get_entry(title)
                entry_converted = markdowner.convert(entry)

                content = {
                    'form': Search(),
                    'entry': entry_converted,
                    'title': title
                }

                return render(request, "encyclopedia/show.html", content)
    else:
        return render(request, "encyclopedia/new.html", {"form": Search(), "post": Post()})


def edit(request, title):
    if request.method == 'GET':
        entry = util.get_entry(title)
        
        content = {
            'form': Search(),
            'edit': Edit(initial={'textarea': entry}),
            'title': title
        }

        return render(request, "encyclopedia/edit.html", content)
    else:
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            entry = util.get_entry(title)
            entry_converted = markdowner.convert(entry)

            content = {
                'form': Search(),
                'entry': entry_converted,
                'title': title
            }

            return render(request, "encyclopedia/show.html", content)

def randomPage(request):
    if request.method == 'GET':
        entries = util.list_entries()
        num = random.randint(0, len(entries) - 1)
        entry_random = entries[num]
        entry = util.get_entry(entry_random)
        entry_converted = markdowner.convert(entry)

        content = {
            'form': Search(),
            'entry': entry_converted,
            'title': entry_random
        }

        return render(request, "encyclopedia/show.html", content)



