from urllib import response
from django.http import Http404, HttpResponse
from os import path
from django.shortcuts import render, get_object_or_404, redirect
import markdown
# import mistune
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from mdit_py_plugins.dollarmath.index import dollarmath_plugin
from notes.models import Folder, Tags, Type, normalNotes
from research_notes.settings import BASE_DIR
from .project_variables import fs_tree_to_dict, iterdict
import json, os
from django.utils.safestring import mark_safe
from django.utils.html import escapejs
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

import environ
env = environ.Env()

def sortDate(item):
    return item.date_modified

def sortTitle(item):
    return item.title

def sortName(item):
    return item.name

def sortPopularity(item):
    return item.note.count()

def sortTagName(item):
    return item.name

def homepage(request):
    all_tags = Tags.objects.all()
    root_parent = get_object_or_404(Folder, name="All Notes")
    full_path = root_parent.path
    tree_dict = root_parent.folder_dict
    nav_html = iterdict(d=tree_dict, level=-1, parent=full_path)
    all_types = Type.objects.all()
    return render(request, 'home.html', {"nav_html": nav_html, "all_tags": all_tags, "all_types": all_types})

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

def displayFolder(request, folder, sort="title", group="none"):
    if request.method == "GET" and "sort" in request.GET:
        sort = request.GET["sort"].lower()
        group = request.GET["group"].lower()
    # Generated the html for the directory tree section
    folder_name = folder.presentable_name()
    root_parent = Folder.objects.get(name="All Notes")
    full_path = root_parent.path + folder.path
    tree_dict = folder.folder_dict
    generated_html = ""
    generated_html = iterdict(d=tree_dict, level=-1, parent=full_path)

    # Retrieve the corresponding file_name in the subfiles list and replace it with the object to django model objects
    for file in folder.subfiles:
        if file.endswith(".md"):
            file_index = folder.subfiles.index(file)
            folder.subfiles[file_index] = normalNotes.objects.get(name=file, parent_folder=folder)
        else:
            folder.subfiles.remove(file)

    for sub_folder in folder.subfolders:
        # folder_name = folder.name.replace('_', ' ').title()
        folder_index = folder.subfolders.index(sub_folder)
        subfold = Folder.objects.get(name=sub_folder, parent=folder)
        folder.subfolders[folder_index] = subfold
    # Sort Items By title or date_modified if the user requests to sort them out
    if sort == "title":
        folder.subfiles.sort(key=sortTitle)
    elif sort == "modified":
        folder.subfiles.sort(key=sortDate)

    # Create lists for grouping Items By tags or status if the user requests to group them
    if group == "tags":
        group_list = []
        for file in folder.subfiles:
            for tag in file.tags.all():
                if tag not in group_list:
                    group_list.append(tag)
    elif group == "status":
        group_list = []
        for file in folder.subfiles:
            if file.status not in group_list:
                group_list.append(file.status)
    else:
        group_list = []

    current_sorting = sort.title()
    current_grouping = group.title()
    sort_options = ["Title", "Date Modified"]
    group_options = ["None", "Status", "Tags"]
    return render(request, "folder-tree.html", {"folder_name": folder_name, "folder_tree":  generated_html, "folder": folder, "group_list": group_list, "current_sorting": current_sorting, "current_grouping": current_grouping, "sort_options": sort_options, "group_options": group_options})

def all_tags(request, sort="popularity", ascending=False):
    # If the filter form is submitted, update the sorting values.
    if request.method == "GET" and "sort" in request.GET:
        sort = request.GET["sort"].lower()
        order = request.GET["order"].lower()
        if order == "ascending":
            ascending = True
        elif order == "descending":
            ascending = False

    # Get all the tags
    all_tags = Tags.objects.all()

    # Sort and order the tags based on default values or submitted values
    if sort == "name":
        all_tags = sorted(all_tags, key=sortTagName, reverse=not ascending)
        # all_tags.sort(key=sortTitle)
    elif sort == "popularity":
        all_tags = sorted(all_tags, key=sortPopularity, reverse=not ascending)

    # Prepare the values for outputting to the template
    current_sorting = sort.title()
    if ascending == True:
        current_ordering = "Ascending"
    elif ascending == False:
        current_ordering = "Descending"
    sort_options = ["Name", "Popularity"]
    order_options = ["Ascending", "Descending"]
    # print(all_tags.notes)
    return render(request, "all_tags.html", {"all_tags": all_tags, "current_sorting": current_sorting, "current_ordering": current_ordering, "sort_options": sort_options, "order_options": order_options})

