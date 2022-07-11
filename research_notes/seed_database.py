import sys, os, markdown, bibtexparser, settings, re, django
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter.index import front_matter_plugin
from mdit_py_plugins.footnote.index import footnote_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from mdit_py_plugins.anchors.index import anchors_plugin
from mdit_py_plugins.dollarmath.index import dollarmath_plugin
from mdit_py_plugins.texmath.index import texmath_plugin
from mdit_py_plugins.amsmath import amsmath_plugin
from github import Github
import frontmatter

import environ
env = environ.Env()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "research_notes.settings")
django.setup()

from django.contrib.auth.models import User
from notes.models import Citations, Papers, normalNotes, Tags, Folder, Type
import project_variables

def create_notes_user():
    email = env("PROJECT_EMAIL")
    username = env("PROJECT_USERNAME")
    pin = env("PROJECT_PASSWORD")

    user = User.objects.get_or_create(email=email, username=username)
    user[0].set_password(pin)
    user[0].save()


# print("Here's all: ", notes_models.objects.all())

notes_path = settings.BASE_DIR / 'templates/all_notes'
# entire_tree = project_variables.fs_tree_to_dict(notes_path)
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
            folder_dict = v
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
                    model_parent = Folder.objects.create(name="All Notes", path=notes_path, subfolders=root_subfold, subfiles=root_subfile, folder_dict=dict)
            else:
                # Else get the parent folder instance
                model_parent = Folder.objects.get(path=parent)

            # Create type model if a folder type is found (A folder type is one of the folders found in the root directory)
            if isType == True:
                the_type = Type.objects.get_or_create(name = k, subfolders=subfolders, subfiles=subfiles)
                folder = Folder.objects.get_or_create(name=name, folder_type=the_type[0], parent=model_parent, path=path, subfolders=subfolders, subfiles=subfiles, folder_dict=folder_dict)
            
            # Create a normal folder if it isn't a root directory
            else:
                model_type = Type.objects.get(name=type)
                parent_list = path.split('/')
                len(parent_list) <= 3
                model_parent = Folder.objects.get(path=parent)
                folder = Folder.objects.get_or_create(name=name, folder_type=model_type, parent=model_parent, path=path, subfolders=subfolders, subfiles=subfiles, folder_dict=folder_dict)
            create_notes_models(v, parent=f"{parent}/{k}", parent_model=folder)
            
            # print(f'{k} is a folder')
        else:
            if k.endswith(".md"):
                # Extravt all the values from the dictionary
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
                abs_path_to_file = f"{notes_path}/{path}"
                with open(abs_path_to_file, "r", encoding="utf-8") as f:
                    content = f.read()
                date_created = os.path.getctime(abs_path_to_file)
                date_modified = os.path.getmtime(abs_path_to_file)
                time_created = datetime.fromtimestamp(date_created)
                time_modified = datetime.fromtimestamp(date_modified)
                md = (
                    MarkdownIt("gfm-like")
                    .use(front_matter_plugin)
                    .use(footnote_plugin)
                    # .use(dollarmath_plugin)
                    # .use(texmath_plugin)
                    .use(anchors_plugin)
                    .use(tasklists_plugin)
                    .use(amsmath_plugin)
                    .disable('image')
                )
                file_content = md.render(content)
                bib_text = r"\\ref{\w*}"
                bib_re = re.compile(bib_text)
                count = 0
                if bool(bib_re.findall(file_content)):
                    file_content += "\n<h1 id='references'>References</h1><ul class='ordered-list reference-list'>"
                    for item in bib_re.finditer(file_content):
                        text = item.group().strip("\\ref{")
                        text = text.strip("}")
                        count += 1
                        ref_obj = Citations.objects.get(name=text)
                        author_list = ref_obj.author.split(", ")
                        if len(author_list) > 3:
                            authors = f"{author_list[0]} et all."
                        else:
                            authors = ref_obj.author
                        ref_html = f"<a class='blue ref-link' id='ref-{count}' href='#reference-{count}'>{authors} ({ref_obj.year})</a>"
                        file_content = file_content.replace(item.group(), ref_html)
                        file_content += f"<li><h6 id='a-reference'><a id='reference-{count}' href='#ref-{count}'>{ref_obj.author} ({ref_obj.year}). {ref_obj.title}. {ref_obj.journal}, {ref_obj.volume}({ref_obj.number}), {ref_obj.pages}. <a href='https://doi.org/{ref_obj.doi}'>{ref_obj.doi}</a></a></h6></li>"
                        # print("{{ tito {}".strip("{"))
                    file_content += "</ul>"

                file_content = file_content.replace('<table>', "<table class='table table-striped'>")

                content_lines = content.split("\n")
                # print(file_content)
                # Create a notes object once all the values have been extracted
                note = normalNotes.objects.update_or_create(title=title, name=name, parent_folder=parent_model[0], note_type=model_type, status=status, path=path, main_content=file_content, date_created=time_created, date_modified=time_modified)

                # Create the tags if they are not available and add them to the note object
                for tag in tags:
                    tag_model = Tags.objects.get_or_create(name=tag)
                    note[0].tags.add(tag_model[0])
                note[0].save()

                if type_str == 'papers':
                    year = v['year']
                    link = v['link']
                    bibtex_ref = v['bibtex_ref']
                    bibtex = Citations.objects.get(name=bibtex_ref)
                    paper = Papers.objects.update_or_create(note=note[0], year=year, link=link, bibtex=bibtex)
                # print(f'{k} is not a folder')
            else:
                continue


