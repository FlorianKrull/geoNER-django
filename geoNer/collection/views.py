from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Collection, Document, Version
from django.contrib.auth.models import User
from .forms import NewDocForm
from django.contrib.auth.decorators import login_required

import spacy
from spacy import displacy
# Create your views here.
def home(request):
    collections = Collection.objects.all()
    return render(request, 'home.html', {'collections': collections})

def collection_docs(request, pk):
    collection = Collection.objects.get(pk=pk)
    return render(request, 'docs.html', {'collection': collection})

@login_required
def new_doc(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    if request.method == 'POST':
        form = NewDocForm(request.POST)

        if form.is_valid():
            document = form.save(commit=False)
            document.collection = collection
            document.starter = request.user
            document.save()

            version = Version.objects.create(
                text = form.cleaned_data.get('text'),
                document = document,
                created_by=request.user
            )
            return redirect('collection_docs', pk=collection.pk) 
    else:
        form = NewDocForm()
    return render(request, 'new_doc.html', {'collection': collection})

def document_version(request, pk, document_pk):
    document = get_object_or_404(Document, collection__pk=pk, pk=document_pk)
    return render(request, 'document_version.html', {'document': document})


def ner_detection(request, pk, document_pk):
    version = get_object_or_404(Version, pk=document_pk)
    nlp = spacy.load("de")
    document = get_object_or_404(Document, collection__pk=pk, pk=document_pk)
    doc = nlp(version.text)
    html = displacy.render(doc, style="ent", page= True)
    return render(request, 'ner_detection.html', {'document': document,'html': html})
