from django.db import models
from django.utils.text import slugify

# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "tag"

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)
    subfolders = models.JSONField() # The name of the Folder model instance will be included in the list will be in a list
    subfiles = models.JSONField() # The name of the subfiles will be in a list

    def __str__(self):
        return self.name

class Citations(models.Model):
    title = models.CharField(max_length=350)
    author = models.JSONField() # List of authors
    year = models.DateField()
    journal = models.CharField(max_length=250)
    volume = models.IntegerField()
    number = models.IntegerField()
    publisher = models.JSONField() # List of publishers
    pages = models.CharField(max_length=100)
    abstract = models.TextField()
    langid = models.CharField(max_length=100, blank=True)
    annotations = models.JSONField()
    issn = models.JSONField()
    doi = models.JSONField()
    keywords = models.JSONField()
    file = models.JSONField()

    class Meta:
        verbose_name = "citation"

    def __str__(self):
        return self.title

class Folder(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(auto_created=True)
    folder_type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey("self", default="", on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(max_length=500)
    subfolders = models.JSONField() # The name of the Folder model instance will be included in the list will be in a list
    subfiles = models.JSONField() # The name of the subfiles will be in a list

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super(Folder, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "folder"

    def __str__(self):
        return self.name

    def get_all_subdirs(self):
        return self.subfolders + self.subfiles
    

    # Make functions for returning all files and all folders under it

class normalNotes(models.Model):
    name = models.CharField(max_length=250)
    note_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    path = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    slug = models.SlugField(default="", max_length=600)
    status = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tags)
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    main_content = models.TextField()

    def generate_slug():
        pass

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super(normalNotes, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "note"

    def __str__(self):
        return self.name

class Papers(models.Model):
    note = models.OneToOneField(normalNotes, on_delete=models.CASCADE, primary_key=True, related_name="papers")
    year = models.DateField()
    link = models.URLField()
    bibtex = models.ForeignKey(Citations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "paper"

    def __str__(self):
        return self.note.name
