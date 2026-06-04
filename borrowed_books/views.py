# from django.contrib import messages
# from django.db.models import Q
# from django.shortcuts import render, redirect, get_object_or_404
#
# from borrowed_books.BookForm import BookForm
# from borrowed_books.models import Book
#
#
# # Create your views here.
#
# def Addbook(request):
#     if request.method == 'POST':
#         form = BookForm(request.POST)
#         if form.is_valid():
#             book = form.save()
#             messages.success(request, f'"{book.title}" was added to the catalogue!')
#             return redirect('Addbook')  # PRG pattern — prevents double-submit on refresh
#     else:
#         form = BookForm()
#
#     # books = Book.objects.all()
#     return render(request, 'Addbook.html', {'form': form,
#                                             # 'books': books
#                                             })
#
#
# def BookCatalogue(request):
#     # query
#     query = request.GET.get('q', '').strip()
#
#     books = Book.objects.all()  # responsible to display all books
#
#     if query:
#         books = books.filter(
#             Q(title__icontains=query) |
#             Q(author__icontains=query)
#         )
#
#     return render(request, 'BookCatalogue.html', {'books': books,'query': query})
#
#
# def BookDetail(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     return render(request, 'BookDetail.html', {'book': book})
#
#
# def EditBook(request, pk):
#     book = get_object_or_404(Book, pk=pk)       # fetch the existing record
#     if request.method == 'POST':
#         form = BookForm(request.POST, instance=book)  # KEY: instance= tells Django to UPDATE, not INSERT
#         if form.is_valid():
#             form.save()                          # runs SQL UPDATE
#             messages.success(request, f'"{book.title}" was updated successfully!')
#             return redirect('BookCatalogue')
#     else:
#         form = BookForm(instance=book)           # pre-fills the form with existing data
#     return render(request, 'EditBook.html', {'form': form, 'book': book})
#
# def DeleteBook(request, pk):
#     book = get_object_or_404(Book, pk=pk)   # fetch record
#     if request.method == 'POST':            # only delete on POST (confirmation form)
#         title = book.title                  # save the title BEFORE deleting (can't access it after)
#         book.delete()                       # runs SQL DELETE
#         messages.success(request, f'"{title}" was removed from the catalogue.')
#         return redirect('BookCatalogue')
#     return render(request, 'DeleteBook.html', {'book': book})  # GET: show confirmation page
#
#
#
# def Dashboard(request):
#     return render(request,'Dashboard.html')
# def base(request):
#     return render(request,'base.html')
# def index(request):
#     return render(request,'index.html')
#
# def b(request):
#     return render(request,'b.html')
#


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from borrowed_books.BookForm import BookForm
from borrowed_books.models import Book


# ── Permission helpers (import from accounts to stay DRY) ────────────────────
def _admin_or_librarian_required(view_func):
    """Only admins and librarians may manage books."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_admin() or request.user.is_librarian()):
            messages.error(request, 'Access denied. Librarians and admins only.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── Book catalogue — all logged-in users can browse ──────────────────────────

@login_required
def BookCatalogue(request):
    query = request.GET.get('q', '').strip()
    books = Book.objects.all()
    if query:
        books = books.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    return render(request, 'BookCatalogue.html', {'books': books, 'query': query})


@login_required
def BookDetail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'BookDetail.html', {'book': book})


# ── Add / Edit / Delete — librarians and admins only ─────────────────────────

@_admin_or_librarian_required
def Addbook(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'"{book.title}" was added to the catalogue!')
            return redirect('Addbook')
    else:
        form = BookForm()
    return render(request, 'Addbook.html', {'form': form})


@_admin_or_librarian_required
def EditBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{book.title}" was updated successfully!')
            return redirect('BookCatalogue')
    else:
        form = BookForm(instance=book)
    return render(request, 'EditBook.html', {'form': form, 'book': book})


@_admin_or_librarian_required
def DeleteBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'"{title}" was removed from the catalogue.')
        return redirect('BookCatalogue')
    return render(request, 'DeleteBook.html', {'book': book})


# ── Legacy / utility views ────────────────────────────────────────────────────

@login_required
def Dashboard(request):
    return redirect('dashboard_redirect')

def base(request):
    return render(request, 'base.html')

def index(request):
    return render(request, 'index.html')

def b(request):
    return render(request, 'b.html')
