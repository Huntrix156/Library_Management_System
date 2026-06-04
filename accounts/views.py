# from django.contrib import messages
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
#
# from .forms import RegisterForm, LoginForm
#
#
# def register_view(request):
#     """Public registration — always creates a 'member' accounts."""
#     if request.user.is_authenticated:
#         return redirect('dashboard_redirect')
#
#     form = RegisterForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.save(commit=False)
#         user.role = 'member'          # public sign-ups are always members
#         user.save()
#         login(request, user)
#         messages.success(request, f'Welcome, {user.first_name}! Your accounts has been created.')
#         return redirect('dashboard_redirect')
#
#     return render(request, 'accounts/register.html', {'form': form})
#
#
# def login_view(request):
#     """Login page — redirects to the correct dashboard based on role."""
#     if request.user.is_authenticated:
#         return redirect('dashboard_redirect')
#
#     form = LoginForm(request, data=request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.get_user()
#         login(request, user)
#         messages.success(request, f'Welcome back, {user.first_name or user.username}!')
#         return redirect('dashboard_redirect')
#
#     return render(request, 'accounts/login.html', {'form': form})
#
#
# def logout_view(request):
#     logout(request)
#     messages.info(request, 'You have been logged out.')
#     return redirect('login')
#
#
# @login_required
# def dashboard_redirect(request):
#     """Send each role to their own dashboard."""
#     role = request.user.role
#     if role == 'admin':
#         return redirect('admin_dashboard')
#     elif role == 'librarian':
#         return redirect('librarian_dashboard')
#     else:
#         return redirect('member_dashboard')
#
#
# @login_required
# def admin_dashboard(request):
#     if not request.user.is_admin():
#         messages.error(request, 'Access denied.')
#         return redirect('dashboard_redirect')
#
#     from borrowed_books.models import Book
#     from returned_books.models import LendingRecord
#     from .models import CustomUser
#
#     context = {
#         'total_books':      Book.objects.count(),
#         'total_copies':     sum(b.copies_available for b in Book.objects.all()),
#         'active_lendings':  LendingRecord.objects.filter(is_returned=False).count(),
#         'total_members':    CustomUser.objects.filter(role='member').count(),
#         'total_librarians': CustomUser.objects.filter(role='librarian').count(),
#         'recent_lendings':  LendingRecord.objects.filter(is_returned=False).select_related('book')[:5],
#         'all_users':        CustomUser.objects.all().order_by('-date_joined')[:10],
#     }
#     return render(request, 'accounts/admin_dashboard.html', context)
#
#
# @login_required
# def librarian_dashboard(request):
#     if not request.user.is_librarian():
#         messages.error(request, 'Access denied.')
#         return redirect('dashboard_redirect')
#
#     from borrowed_books.models import Book
#     from returned_books.models import LendingRecord
#     from django.utils import timezone
#
#     today   = timezone.now().date()
#     context = {
#         'total_books':     Book.objects.count(),
#         'total_copies':    sum(b.copies_available for b in Book.objects.all()),
#         'active_lendings': LendingRecord.objects.filter(is_returned=False).count(),
#         'overdue':         LendingRecord.objects.filter(is_returned=False, due_date__lt=today).count(),
#         'recent_lendings': LendingRecord.objects.filter(is_returned=False).select_related('book')[:5],
#     }
#     return render(request, 'accounts/librarian_dashboard.html', context)
#
#
# @login_required
# def member_dashboard(request):
#     if not request.user.is_member():
#         messages.error(request, 'Access denied.')
#         return redirect('dashboard_redirect')
#
#     from borrowed_books.models import Book
#
#     context = {
#         'books': Book.objects.filter(copies_available__gt=0).order_by('-date_added'),
#     }
#     return render(request, 'accounts/member_dashboard.html', context)



