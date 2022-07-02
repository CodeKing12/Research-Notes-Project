from django.contrib import admin
from . import models as notes_models

# Register your models here.
class CitationsAdmin(admin.ModelAdmin):
    pass

class CitationsAdmin(admin.ModelAdmin):
    pass

class TagsAdmin(admin.ModelAdmin):
    pass

class normalNotesAdmin(admin.ModelAdmin):
    pass

class PapersAdmin(admin.ModelAdmin):
    pass

class FolderAdmin(admin.ModelAdmin):
    pass

class TypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(notes_models.Citations, CitationsAdmin)
admin.site.register(notes_models.Tags, TagsAdmin)
admin.site.register(notes_models.normalNotes, normalNotesAdmin)
admin.site.register(notes_models.Papers, PapersAdmin)
admin.site.register(notes_models.Folder, FolderAdmin)
admin.site.register(notes_models.Type, TypeAdmin)