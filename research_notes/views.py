from urllib import response
from django.http import Http404, HttpResponse
from os import path
from django.shortcuts import render
import markdown
# import mistune
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.dollarmath.index import dollarmath_plugin
from notes.models import Folder, Tags, normalNotes
from research_notes.settings import BASE_DIR
from .project_variables import fs_tree_to_dict, iterdict
import json, os
from django.utils.safestring import mark_safe
from django.utils.html import escapejs
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


def homepage(request):
    all_tags = Tags.objects.all()
    root_parent = Folder.objects.get(name="All Notes")
    full_path = root_parent.path
    tree_dict = fs_tree_to_dict(full_path)
    nav_html = iterdict(d=tree_dict, level=-1, parent=full_path)
    return render(request, 'home.html', {"nav_html": nav_html, "all_tags": all_tags})

def resolveObject(request, path_to_file):
    path_to_file = path_to_file.strip("/")
    path_list = path_to_file.split("/")
    slug = path_list[-1]
    parent_path = "/".join(path_list[:-1])
    # path_to_file = f"/{path_to_file}"
    if parent_path == "":
        model_parent = Folder.objects.get(name="All Notes")
    else:
        model_parent = Folder.objects.get(path=f"/{parent_path}")
    try:
        # print(file_name, model_parent_fold.id)
        model_file = normalNotes.objects.get(slug=slug, parent_folder=model_parent)
    except ObjectDoesNotExist:
        try:
            # print(slug, model_parent)
            folder = Folder.objects.get(slug=slug, parent=model_parent)
            # print(folder)
        except ObjectDoesNotExist:
            raise Http404
            file_exists = path.exists(file.strip("/"))
            if not file_exists:
                raise Http404
    
    try:
        response = displayFile(request, model_file)
    except UnboundLocalError:
        response = displayFolder(request, folder)

    return response
        
def displayFile(request, file):
    # print(file.papers.bibtex.file)
    return render(request, "file-display.html", {"file": file})

def displayFolder(request, folder):
    folder_name = folder.name.replace('_', ' ').title()
    root_parent = Folder.objects.get(name="All Notes")
    full_path = root_parent.path + folder.path
    tree_dict = fs_tree_to_dict(full_path)
    print("Heyaa", BASE_DIR / folder.path)
    generated_html = ""
    print()
    print(tree_dict)
    generated_html = iterdict(d=tree_dict, level=-1, parent=full_path)
     # print("Generated This: ", generated_html)
    return render(request, "folder-tree.html", {"folder_name": folder_name, "folder_tree":  generated_html})

def all_tags(request):
    all_tags = Tags.objects.all()
    # print(all_tags.notes)
    return render(request, "all_tags.html", {"all_tags": all_tags})

def all_categories(request):
    all_tags = Tags.objects.all()
    # print(all_tags.notes)
    return render(request, "all_categories.html", {"all_tags": all_tags})

def tag(request, tag_name):
    tag = Tags.objects.get(name=tag_name)
    return render(request, "tag.html", {"tag": tag})