tree, citations_list = project_variables.fs_tree_to_dict(path_=notes_path, citations=[])
def generate_citations_model_fields(citations_list):
    for cite in citations_list:
        file = f"{cite[0]}/{cite[1]}"
        with open(file, "r") as citation_file:
            bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse_file(citation_file)
        citations = bib_database.entries_dict
    for article in citations:
        name = article
        citation = citations[article]
        try:
            title = citation['title']
        except KeyError:
            title = ""

        try:
            shorttitle = citation['shorttitle']
        except KeyError:
            shorttitle = ""

        try:
            author = citation['author']
        except KeyError:
            author = ""

        try:
            year = citation['year']
        except KeyError:
            year = ""

        try:
            month = citation['month']
        except KeyError:
            month = ""

        try:
            journal = citation['journal']
        except KeyError:
            journal = ""

        try:
            volume = citation['volume']
        except KeyError:
            volume = 0

        try:
            number = citation['number']
        except KeyError:
            number = 0

        try:
            pages = citation['pages']
        except KeyError:
            pages = ""

        try:
            issn = citation['issn']
        except KeyError:
            issn = ""

        try:
            abstract = citation['abstract']
        except KeyError:
            abstract = ""

        try:
            langid = citation['langid']
        except KeyError:
            langid = ""

        try:
            keywords = citation['keywords']
        except KeyError:
            keywords = ""

        try:
            cite_file = citation['file']
        except KeyError:
            cite_file = ""

        try:
            doi = citation['doi']
        except KeyError:
            doi = ""

        try:
            annotation = citation['annotation']
        except KeyError:
            annotation = ""
        
        try:
            publisher = citation['publisher']
        except KeyError:
            publisher = ""


        citation = Citations.objects.get_or_create(
            name = name,
            title = title, 
            shorttitle = shorttitle, 
            author = author, 
            year = year, 
            month = month, 
            journal = journal, 
            volume = volume, 
            number = number, 
            publisher = publisher,
            pages = pages, 
            issn = issn, 
            doi = doi,
            abstract = abstract, 
            langid = langid, 
            keywords = keywords, 
            file = cite_file, 
            annotations = annotation
        )
        print(citation)

def identify_headers(lines):
    headers = []
    re_hashtag_headers = r"^#+\ .*$"
    re_alternative_header_lvl1 = r"^=+ *$"
    re_alternative_header_lvl2 = r"^-+ *$"

    for i, line in enumerate(lines):
        # identify headers by leading hashtags
        if re.search(re_hashtag_headers, line):
            headers.append([line, i])
            
    return headers


# generate_citations_model_fields(citations_list)
# create_notes_models(entire_tree, parent='')
# create_notes_user()
# There's no need to define $$ when using any /begin{} attribute

g = Github("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")
user = g.get_user()
folder_regex = re.compile(r'^\w+$')
research_repo = []
research_repo = user.get_repo("Research-Notes-Test")
contents = research_repo.get_contents("")


