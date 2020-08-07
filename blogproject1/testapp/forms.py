from django import forms
class EmailSendForm(forms.Form):
     Name=forms.CharField()
     Email=forms.EmailField()
     To=forms.EmailField()
     Comments=forms.CharField(required=False,widget=forms.Textarea)
