import sys, os

import settings
import project_variables
import re
import django 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "research_notes.settings")
django.setup()

from notes.models import normalNotes as notes_models

print("Here's all: ", notes_models.objects.all())

notes_path = settings.BASE_DIR / 'templates/all_notes'
entire_tree = project_variables.fs_tree_to_dict(settings.BASE_DIR / "templates/all_notes")
# print(entire_tree)

folder_regex = re.compile(r'^\w+$')


def isFolder(notes_path=notes_path, parent="", file=""):
    # print(os.path.isdir(f"{notes_path}/{parent}/{file}"))
    # print(f"{notes_path}/{parent}/{file}")
    if os.path.isdir(f"{notes_path}/{parent}/{file}") and bool(folder_regex.match(file)):
        return True
    else:
        return False

def create_notes_models(dict, parent=""):
    for k, v in dict.items():
        current_abspath = os.path.abspath(parent)+ "/" + k
        if isFolder(parent=parent, file=k):

            # Determine Folder Type
            folder_type = ""
            root = f"{notes_path}/{parent}"
            root_list = root.split("/")
            folder_index = root_list.index("all_notes") + 1
            folder_type = root_list[folder_index]
            if (folder_type == "") and (folder_type != root_list[-1]):
                folder_type = root_list[folder_index+1]
            elif (folder_type == "") and (folder_type == root_list[-1]):
                isType = True

            # Determine the values to be outputted in the database
            name = k
            type = folder_type
            # type = v[list(v.keys())[0]]['type']
            parent = parent
            path = f"{parent}/{name}"
            subfolders = []
            subfiles = []
            print(
                f"""
                    Name: {name}
                    Folder Type: {type}
                    Parent: {parent}
                    Path: {path}
                    Subfolders: {subfolders}
                    Subfiles: {subfiles}
                """
            )
            create_notes_models(v, parent=f"{parent}/{k}")
            # print(f'{k} is a folder')
        else:
            # print(os.path.isdir(f"{notes_path}/{parent}/{k}"))
            # print(f"{notes_path}/{k}")
            title = v['title']
            name = k
            tags = v['tags']
            status = v['status']
            type = v['type']
            path = f"{parent}/{name}"
            print(
                f"""
                    Parent: {parent}
                    Title: {title}
                    Name: {name}
                    Tags: {tags}
                    Status: {status}
                    Type: {type}
                    Path: {path}
                """
            )
            # notes_models.objects.create()
            # print(f'{k} is not a folder')

create_notes_models(entire_tree, parent='')