def repo_to_dict(contents, file_dict={}):
    # repo_tree = research_repo.get_git_tree("d0cb2aa1f16cd244488033d561ecef5e5b6c69eb", recursive=True).raw_data["tree"]
    # print(repo_tree)
    for content in contents:
        if content.type == "dir":
            dir_contents = research_repo.get_contents(content.path)
            content_dict = {}
            parsed_contents = repo_to_dict(contents=dir_contents, file_dict={})
            for cont in dir_contents:
                if cont.type == "file":
                    content_dict[cont.name] = cont
                elif cont.type == "dir":
                    fold_cont = repo_to_dict(research_repo.get_contents(cont.path), file_dict={})
                    content_dict[cont] = fold_cont
            file_dict[content] = content_dict
        else:
            # if content.name.endswith(".md"):
            #     path_list = content.path.split("/")
            #     if len(path_list) > 1:
            #         note_type = path_list[0]
            #     else:
            #         note_type="root"
            #     cont = content.decoded_content
            #     note = frontmatter.loads(cont)
            #     file_token = note.metadata
            #     file_token.update({"type": note_type})
            #     file_dict[content.name] = file_token
            # else:
            file_dict[content.name] = content
    return file_dict
    
tree = repo_to_dict(contents, file_dict={})
print(tree)
print("-------------------------------------------------------------------")


