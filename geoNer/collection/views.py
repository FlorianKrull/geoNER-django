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
    #nlp = spacy.load("en_core_web_sm")
    #doc = nlp(text)
    #print(displacy.render(doc, style="ent",page=True))
    #return displacy.render(doc, style="ent",page=True)
    document = get_object_or_404(Document, collection__pk=pk, pk=document_pk)
    return render(request, 'ner_detection.html', {'document': document})


def visualize_view(request):
    ret = {}
    text = request.POST.get('sentences')
    if (text is None):
        return render(request, 'nlp/visualize_error.html')
    markup = visualize_text(text)
    ret['json'] = markup
    return render(request, 'nlp/visualize.html', ret)


def analyze(request):
    'API text analyze view'
    if request.method == 'POST':
        text = request.body.decode('utf-8')
        try:
            text = json.loads(text)['text']
        except ValueError:
            # catch POST form as well
            for key in request.POST.dict().keys():
                text = key

        if settings.ALLOW_URL_IMPORTS and text.startswith(('http://', 'https://', 'www')):
            page = requests.get(text)
            doc = Document(page.text)
            soup = BeautifulSoup(doc.summary())
            text = soup.get_text()
            title = doc.title().strip()
            text = '{0}.\n{1}'.format(title, text)

        if not text:
            response = JsonResponse(
                {'status': 'false', 'message': 'need some text here!'})
            response.status_code = 400
            return response

        # add some limit here
        text = text[:200000]
        ret = {}
        ret = analyze_text(text)
        return JsonResponse(ret)
    else:
        ret = {'methods_allowed': 'POST'}
        return JsonResponse(ret)
