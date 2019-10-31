from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Collection, Document, Version
from django.contrib.auth.models import User
from .forms import NewDocForm

# Create your views here.
def home(request):
    collections = Collection.objects.all()
    return render(request, 'home.html', {'collections': collections})

def collection_docs(request, pk):
    collection = Collection.objects.get(pk=pk)
    return render(request, 'docs.html', {'collection': collection})

def new_doc(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewDocForm(request.POST)

        if form.is_valid():
            document = form.save(commit=False)
            document.collection = collection
            document.starter = user
            document.save()

            version = Version.objects.create(
                text = form.cleaned_data.get('text'),
                document = document,
                created_by = user
            )
            return redirect('collection_docs', pk=collection.pk) 
    else:
        form = NewDocForm()
    return render(request, 'new_doc.html', {'collection': collection})