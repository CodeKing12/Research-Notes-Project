from django.http import Http404, HttpResponse
from os import path

def displayFile(request, parent, path_to_file, file_name):
    # boolean = path.exists('templates/all_notes/classes/econ101/My First Note.md')
    file = f'templates/all_notes/{parent}/{path_to_file}/{file_name}'
    file_exists = path.exists(file)
    if not file_exists:
        raise Http404
    
    return HttpResponse(
        f"""
        Parent: {parent}
        File Path: {path_to_file}
        Name of File: {file_name}
        File Exists: {file_exists}
        """
    )