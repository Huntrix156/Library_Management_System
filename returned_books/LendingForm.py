from django import forms
from returned_books.models import LendingRecord


class LendingForm(forms.ModelForm):
    """
    ModelForm for creating a new LendingRecord.

    We exclude:
      - book        → passed in via the URL (pk), not a form field
      - is_returned → always False on creation
      - date_borrowed → auto-set by the model default

    'copies_lent' gets a min_value validator so nobody can lend 0 copies.
    'due_date' uses a date-picker widget.
    """
    class Meta:
        model  = LendingRecord
        fields = ['borrower_name', 'copies_lent', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, book=None, **kwargs):
        """
        Accept the Book instance so we can validate copies_lent
        against copies_available on the book.
        """
        self.book = book
        super().__init__(*args, **kwargs)
        self.fields['copies_lent'].widget.attrs['min'] = 1
        if book:
            self.fields['copies_lent'].widget.attrs['max'] = book.copies_available

    def clean_copies_lent(self):
        """
        Custom validator: copies_lent must not exceed copies_available.
        This runs automatically when form.is_valid() is called.
        """
        copies = self.cleaned_data['copies_lent']
        if copies < 1:
            raise forms.ValidationError("You must lend at least 1 copy.")
        if self.book and copies > self.book.copies_available:
            raise forms.ValidationError(
                f"Only {self.book.copies_available} cop"
                f"{'y' if self.book.copies_available == 1 else 'ies'} available."
            )
        return copies