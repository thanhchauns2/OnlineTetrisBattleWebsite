from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()

class FileUploadDuelForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()