from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm
#
#
# # ── Shared permission decorators ──────────────────────────────────────────────
#
# def admin_required(view_func):
#     """Redirect non-admins away with an error message."""
#     @login_required
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_admin():
#             messages.error(request, 'Access denied. Admins only.')
#             return redirect('dashboard_redirect')
#         return view_func(request, *args, **kwargs)
#     wrapper.__name__ = view_func.__name__
#     return wrapper
#
#
# def librarian_required(view_func):
#     """Redirect non-librarians away with an error message."""
#     @login_required
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_librarian():
#             messages.error(request, 'Access denied. Librarians only.')
#             return redirect('dashboard_redirect')
#         return view_func(request, *args, **kwargs)
#     wrapper.__name__ = view_func.__name__
#     return wrapper
#
#
# def member_required(view_func):
#     """Redirect non-members away with an error message."""
#     @login_required
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_member():
#             messages.error(request, 'Access denied. Members only.')
#             return redirect('dashboard_redirect')
#         return view_func(request, *args, **kwargs)
#     wrapper.__name__ = view_func.__name__
#     return wrapper
#
#
# # ── Public views ──────────────────────────────────────────────────────────────
#
# def register_view(request):
#     """Public registration — always creates a 'member' account."""
#     if request.user.is_authenticated:
#         return redirect('dashboard_redirect')
#
#     form = RegisterForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.save(commit=False)
#         user.role = 'member'
#         user.save()
#
#         # Auto-assign to member group
#         from django.contrib.auth.models import Group
#         member_group, _ = Group.objects.get_or_create(name='member')
#         user.groups.add(member_group)
#
#         login(request, user)
#         messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
#         return redirect('dashboard_redirect')
#
#     return render(request, 'accounts/register.html', {'form': form})
#
#
# def login_view(request):
#     """Login page — redirects to the correct dashboard based on role."""
#     if request.user.is_authenticated:
#         return redirect('dashboard_redirect')
#
#     form = LoginForm(request, data=request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.get_user()
#         login(request, user)
#         messages.success(request, f'Welcome back, {user.first_name or user.username}!')
#         return redirect('dashboard_redirect')
#
#     return render(request, 'accounts/login.html', {'form': form})
#
#
# def logout_view(request):
#     logout(request)
#     messages.info(request, 'You have been logged out.')
#     return redirect('login')
#
#
# # ── Dashboard router ──────────────────────────────────────────────────────────
#
# @login_required
# def dashboard_redirect(request):
#     """Send each role to their own dashboard."""
#     role = request.user.role
#     if role == 'admin':
#         return redirect('admin_dashboard')
#     elif role == 'librarian':
#         return redirect('librarian_dashboard')
#     else:
#         return redirect('member_dashboard')
#
#
# # ── Role dashboards ───────────────────────────────────────────────────────────
#
# @admin_required
# def admin_dashboard(request):
#     from borrowed_books.models import Book
#     from returned_books.models import LendingRecord
#     from .models import CustomUser
#
#     context = {
#         'total_books':      Book.objects.count(),
#         'total_copies':     sum(b.copies_available for b in Book.objects.all()),
#         'active_lendings':  LendingRecord.objects.filter(is_returned=False).count(),
#         'total_members':    CustomUser.objects.filter(role='member').count(),
#         'total_librarians': CustomUser.objects.filter(role='librarian').count(),
#         'recent_lendings':  LendingRecord.objects.filter(is_returned=False).select_related('book')[:5],
#         'all_users':        CustomUser.objects.all().order_by('-date_joined')[:10],
#     }
#     return render(request, 'accounts/admin_dashboard.html', context)
#
#
# @librarian_required
# def librarian_dashboard(request):
#     from borrowed_books.models import Book
#     from returned_books.models import LendingRecord
#     from django.utils import timezone
#
#     today = timezone.now().date()
#     context = {
#         'total_books':     Book.objects.count(),
#         'total_copies':    sum(b.copies_available for b in Book.objects.all()),
#         'active_lendings': LendingRecord.objects.filter(is_returned=False).count(),
#         'overdue':         LendingRecord.objects.filter(is_returned=False, due_date__lt=today).count(),
#         'recent_lendings': LendingRecord.objects.filter(is_returned=False).select_related('book')[:5],
#     }
#     return render(request, 'accounts/librarian_dashboard.html', context)
#
#
# @member_required
# def member_dashboard(request):
#     from borrowed_books.models import Book
#
#     context = {
#         'books': Book.objects.filter(copies_available__gt=0).order_by('-date_added'),
#     }
#     return render(request, 'accounts/member_dashboard.html', context)
#