def all_statuses(request, sort="title", ascending=False):
    sort_options = ["Title", "Date Modified (File)"]
    order_options = ["Ascending", "Descending"]
    # If the filter form is submitted, update the sorting values.
    if request.method == "GET" and "sort" in request.GET:
        sort = request.GET["sort"].lower()
        if sort == sort_options[1]:
            sort = "modified"
        order = request.GET["order"].lower()
        if order == "ascending":
            ascending = True
        elif order == "descending":
            ascending = False

    all_notes = normalNotes.objects.all()
    if sort == "title":
        all_notes = sorted(all_notes, key=sortTitle, reverse=not ascending)
    elif sort == "modified":
        all_notes = sorted(all_notes, key=sortDate, reverse=not ascending)

    # Create lists for grouping Items By tags or status if the user requests to group them
    group_list = []
    for file in all_notes:
        if file.status not in group_list:
            group_list.append(file.status)
        
    # The sorting looks wonky on the frontend because some files (specifically files with type: paper) are being displayed with their bibtex title instead of their normal title

    # Prepare the values for outputting to the template
    current_sorting = sort.title()
    if ascending == True:
        current_ordering = "Ascending"
    elif ascending == False:
        current_ordering = "Descending"
    return render(request, "all_statuses.html", {"group_list": group_list, "all_notes": all_notes ,"sort_options": sort_options, "order_options": order_options, "current_sorting": current_sorting , "current_ordering": current_ordering})

def tag(request, tag_name):
    tag = Tags.objects.get(name=tag_name)
    return render(request, "tag.html", {"tag": tag})

def status(request, status_name):
    status_list = normalNotes.objects.filter(status=status_name)
    return render(request, "status.html", {"status": status_name, "status_list": status_list})

def login_view(request):
    if request.method == 'POST':
        passkey = request.POST["pin"]
        username = env("PROJECT_USERNAME")
        email = env("PROJECT_EMAIL")
        user = authenticate(username=username, email=email, password=passkey)
        if user is not None:
            log_user = login(request, user)
            return redirect("home")
        else:
            print("Error")
            pass
    return render(request, "login.html")

def search_results(request, sort="name", group="none", ascending=True):
    if request.method == "GET":
        if "group" in request.GET:
            group = request.GET["group"].lower()
        else:
            group = "none"

        if "sort" in request.GET:
            sort = request.GET["sort"].lower()
        else:
            sort = "name"

        if "search_input" in request.GET:
            search = request.GET["search_input"]
        else:
            search = ""
            group = "folders"
        folder_results = Folder.objects.filter(Q(name__icontains=search))
        file_results = normalNotes.objects.filter(
            Q(name__icontains=search) | Q(title__icontains=search) | Q(main_content__icontains=search) | Q(tags__name__icontains=search) | Q(status__icontains=search)
        ).distinct()
        all_folders = []
        all_types = Type.objects.all()
        if sort == "name":
            if ascending == True:
                file_results = file_results.order_by("title")
                folder_results = folder_results.order_by("name")
            else:
                file_results = file_results.order_by("-title")
                folder_results = folder_results.order_by("-name")
        elif sort == "modified":
            if ascending == True:
                file_results = file_results.order_by("date_modified")
            else:
                file_results = file_results.order_by("-date_modified")

        # Create lists for grouping Items By tags or status if the user requests to group them
        if group == "tags":
            group_list = []
            for file in file_results:
                for tag in file.tags.all():
                    if tag not in group_list:
                        group_list.append(tag)
        elif group == "status":
            group_list = []
            for file in file_results:
                if file.status not in group_list:
                    group_list.append(file.status)
        elif group == "folders":
            group_list = []
            for file in file_results:
                if file.note_type not in group_list:
                    group_list.append(file.note_type)
        else:
            group_list = []

        current_sorting = sort.title()
        current_grouping = group.title()
        if ascending == True:
            current_ordering = "Ascending"
        elif ascending == False:
            current_ordering = "Descending"
        sort_options = ["Name", "Date Modified"]
        group_options = ["None", "Status", "Tags", "Folders"]
        order_options = ["Ascending", "Descending"]
    else:
        search = ""
    return render(request, "search-results.html", {"folder_results": folder_results, "file_results": file_results, "folders": all_folders, "all_types": all_types, "search_term": search, "sort_options": sort_options, "group_options": group_options, "order_options": order_options, "current_sorting": current_sorting, "current_grouping": current_grouping, "current_ordering": current_ordering, "group_list": group_list})