import sys, os

import settings
import project_variables
import re
import django
from django.core.exceptions import ObjectDoesNotExist

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "research_notes.settings")
django.setup()

from notes.models import normalNotes, Tags, Folder, Type

# print("Here's all: ", notes_models.objects.all())

notes_path = settings.BASE_DIR / 'templates/all_notes'
entire_tree = project_variables.fs_tree_to_dict(settings.BASE_DIR / "templates/all_notes")
# print(entire_tree)

folder_regex = re.compile(r'^\w+$')


def isFolder(notes_path=notes_path, parent="", file=""):
    if os.path.isdir(f"{notes_path}/{parent}/{file}") and bool(folder_regex.match(file)):
        return True
    else:
        return False

def create_notes_models(dict, parent="", parent_model=""):
    for k, v in dict.items():
        current_abspath = os.path.abspath(parent)+ "/" + k
        if isFolder(parent=parent, file=k):
            isType = False
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
            parent = parent
            path = f"{parent}/{name}"
            subfolders = []
            subfiles = []
            full_path = f"{notes_path}/{path}"
            for i in os.listdir(full_path):
                file_path = full_path + "/" + i
                if os.path.isdir(file_path):
                    subfolders.append(i)
                elif os.path.isfile(file_path):
                    subfiles.append(i)
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
            parent_list = parent.split('/')
            # print(parent_list)

            # Create Root 'All Notes' folder
            if len(parent_list) == 1 and parent_list[0] == "":
                try:
                    model_parent = Folder.objects.get(name="All Notes")
                except ObjectDoesNotExist:
                    root_subfold = []
                    root_subfile = []
                    for i in os.listdir(notes_path):
                        full_path = f"{notes_path}/{i}"
                        if os.path.isdir(full_path):
                            root_subfold.append(i)
                        elif os.path.isfile(full_path):
                            root_subfile.append(i)
                    model_parent = Folder.objects.create(name="All Notes", path=notes_path, subfolders=root_subfold, subfiles=root_subfile)
            else:
                # Else get the parent folder instance
                model_parent = Folder.objects.get(path=parent)

            # Create type model if a folder type is found (A folder type is one of the folders found in the root directory)
            if isType == True:
                the_type = Type.objects.get_or_create(name = k, subfolders=subfolders, subfiles=subfiles)
                folder = Folder.objects.get_or_create(name=name, folder_type=the_type[0], parent=model_parent, path=path, subfolders=subfolders, subfiles=subfiles)
            
            # Create a normal folder if it isn't a root directory
            else:
                model_type = Type.objects.get(name=type)
                parent_list = path.split('/')
                # print(len(parent_list))
                # print(Type.objects.get(name=parent_list[1]))
                len(parent_list) <= 3
                # if len(parent_list) <= 3 and (Type.objects.get(name=parent_list[1])):
                #     model_parent = False
                # else:
                model_parent = Folder.objects.get(path=parent)
                folder = Folder.objects.get_or_create(name=name, folder_type=model_type, parent=model_parent, path=path, subfolders=subfolders, subfiles=subfiles)
            create_notes_models(v, parent=f"{parent}/{k}", parent_model=folder)
            
            # print(f'{k} is a folder')
        else:
            title = v['title']
            name = k
            tags = v['tags']
            status = v['status']
            type_str = v['type']
            # print(type_str)
            model_type = Type.objects.get(name=type_str)
            # type = v['type']
            path = f"{parent}/{name}"
            print(
                f"""
                    Parent: {parent}
                    Title: {title}
                    Name: {name}
                    Tags: {tags}
                    Status: {status}
                    Type: {type_str}
                    Path: {path}
                """
            )
            note = normalNotes.objects.get_or_create(title=title, name=name, parent_folder=parent_model[0], note_type=model_type, status=status, path=path)
            for tag in tags:
                tag_model = Tags.objects.get_or_create(name=tag)
                note[0].tags.add(tag_model[0])
            note[0].save()
            # print(f'{k} is not a folder')

create_notes_models(entire_tree, parent='')






# def create_notes_models(dict, parent=""):
#     for k, v in dict.items():
#         current_abspath = os.path.abspath(parent)+ "/" + k
#         if isFolder(parent=parent, file=k):

#             # Determine Folder Type
#             folder_type = ""
#             root = f"{notes_path}/{parent}"
#             root_list = root.split("/")
#             folder_index = root_list.index("all_notes") + 1
#             folder_type = root_list[folder_index]
#             if (folder_type == "") and (folder_type != root_list[-1]):
#                 folder_type = root_list[folder_index+1]
#             elif (folder_type == "") and (folder_type == root_list[-1]):
#                 isType = True

#             # Determine the values to be outputted in the database
#             name = k
#             type = folder_type
#             # type = v[list(v.keys())[0]]['type']
#             parent = parent
#             path = f"{parent}/{name}"
#             subfolders = []
#             subfiles = []
#             print(
#                 f"""
#                     Name: {name}
#                     Folder Type: {type}
#                     Parent: {parent}
#                     Path: {path}
#                     Subfolders: {subfolders}
#                     Subfiles: {subfiles}
#                 """
#             )
#             create_notes_models(v, parent=f"{parent}/{k}")
#             # print(f'{k} is a folder')
#         else:
#             # print(os.path.isdir(f"{notes_path}/{parent}/{k}"))
#             # print(f"{notes_path}/{k}")
#             title = v['title']
#             name = k
#             tags = v['tags']
#             status = v['status']
#             type = v['type']
#             path = f"{parent}/{name}"
#             print(
#                 f"""
#                     Parent: {parent}
#                     Title: {title}
#                     Name: {name}
#                     Tags: {tags}
#                     Status: {status}
#                     Type: {type}
#                     Path: {path}
#                 """
#             )
#             # notes_models.objects.create()
#             # print(f'{k} is not a folder')