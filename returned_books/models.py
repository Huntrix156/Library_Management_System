from django.db import models
from django.utils import timezone

# Create your models here.
class ReturnedBook(models.Model):
    book = models.ForeignKey('borrowed_books.Book', on_delete=models.CASCADE)
    borrower_name = models.CharField(max_length=255)
    return_date = models.DateField(auto_now_add=True)




class LendingRecord(models.Model):
    """
    Captures every lending transaction.

    Fields
    ------
    book              → ForeignKey to Book (which book was lent)
    borrower_name     → full name of the person borrowing
    copies_lent       → how many copies of this book this borrower took
    date_borrowed     → auto-set to the moment the form is submitted
    due_date          → librarian sets the deadline for return
    is_returned       → False until the book is handed back
    """
    book = models.ForeignKey(
        'borrowed_books.Book',
        on_delete=models.CASCADE,
        related_name='lending_records'
    )
    borrower_name = models.CharField(max_length=255)
    copies_lent   = models.PositiveIntegerField(default=1)
    date_borrowed = models.DateTimeField(default=timezone.now)
    due_date      = models.DateField()
    is_returned   = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_borrowed']

    def __str__(self):
        return f"{self.borrower_name} — {self.book.title} ({self.copies_lent} cop.)"