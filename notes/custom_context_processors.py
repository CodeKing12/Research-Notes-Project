from .models import Folder
import os
from django.core.exceptions import ObjectDoesNotExist

def tree_nav(request):
    try:
        root_parent = Folder.objects.get(name="All Notes")
    except ObjectDoesNotExist:
        os.system("python research_notes/seed_database.py")
        root_parent = Folder.objects.get(name="All Notes")
    nav_html = root_parent.get_folder_tree()
    # nav_html = ""
    return {"full_nav": nav_html}