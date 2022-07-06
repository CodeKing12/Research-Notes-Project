from django.contrib import admin
from . import models as notes_models

# Register your models here.
class CitationsAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'year', 'month', 'keywords']

class TagsAdmin(admin.ModelAdmin):
    list_display = ['name']

class normalNotesAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'note_type', 'path', 'parent_folder', 'slug']

class PapersAdmin(admin.ModelAdmin):
    list_display = ['note', 'year', 'bibtex', 'link']

class FolderAdmin(admin.ModelAdmin):
    list_display = ['name', 'folder_type', 'path', 'slug']

class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'subfolders', 'subfiles']


admin.site.register(notes_models.Citations, CitationsAdmin)
admin.site.register(notes_models.Tags, TagsAdmin)
admin.site.register(notes_models.normalNotes, normalNotesAdmin)
admin.site.register(notes_models.Papers, PapersAdmin)
admin.site.register(notes_models.Folder, FolderAdmin)
admin.site.register(notes_models.Type, TypeAdmin)