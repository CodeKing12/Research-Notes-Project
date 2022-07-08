from .models import Folder
from research_notes.project_variables import iterdict

def tree_nav(request):
    root_parent = Folder.objects.get(name="All Notes")
    full_path = root_parent.path
    tree_dict = root_parent.folder_dict
    nav_html = iterdict(d=tree_dict, level=-1, parent=full_path)

    return {"full_nav": nav_html}