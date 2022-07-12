from .models import Folder
from research_notes.project_variables import iterdict

def tree_nav(request):
    root_parent = Folder.objects.get(name="All Notes")
    nav_html = root_parent.get_folder_tree()
    # nav_html = ""
    return {"full_nav": nav_html}