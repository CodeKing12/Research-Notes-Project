from .models import Folder
import os

def tree_nav(request):
    try:
        root_parent = Folder.objects.get(name="All Notes")
        nav_html = root_parent.get_folder_tree()
    except:
        os.system("python research_notes/seed_database.py")
    # nav_html = ""
    return {"full_nav": nav_html}