# from django.contrib import messages
# from django.contrib.auth import login, logout, authenticate
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect
#
# from .forms import RegisterForm, LoginForm
#
#
# def register_view(request):
#     """Public registration — always creates a 'member' accounts."""
#     if request.user.is_authenticated:
#         return redirect('dashboard_redirect')
#
#     form = RegisterForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.save(commit=False)
#         user.role = 'member'          # public sign-ups are always members
#         user.save()
#         login(request, user)
#         messages.success(request, f'Welcome, {user.first_name}! Your accounts has been created.')
#         return redirect('dashboard_redirect')
#
#     return render(request, 'accounts/register.html', {'form': form})
#
#
# def login_view(request):
#     """Login page — redirects to the correct dashboard based on role."""
#     if request.user.is_authenticated:
#         return redirect('dashboard_redirect')
#
#     form = LoginForm(request, data=request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         user = form.get_user()
#         login(request, user)
#         messages.success(request, f'Welcome back, {user.first_name or user.username}!')
#         return redirect('dashboard_redirect')
#
#     return render(request, 'accounts/login.html', {'form': form})
#
#
# def logout_view(request):
#     logout(request)
#     messages.info(request, 'You have been logged out.')
#     return redirect('login')
#
#
# @login_required
# def dashboard_redirect(request):
#     """Send each role to their own dashboard."""
#     role = request.user.role
#     if role == 'admin':
#         return redirect('admin_dashboard')
#     elif role == 'librarian':
#         return redirect('librarian_dashboard')
#     else:
#         return redirect('member_dashboard')
#
#
# @login_required
# def admin_dashboard(request):
#     if not request.user.is_admin():
#         messages.error(request, 'Access denied.')
#         return redirect('dashboard_redirect')
#
#     from borrowed_books.models import Book
#     from returned_books.models import LendingRecord
#     from .models import CustomUser
#
#     context = {
#         'total_books':      Book.objects.count(),
#         'total_copies':     sum(b.copies_available for b in Book.objects.all()),
#         'active_lendings':  LendingRecord.objects.filter(is_returned=False).count(),
#         'total_members':    CustomUser.objects.filter(role='member').count(),
#         'total_librarians': CustomUser.objects.filter(role='librarian').count(),
#         'recent_lendings':  LendingRecord.objects.filter(is_returned=False).select_related('book')[:5],
#         'all_users':        CustomUser.objects.all().order_by('-date_joined')[:10],
#     }
#     return render(request, 'accounts/admin_dashboard.html', context)
#
#
# @login_required
# def librarian_dashboard(request):
#     if not request.user.is_librarian():
#         messages.error(request, 'Access denied.')
#         return redirect('dashboard_redirect')
#
#     from borrowed_books.models import Book
#     from returned_books.models import LendingRecord
#     from django.utils import timezone
#
#     today   = timezone.now().date()
#     context = {
#         'total_books':     Book.objects.count(),
#         'total_copies':    sum(b.copies_available for b in Book.objects.all()),
#         'active_lendings': LendingRecord.objects.filter(is_returned=False).count(),
#         'overdue':         LendingRecord.objects.filter(is_returned=False, due_date__lt=today).count(),
#         'recent_lendings': LendingRecord.objects.filter(is_returned=False).select_related('book')[:5],
#     }
#     return render(request, 'accounts/librarian_dashboard.html', context)
#
#
# @login_required
# def member_dashboard(request):
#     if not request.user.is_member():
#         messages.error(request, 'Access denied.')
#         return redirect('dashboard_redirect')
#
#     from borrowed_books.models import Book
#
#     context = {
#         'books': Book.objects.filter(copies_available__gt=0).order_by('-date_added'),
#     }
#     return render(request, 'accounts/member_dashboard.html', context)



from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import RegisterForm, LoginForm


# ── Shared permission decorators ──────────────────────────────────────────────

def admin_required(view_func):
    """Redirect non-admins away with an error message."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(request, 'Access denied. Admins only.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def librarian_required(view_func):
    """Redirect non-librarians away with an error message."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_librarian():
            messages.error(request, 'Access denied. Librarians only.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


def member_required(view_func):
    """Redirect non-members away with an error message."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_member():
            messages.error(request, 'Access denied. Members only.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── Public views ──────────────────────────────────────────────────────────────

def register_view(request):
    """Public registration — always creates a 'member' account."""
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save(commit=False)
        user.role = 'member'
        user.save()

        # Auto-assign to member group
        from django.contrib.auth.models import Group
        member_group, _ = Group.objects.get_or_create(name='member')
        user.groups.add(member_group)

        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
        return redirect('dashboard_redirect')

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """Login page — redirects to the correct dashboard based on role."""
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        return redirect('dashboard_redirect')

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ── Dashboard router ──────────────────────────────────────────────────────────

@login_required
def dashboard_redirect(request):
    """Send each role to their own dashboard."""
    role = request.user.role
    if role == 'admin':
        return redirect('admin_dashboard')
    elif role == 'librarian':
        return redirect('librarian_dashboard')
    else:
        return redirect('member_dashboard')


# ── Role dashboards ───────────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    from borrowed_books.models import Book
    from returned_books.models import LendingRecord
    from .models import CustomUser
    from django.utils import timezone

    today = timezone.now().date()
    context = {
        'today': today,
        'total_books':      Book.objects.count(),
        'total_copies':     sum(b.copies_available for b in Book.objects.all()),
        'active_lendings':  LendingRecord.objects.filter(is_returned=False).count(),
        'total_members':    CustomUser.objects.filter(role='member').count(),
        'total_librarians': CustomUser.objects.filter(role='librarian').count(),
        'recent_lendings':  LendingRecord.objects.filter(is_returned=False).select_related('book')[:5],
        'all_users':        CustomUser.objects.all().order_by('-date_joined')[:10],
    }
    return render(request, 'accounts/admin_dashboard.html', context)


@librarian_required
def librarian_dashboard(request):
    from borrowed_books.models import Book
    from returned_books.models import LendingRecord
    from django.utils import timezone

    today = timezone.now().date()
    context = {
        'total_books':     Book.objects.count(),
        'total_copies':    sum(b.copies_available for b in Book.objects.all()),
        'active_lendings': LendingRecord.objects.filter(is_returned=False).count(),
        'overdue':         LendingRecord.objects.filter(is_returned=False, due_date__lt=today).count(),
        'recent_lendings': LendingRecord.objects.filter(is_returned=False).select_related('book')[:5],
    }
    return render(request, 'accounts/librarian_dashboard.html', context)


@member_required
def member_dashboard(request):
    from borrowed_books.models import Book

    context = {
        'books': Book.objects.filter(copies_available__gt=0).order_by('-date_added'),
    }
    return render(request, 'accounts/member_dashboard.html', context)