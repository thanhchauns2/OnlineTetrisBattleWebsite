from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()

class FileUploadDuelForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()

class TournamentForm(forms.Form):
    tournament_id = forms.CharField(label='Tournament ID', max_length=100)