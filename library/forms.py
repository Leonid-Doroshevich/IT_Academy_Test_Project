from django import forms
from .models import Author, Book

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name and last_name:
            # Проверяем, существует ли уже автор с таким же именем и фамилией
            existing_author = Author.objects.filter(first_name=first_name, last_name=last_name).exclude(id=self.instance.id).first()
            if existing_author:
                raise forms.ValidationError("Такой автор уже существует.")

        return cleaned_data


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'