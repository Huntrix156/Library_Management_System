# from django.contrib import messages
# from django.shortcuts import render, redirect, get_object_or_404
# from django.utils import timezone
#
# from returned_books.LendingForm import LendingForm
# from borrowed_books.models import Book
# from returned_books.models import LendingRecord
#
#
# from returned_books.models import ReturnedBook
#
#
# # Create your views here.
#
# # ── LENDING CATALOGUE — shows all books, lets librarian click "Lend" ─────────
# def LendingCatalogue(request):
#     """
#     READ: list every book with its live copies_available count.
#     The template adds a "Lend" button per book that links to LendBook(pk).
#     """
#     books = Book.objects.all()
#     return render(request, 'LendingCatalogue.html', {'books': books})
#
#
# # ── LEND A BOOK — form to record a new lending transaction ───────────────────
# def LendBook(request, pk):
#     """
#     CREATE a LendingRecord for book <pk>.
#
#     GET  → show the lending form pre-loaded with book info
#     POST → validate, deduct copies, save the record, redirect
#     """
#     book = get_object_or_404(Book, pk=pk)
#
#     if request.method == 'POST':
#         # Pass book= so the form can validate copies_lent vs copies_available
#         form = LendingForm(request.POST, book=book)
#         if form.is_valid():
#             copies = form.cleaned_data['copies_lent']
#
#             # Save the record without committing to DB yet (commit=False),
#             # so we can attach the book foreign key first.
#             record = form.save(commit=False)
#             record.book = book
#             record.save()
#
#             # Deduct lent copies from the book's available stock
#             book.copies_available -= copies
#             book.save()
#
#             messages.success(
#                 request,
#                 f'"{book.title}" lent to {record.borrower_name} '
#                 f'({copies} cop{"y" if copies == 1 else "ies"}). '
#                 f'{book.copies_available} remaining in catalogue.'
#             )
#             return redirect('LendingCatalogue')
#     else:
#         form = LendingForm(book=book)
#
#     # All active lending records for this book (for the history table)
#     active_lendings = LendingRecord.objects.filter(book=book, is_returned=False)
#
#     return render(request, 'LendBook.html', {
#         'book':           book,
#         'form':           form,
#         'active_lendings': active_lendings,
#     })
#
#
# # ── MARK A BOOK AS RETURNED ───────────────────────────────────────────────────
# def MarkReturned(request, record_id):
#     """
#     UPDATE: flip is_returned=True on a LendingRecord and restore copies.
#     Only executes on POST (button in a small form).
#     """
#     record = get_object_or_404(LendingRecord, pk=record_id)
#     if request.method == 'POST':
#         if not record.is_returned:
#             # Give copies back to the catalogue
#             record.book.copies_available += record.copies_lent
#             record.book.save()
#             record.is_returned = True
#             record.save()
#             messages.success(
#                 request,
#                 f'"{record.book.title}" marked as returned by {record.borrower_name}. '
#                 f'{record.book.copies_available} cop'
#                 f'{"y" if record.book.copies_available == 1 else "ies"} back in catalogue.'
#             )
#     return redirect('LendingCatalogue')
#
#
# # ── ALL ACTIVE LENDINGS ───────────────────────────────────────────────────────
# def ActiveLendings(request):
#     """
#     READ: show every LendingRecord that has not been returned yet.
#     Overdue records (due_date < today) are flagged in the template.
#     """
#     today   = timezone.now().date()
#     records = LendingRecord.objects.filter(is_returned=False).select_related('book')
#     return render(request, 'ActiveLendings.html', {
#         'records': records,
#         'today':   today,
#     })
#
#
# # ── EXISTING VIEW — kept untouched ────────────────────────────────────────────
# def Returned_books(request):
#     returned_books = ReturnedBook.objects.all().order_by('-return_date')
#     return render(request, 'Returned_books.html', {'returned_books': returned_books})


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from returned_books.LendingForm import LendingForm
from borrowed_books.models import Book
from returned_books.models import LendingRecord, ReturnedBook


# ── Permission helper ─────────────────────────────────────────────────────────
def _librarian_or_admin_required(view_func):
    """Only librarians and admins can lend / mark returns."""
    @login_required
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_librarian() or request.user.is_admin()):
            messages.error(request, 'Access denied. Librarians and admins only.')
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper


# ── Lending catalogue ─────────────────────────────────────────────────────────

@_librarian_or_admin_required
def LendingCatalogue(request):
    books = Book.objects.all()
    return render(request, 'LendingCatalogue.html', {'books': books})


# ── Lend a book ───────────────────────────────────────────────────────────────

@_librarian_or_admin_required
def LendBook(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = LendingForm(request.POST, book=book)
        if form.is_valid():
            copies = form.cleaned_data['copies_lent']
            record = form.save(commit=False)
            record.book = book
            record.save()
            book.copies_available -= copies
            book.save()
            messages.success(
                request,
                f'"{book.title}" lent to {record.borrower_name} '
                f'({copies} cop{"y" if copies == 1 else "ies"}). '
                f'{book.copies_available} remaining.'
            )
            return redirect('LendingCatalogue')
    else:
        form = LendingForm(book=book)

    active_lendings = LendingRecord.objects.filter(book=book, is_returned=False)
    return render(request, 'LendBook.html', {
        'book': book,
        'form': form,
        'active_lendings': active_lendings,
    })


# ── Mark returned ─────────────────────────────────────────────────────────────

@_librarian_or_admin_required
def MarkReturned(request, record_id):
    record = get_object_or_404(LendingRecord, pk=record_id)
    if request.method == 'POST':
        if not record.is_returned:
            record.book.copies_available += record.copies_lent
            record.book.save()
            record.is_returned = True
            record.save()
            messages.success(
                request,
                f'"{record.book.title}" marked as returned by {record.borrower_name}. '
                f'{record.book.copies_available} cop'
                f'{"y" if record.book.copies_available == 1 else "ies"} back in catalogue.'
            )
    return redirect('LendingCatalogue')


# ── Active lendings ───────────────────────────────────────────────────────────

@_librarian_or_admin_required
def ActiveLendings(request):
    today   = timezone.now().date()
    records = LendingRecord.objects.filter(is_returned=False).select_related('book')
    return render(request, 'ActiveLendings.html', {'records': records, 'today': today})


# ── Returned books history ────────────────────────────────────────────────────

@login_required
def Returned_books(request):
    returned_books = ReturnedBook.objects.all().order_by('-return_date')
    return render(request, 'Returned_books.html', {'returned_books': returned_books})

