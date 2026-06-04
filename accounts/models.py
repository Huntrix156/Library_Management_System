from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin',     'Admin'),
        ('librarian', 'Librarian'),
        ('member',    'Member'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def is_admin(self):
        return self.role == 'admin'

    def is_librarian(self):
        return self.role == 'librarian'

    def is_member(self):
        return self.role == 'member'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"