from logging import root
import os, frontmatter
import re
from research_notes import settings

root_path = os.path.abspath(".")

def fs_tree_to_dict(path_):
    file_token = []
    for root, dirs, files in os.walk(path_):
        if "papers" in root:
            file_token = "Something Else"
        if ".git" in dirs:
            dirs.remove(".git")
        tree = {d: fs_tree_to_dict(os.path.join(root, d)) for d in dirs}
        # tree.update({f: file_token for f in files})
        for f in files:
            file_exclude = [".DS_Store", "new.py", "README.md", "index.md", "citations.bib"]
            if f not in file_exclude:
                root_list = root.split("/")
                note_index = root_list.index("all_notes") + 1
                note_type = root_list[note_index]
                note = frontmatter.load(os.path.join(root, f))
                file_token = note.metadata
                file_token.update({"type": note_type})
                tree.update({f: file_token})
        return tree  # note we discontinue iteration trough os.walk

# tree_dict = fs_tree_to_dict(".")

# def iterdict(d, level, parent):
#     level += 1
#     for k,v in d.items():
#         indent = ' ' * 4 * (level)
#         subindent = ' ' * 4 * (level + 1)
#         current_abspath = os.path.abspath(parent)+ "/" + k
#         if os.path.isdir(os.path.abspath(parent)+ '/' + k) and isinstance(v, dict):
#             print(f"{indent}k{level} : v{level}")
#             iterdict(v, level, current_abspath)
#         else:
#             print(f"{indent} {v['title']} : {v['status']}")

# iterdict(tree_dict['classes'], -1, "classes")

# def iterdict(d, level, parent, html=""):
#     level += 1
#     for k,v in d.items():
#         indent = ' ' * 4 * (level)
#         current_abspath = os.path.abspath(parent)+ "/" + k
#         if os.path.isdir(os.path.abspath(parent)+ '/' + k) and isinstance(v, dict):
#             html += f"<li class='nav-item subfolder'><a href='#' class='nav-link'><img class=\"flat-icon\" src=\"/static/img/side-nav/folder.png\" alt='folder'>{k.replace('_', ' ').title()}</a><span class='icon'><i class='arrow_carrot-down'></i></span><ul class='list-unstyled dropdown_nav'>"
#             # html += f"<li class='nav-item'><a href='#' class='nav-link'><img class=\"flat-icon\" src=\"{{% static 'img/side-nav/folder.png' %}}\" alt='folder'>{k.replace('_', ' ').title()}</a><span class='icon'><i class='arrow_carrot-down'></i></span><ul class='list-unstyled dropdown_nav'>"
#             html += iterdict(v, level, current_abspath, html)
#         else:
#             append_html = f"<li class=\"file-link\"><a href='tab.html'><img class=\"file-icon\" src=\"/static/img/side-nav/file.png\" alt='folder'>{v['title']}</a></li>"
#             # append_html = f"<li class=\"file-link\"><a href='tab.html'><img class=\"file-icon\" src=\"{{% static 'img/side-nav/file.png' %}}\" alt='file'>{v['title']}</a></li>"
#             html += append_html
#     html += "</ul></li>"
#     return html


# Working Iterdict for Files and Folders
# def iterdict(d, level, parent):
#     level += 1
#     for k,v in d.items():
#         # print(os.path.join(root_path, parent))
#         indent = ' ' * 4 * (level)
#         subindent = ' ' * 4 * (level + 1)
#         current_abspath = os.path.abspath(parent)+ "/" + k
#         # print(current_abspath)
#         # print(f"{indent}{os.path.isdir(os.path.abspath(parent)+ '/' + k)}")
#         if os.path.isdir(os.path.abspath(parent)+ '/' + k) and isinstance(v, dict):
#             print(f"""
#             {indent}<li class='nav-item'>
#                 <a href='#' class='nav-link'>
#                     <img class=\"flat-icon\" src=\"{{% static 'img/side-nav/folder.png' %}}\" alt='folder'>
#                     {k.replace('_', ' ').title()}
#                 </a>
#                 <span class='icon'><i class='arrow_carrot-down'></i></span>
#                 <ul class='list-unstyled dropdown_nav'>""")
#             iterdict(v, level, current_abspath)
#         else:
#             print(f"""
#                 {indent}<li class=\"file-link\">
#                         <a href='tab.html'>
#                             <img class=\"file-icon\" src=\"img/side-nav/file.png\" alt='folder'>
#                             {v['title']}
#                         </a>
#                     </li>""")
#     print("""
#                 </ul>
#             </li>
#     """)


# Current Iterdict
def iterdict(d, level, parent, html=""):
    level += 1
    for k,v in d.items():
        # print(os.path.join(root_path, parent))
        indent = ' ' * 4 * (level)
        subindent = ' ' * 4 * (level + 1)
        current_abspath = os.path.abspath(parent)+ "/" + k
        # print(current_abspath)
        # print(f"{indent}{os.path.isdir(os.path.abspath(parent)+ '/' + k)}")
        if os.path.isdir(os.path.abspath(parent)+ '/' + k) and isinstance(v, dict):
            html += f"""
            {indent}<li class='nav-item subfolder'>
                <a href='#' class='nav-link'>
                    <img class=\"flat-icon\" src=\"{settings.STATIC_URL}img/side-nav/folder.png\" alt='folder'>
                    {k.replace('_', ' ').title()}
                </a>
                <span class='icon'><i class='arrow_carrot-down'></i></span>
                <ul class='list-unstyled dropdown_nav'>"""
            html += iterdict(v, level, current_abspath)
            html += """
                </ul>
            </li>
            """
        else:
            html += f"""
                {indent}<li class=\"file-link\">
                        <a href='tab.html'>
                            <img class=\"file-icon\" src=\"{settings.STATIC_URL}img/side-nav/file.png\" alt='folder'>
                            {v['title']}
                        </a>
                    </li>"""
    return html