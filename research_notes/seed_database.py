import sys, os
# sys.path.append('/path/to/your/django/app')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings

import settings
import project_variables

entire_tree = project_variables.fs_tree_to_dict(settings.BASE_DIR / "templates/all_notes")
# print(entire_tree)

