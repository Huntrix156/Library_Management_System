from django import forms

from borrowed_books.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'genre', 'published_year',
                  'copies_available', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Things Fall Apart'}),
            'author': forms.TextInput(attrs={'placeholder': 'e.g. Chinua Achebe'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'e.g. 978-0385474542'}),
            'published_year': forms.NumberInput(attrs={'placeholder': 'e.g. 1958'}),
            'copies_available': forms.NumberInput(attrs={'min': 1}),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Brief description of the book…'
            }),
        }