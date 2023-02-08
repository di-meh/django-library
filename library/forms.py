from django import forms

from library.models import ReadingClub, ReadingClubSession


class ReadingClubForm(forms.ModelForm):
    class Meta:
        model = ReadingClub
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

class ReadingClubSessionForm(forms.ModelForm):
    class Meta:
        model = ReadingClubSession
        fields = ('date', 'description')
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }