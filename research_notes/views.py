from django.http import Http404, HttpResponse
from os import path
from django.shortcuts import render
import markdown
# import mistune
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.dollarmath.index import dollarmath_plugin
from research_notes.settings import BASE_DIR
from .project_variables import fs_tree_to_dict, iterdict
import json, os
from django.utils.safestring import mark_safe
from django.utils.html import escapejs


def homepage(request):
    return render(request, 'home.html')

def displayFile(request, parent, file_name='', path_to_file=''):
    # boolean = path.exists('templates/all_notes/classes/econ101/My First Note.md')
    print("Hello")
    file = f'templates/all_notes/{parent}/{path_to_file}/{file_name}'
    file_exists = path.exists(file.strip("/"))
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

    return render(request, "file-display.html", {"file_contents": html})
    
def displayFolder(request, file):
    file = file.strip("/")
    folder_name = file.split("/")[-1]
    folder_name = folder_name.replace('_', ' ').title()
    tree_dict = fs_tree_to_dict(BASE_DIR / file)
    generated_html = iterdict(d=tree_dict, level=-1, parent=os.path.abspath(file))
    # print("Generated This: ", generated_html)
    return render(request, "folder-tree.html", {"folder_name": folder_name, "folder_tree":  generated_html})