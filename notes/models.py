# from __future__ import annotations
# from tkinter.messagebox import YES
# from xmlrpc.server import DocCGIXMLRPCRequestHandler
# from django.db import models

# # Create your models here.
# class Tags(models.Model):
#     name = models.CharField(max_length=150)

# class Type(models.Model):
#     name = models.CharField(max_length=100)
#     subfolders = [] # The name of the Folder model instance will be included in the list will be in a list
#     subfiles = [] # The name of the subfiles will be in a list

# class Citations(models.Model):
#     title = models.CharField(max_length=350)
#     author = []
#     year = models.DateField()
#     journal = models.CharField(max_length=250)
#     volume = models.IntegerField()
#     number = models.IntegerField()
#     publisher = []
#     pages = models.Range
#     abstract = models.TextField()
#     langid = models.CharField(max_length=100, blank=True)
#     # annotations
#     # issn
#     # doi
#     # keywords
#     # file

# class Folder(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(auto_created=True)
#     folder_type = models.ForeignKey(Type, on_delete=models.CASCADE)
#     parent = models.ManyToManyField(Type)
#     subfolders = [] # The name of the Folder model instance will be included in the list will be in a list
#     subfiles = [] # The name of the subfiles will be in a list

#     # Make functions for returning all files and all folders under it

# class normalNotes(models.Model):
#     name = models.CharField(max_length=250)
#     folder_type = models.ForeignKey(Type, on_delete=models.CASCADE)
#     title = models.CharField(max_length=500)
#     slug = models.SlugField(auto_created=True)
#     status = models.CharField(max_length=200)
#     tags = models.ManyToManyField(Tags)
#     parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
#     main_content = models.TextField()

#     def generate_slug():
#         pass

#     def save(self, *args, **kwargs):
#         super(normalNotes, self).save(*args, **kwargs)

# class Papers(models.Model):
#     note = models.OneToOneField(normalNotes, on_delete=models.CASCADE, primary_key=True, related_name="papers")
#     year = models.DateField()
#     link = models.URLField()
#     bibtex = models.ForeignKey(Citations, on_delete=models.CASCADE)
