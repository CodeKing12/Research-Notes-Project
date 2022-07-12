from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from research_notes import settings

# Create your models here.
class Tags(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        self.name = self.name.title()
        super(Tags, self).save(*args, **kwargs)

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
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=700)
    shorttitle = models.CharField(max_length=350)
    author = models.JSONField() # List of authors
    year = models.CharField(max_length=50)
    month = models.CharField(max_length=50)
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
    slug = models.SlugField(auto_created=True, blank=True)
    folder_type = models.ForeignKey(Type, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey("self", default="", on_delete=models.CASCADE, null=True, blank=True)
    path = models.CharField(max_length=500)
    folder_dict = models.JSONField(blank=True, null=True)
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

    def presentable_name(self):
        return self.name.replace('_', ' ').title()

    def get_all_subdirs(self):
        return self.subfolders + self.subfiles

    def file_count(self):
        return len(self.subfiles)

    def subfolder_count(self):
        return len(self.subfolders)

    def get_url_path(self):
        if self.parent == None:
            url = "/"
        else:
            parent_path = self.parent.path.strip("/")
            slug = self.slug
            url = f"{parent_path}/{slug}"
            if self.parent == Folder.objects.get(name="All Notes") and self.parent.folder_type == None:
                url = slug
        return url
    
    def get_breadcrumb_html(self):
        html = "<ol class=\"breadcrumb\"><li class='breadcrumb-item'><a href='/'>Home</a></li>"
        path_list = self.get_url_path().split("/")
        current_item = len(path_list) - 1
        # print(path_list)
        for item in path_list:
            path_index = path_list.index(item)
            # print(item, path_index)
            if path_index == 0:
                path = path_list[0]
            else:
                path = "/".join(path_list[:path_index])
            # print(path)
            url = reverse("show-content", args=[path])
            if path_index == current_item:
                path_html = f"<li class='breadcrumb-item active' aria-current='page'><a href='{url}'>{item.replace('_', ' ').title()}</a></li>"
            else:
                path_html = f"<li class='breadcrumb-item'><a href='{url}'>{item.replace('_', ' ').title()}</a></li>"
            html += path_html
        html += "</ol>"
        return html

    def get_folder_tree(self):
        exclude_list = ["README.md", "citations.bib", "index.md"]
        def iterdict(model, level, html=""):
            all_items = model.get_all_subdirs()
            level += 1
            for item in all_items:
                try:
                    folder = Folder.objects.get(name=item, parent=model)
                    isFolder = True
                except ObjectDoesNotExist:
                    if item.endswith(".md") and item not in exclude_list:
                        file = normalNotes.objects.get(name=item, parent_folder=model)
                        isFolder = False
                    else:
                        isFolder = None
                
                indent = ' ' * 4 * (level)
                subindent = ' ' * 4 * (level + 1)
                if isFolder == True:
                    # print("We have a folder")
                    url = reverse('show-content', args=[folder.get_url_path()])
                    html += f"""
                    {indent}<li class='nav-item subfolder'>
                        <a href='{url}' class='nav-link'>
                            <img class=\"flat-icon\" src=\"{settings.STATIC_URL}img/side-nav/folder.png\" alt='folder'>
                            {folder.presentable_name()}
                        </a>
                        <span class='icon'><i class='arrow_carrot-down'></i></span>
                        <ul class='list-unstyled dropdown_nav'>"""
                    html += iterdict(folder, level)
                    html += """
                        </ul>
                    </li>
                    """
                elif isFolder == False:
                    # print("We have a file")
                    url = reverse('show-content', args=[file.get_url_path()])
                    title = file.title
                    html += f"""
                        {indent}<li class=\"file-link\">
                                <a href="{url}">
                                    <img class=\"file-icon\" src=\"{settings.STATIC_URL}img/side-nav/file.png\" alt='folder'>
                                    {title}
                                </a>
                            </li>"""
            return html
        return iterdict(model=self, level=-1)

    # Make functions for returning all files and all folders under it

class normalNotes(models.Model):
    name = models.CharField(max_length=250)
    note_type = models.ForeignKey(Type, on_delete=models.CASCADE)
    path = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    slug = models.SlugField(default="", max_length=600)
    status = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tags, related_query_name="notes", related_name="note")
    parent_folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    # date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.CharField(default=timezone.now, max_length=150)
    main_content = models.TextField()

    def generate_slug():
        pass

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        self.status = self.status.title()
        super(normalNotes, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "note"

    def __str__(self):
        return self.name

    def get_url_path(self):
        parent_path = self.parent_folder.path.strip("/")
        slug = self.slug
        url = f"{parent_path}/{slug}"
        return url

    def get_breadcrumb_html(self):
        html = "<ol class=\"breadcrumb\">"
        path_list = self.get_url_path().split("/")
        # print(path_list)
        current_item = len(path_list) - 1
        # print(path_list)
        for item in path_list:
            path_index = path_list.index(item)
            # print(item, path_index)
            if path_index == 0:
                path = path_list[0]
            else:
                path = "/".join(path_list[:path_index+1])
            # print(path)
            url = reverse("show-content", args=[path])
            if path_index == current_item:
                path_html = f"<li class='breadcrumb-item active' aria-current='page'><a href='{url}'>{item.replace('_', ' ').title()}</a></li>"
            else:
                path_html = f"<li class='breadcrumb-item'><a href='{url}'>{item.replace('_', ' ').title()}</a></li>"
            html += path_html
        html += "</ol>"
        return html

class Papers(models.Model):
    note = models.OneToOneField(normalNotes, on_delete=models.CASCADE, primary_key=True, related_name="papers")
    year = models.CharField(max_length=10)
    link = models.URLField()
    bibtex = models.ForeignKey(Citations, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "paper"

    def __str__(self):
        return self.note.name
