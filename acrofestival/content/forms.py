from django import forms

from acrofestival.content.models import Teacher


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ("name", "country", "photo", "bio", "instagram_url", "website_url", "notes")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 6}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
