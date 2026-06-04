from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import CustomUser


# ── Helper: get-or-create the three role groups ───────────────────────────────

def _get_or_create_groups():
    admin_group, _     = Group.objects.get_or_create(name='admin')
    librarian_group, _ = Group.objects.get_or_create(name='librarian')
    member_group, _    = Group.objects.get_or_create(name='member')
    return admin_group, librarian_group, member_group


def _sync_group(user):
    """Remove user from all role-groups, then add them to the correct one."""
    admin_group, librarian_group, member_group = _get_or_create_groups()
    role_groups = {admin_group, librarian_group, member_group}

    user.groups.remove(*role_groups)

    mapping = {
        'admin':     admin_group,
        'librarian': librarian_group,
        'member':    member_group,
    }
    target = mapping.get(user.role)
    if target:
        user.groups.add(target)


# ── CustomUser admin ──────────────────────────────────────────────────────────

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display   = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter    = ('role', 'is_staff', 'is_active')
    list_editable  = ('role',)
    search_fields  = ('username', 'email', 'first_name', 'last_name')
    ordering       = ('-date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        ('Library Role', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Library Role', {'fields': ('role',)}),
    )

    def save_model(self, request, obj, form, change):
        # Admin-role users need is_staff=True to access /admin/
        if obj.role == 'admin':
            obj.is_staff = True
        super().save_model(request, obj, form, change)
        _sync_group(obj)