def create_notes_models_from_github(the_dict, parent="", parent_model=""):
    for k, v in the_dict.items():
        if type(v) == dict and k.type == "dir":
            print("Encounter Dir")
            subfiles = []
            subfolders = []
            for file in research_repo.get_contents(k.path):
                if file.type == "dir":
                    subfolders.append(file.name)
                elif file.type == "file":
                    subfiles.append(file.name)
            name = k.name
            path_list = k.path.split("/")

            path = k.path
            parent = parent
            if parent == "":
                root_subfold = []
                root_subfiles = []
                root_path = "/"
                for file in contents:
                    if file.type == "dir":
                        root_subfold.append(file.name)
                    elif file.type == "file":
                        root_subfiles.append(file.name)
                model_parent = Folder.objects.get_or_create(name="All Notes", path=root_path, subfolders=root_subfold, subfiles=root_subfiles)
                model_parent = model_parent[0]
            else:
                model_parent = Folder.objects.get(path=parent)
            if len(path_list) > 1:
                folder_type = path_list[0]
                model_type = Type.objects.get(name=folder_type)
                parent_list = path.split('/')
                len(parent_list) <= 3
                folder = Folder.objects.get_or_create(name=name, folder_type=model_type, parent=model_parent, path=path, subfolders=subfolders, subfiles=subfiles)
            else:
                folder_type="root"
                the_type = Type.objects.get_or_create(name = name, subfolders=subfolders, subfiles=subfiles)
                folder = Folder.objects.get_or_create(name=name, folder_type=the_type[0], parent=model_parent, path=path, subfolders=subfolders, subfiles=subfiles)
            print(
                f"""
                    Name: {name}
                    Folder Type: {folder_type}
                    Parent: {parent}
                    Path: {path}
                    Subfolders: {subfolders}
                    Subfiles: {subfiles}
                """
            )
            create_notes_models_from_github(v, parent=path, parent_model=folder)

            # print(f'{k} is a folder')
        else:
            print("Encountered File")
            print(k,v)
            exclude_list = ["README.md", "index.md"]
            if k.endswith(".md") and v.name not in exclude_list:
                path_list = v.path.split("/")
                if len(path_list) > 1:
                    note_type = path_list[0]
                else:
                    note_type="root"
                name = v.name
                md_content = v.decoded_content
                md_content = str(md_content, encoding="utf-8")
                note = frontmatter.loads(md_content)
                file_token = note.metadata
            #     # Extract all the values from the dictionary
                print(file_token)
                title = file_token['title']
                tags = file_token['tags']
                status = file_token['status']
                model_type = Type.objects.get(name=note_type)
                date_modified = v.last_modified
                path = v.path
                print(
                    f"""
                        Parent: {parent}
                        Title: {title}
                        Name: {name}
                        Tags: {tags}
                        Status: {status}
                        Type: {note_type}
                        Path: {path}
                    """
                )
                md = (
                    MarkdownIt("gfm-like")
                    .use(front_matter_plugin)
                    .use(footnote_plugin)
                    # .use(dollarmath_plugin)
                    # .use(texmath_plugin)
                    .use(anchors_plugin)
                    .use(tasklists_plugin)
                    .use(amsmath_plugin)
                    .disable('image')
                )
                file_content = md.render(md_content)
                bib_text = r"\\ref{\w*}"
                bib_re = re.compile(bib_text)
                count = 0
                if bool(bib_re.findall(file_content)):
                    file_content += "\n<h1 id='references'>References</h1><ul class='ordered-list reference-list'>"
                    for item in bib_re.finditer(file_content):
                        text = item.group().strip("\\ref{")
                        text = text.strip("}")
                        count += 1
                        ref_obj = Citations.objects.get(name=text)
                        author_list = ref_obj.author.split(", ")
                        if len(author_list) > 3:
                            authors = f"{author_list[0]} et all."
                        else:
                            authors = ref_obj.author
                        ref_html = f"<a class='blue ref-link' id='ref-{count}' href='#reference-{count}'>{authors} ({ref_obj.year})</a>"
                        file_content = file_content.replace(item.group(), ref_html)
                        file_content += f"<li><h6 id='a-reference'><a id='reference-{count}' href='#ref-{count}'>{ref_obj.author} ({ref_obj.year}). {ref_obj.title}. {ref_obj.journal}, {ref_obj.volume}({ref_obj.number}), {ref_obj.pages}. <a href='https://doi.org/{ref_obj.doi}'>{ref_obj.doi}</a></a></h6></li>"
                        # print("{{ tito {}".strip("{"))
                    file_content += "</ul>"

                file_content = file_content.replace('<table>', "<table class='table table-striped'>")

            #     content_lines = content.split("\n")
            #     # print(file_content)
            #     # Create a notes object once all the values have been extracted
                note = normalNotes.objects.update_or_create(title=title, name=name, parent_folder=parent_model[0], note_type=model_type, status=status, path=path, main_content=file_content, date_modified=date_modified)

            # Create the tags if they are not available and add them to the note object
                # print("Breaks Here")
                for tag in tags:
                    try:
                        tag_model = Tags.objects.get(name=tag)
                    except ObjectDoesNotExist:
                        tag_model = Tags.objects.create(name=tag)
                    note[0].tags.add(tag_model)
                note[0].save()

                if note_type == 'papers':
                    year = file_token['year']
                    link = file_token['link']
                    bibtex_ref = file_token['bibtex_ref']
                    print(year, link, bibtex_ref)
                    # bibtex = Citations.objects.get(name=bibtex_ref)
                    # paper = Papers.objects.update_or_create(note=note[0], year=year, link=link, bibtex=bibtex)
            #     # print(f'{k} is not a folder')
            elif k.endswith(".bib") and v.name not in exclude_list:
                bib_content = v.decoded_content
                bib_content = str(bib_content, encoding="utf-8")
                bib_database = bibtexparser.bparser.BibTexParser(common_strings=True).parse(bib_content)
                citations = bib_database.entries_dict
                for article in citations:
                    name = article
                    citation = citations[article]
                    try:
                        title = citation['title']
                    except KeyError:
                        title = ""

                    try:
                        shorttitle = citation['shorttitle']
                    except KeyError:
                        shorttitle = ""

                    try:
                        author = citation['author']
                    except KeyError:
                        author = ""

                    try:
                        year = citation['year']
                    except KeyError:
                        year = ""

                    try:
                        month = citation['month']
                    except KeyError:
                        month = ""

                    try:
                        journal = citation['journal']
                    except KeyError:
                        journal = ""

                    try:
                        volume = citation['volume']
                    except KeyError:
                        volume = 0

                    try:
                        number = citation['number']
                    except KeyError:
                        number = 0

                    try:
                        pages = citation['pages']
                    except KeyError:
                        pages = ""

                    try:
                        issn = citation['issn']
                    except KeyError:
                        issn = ""

                    try:
                        abstract = citation['abstract']
                    except KeyError:
                        abstract = ""

                    try:
                        langid = citation['langid']
                    except KeyError:
                        langid = ""

                    try:
                        keywords = citation['keywords']
                    except KeyError:
                        keywords = ""

                    try:
                        cite_file = citation['file']
                    except KeyError:
                        cite_file = ""

                    try:
                        doi = citation['doi']
                    except KeyError:
                        doi = ""

                    try:
                        annotation = citation['annotation']
                    except KeyError:
                        annotation = ""
                    
                    try:
                        publisher = citation['publisher']
                    except KeyError:
                        publisher = ""


                    citation = Citations.objects.get_or_create(
                        name = name,
                        title = title, 
                        shorttitle = shorttitle, 
                        author = author, 
                        year = year, 
                        month = month, 
                        journal = journal, 
                        volume = volume, 
                        number = number, 
                        publisher = publisher,
                        pages = pages, 
                        issn = issn, 
                        doi = doi,
                        abstract = abstract, 
                        langid = langid, 
                        keywords = keywords, 
                        file = cite_file, 
                        annotations = annotation
                    )
                    print(citation)
            else:
                continue

create_notes_models_from_github(tree)