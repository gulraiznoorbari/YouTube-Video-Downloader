from django import forms

class DownloadForm(forms.Form):
    url = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder":"Enter Video URL...", "autocomplete":"off"}), 
        label=False
    )
