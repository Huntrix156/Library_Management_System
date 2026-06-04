
# Create your models here.
from django.db import models


class Book(models.Model):
    # tuple
    GENRE_CHOICES = [
        ('fiction', 'Fiction'),
        ('non_fiction', 'Non-Fiction'),
        ('science', 'Science'),
        ('history', 'History'),
        ('biography', 'Biography'),
        ('technology', 'Technology'),
        ('arts', 'Arts & Literature'),
        ('other', 'Other'),
    ]
    # fields
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='other')
    published_year = models.PositiveIntegerField()
    copies_available = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.author}"

    class Meta:
        ordering = ['-date_added']
