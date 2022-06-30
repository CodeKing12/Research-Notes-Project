from django.http import Http404, HttpResponse
from os import path
from django.shortcuts import render
import markdown
# import mistune
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.dollarmath.index import dollarmath_plugin

def homepage(request):
    return render(request, 'home.html')

def displayFile(request, parent, file_name='', path_to_file=''):
    # boolean = path.exists('templates/all_notes/classes/econ101/My First Note.md')
    file = f'templates/all_notes/{parent}/{path_to_file}/{file_name}'
    file_exists = path.exists(file)
    if not file_exists:
        raise Http404
    
    if path.isdir(file):
        response = displayFolder(request, file)
        return response

    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    md = (
        MarkdownIt()
        .use(front_matter_plugin)
        .use(footnote_plugin)
        .use(dollarmath_plugin)
        .disable('image')
        .enable('table')
    )

    print(md.parse)
    html = md.render(content)

    return HttpResponse(html)
    
def displayFolder(request, file):
    return HttpResponse(file)