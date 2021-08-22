from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views import View, generic
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# login_required is for function based view but LoginRequiredMixin is for CBW

from .models import Author, Book, BookInstance
from .forms import *


def index(request):
    num_books = Book.objects.count()
    num_book_instance = BookInstance.objects.count()
    num_book_instance_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_book_instance,
        'num_instances_available': num_book_instance_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }
    return render(request, template_name='catalog/index.html', context=context)


class BookList(generic.ListView):
    model = Book
    template_name = 'catalog/book_list.html'
    paginate_by = 5
    # login_url = '/accounts/login/'  # the default

# class BookList(View):
#     def get(self, request):
#         books = Book.objects.all()
#         return render(request, 'book_list.html', context={'books': books})


# class AuthorList(LoginRequiredMixin, generic.ListView):
class AuthorList(generic.ListView):
    model = Author
    template_name = 'catalog/author_list.html'
    paginate_by = 5

# def author_list(request):
#     authors = Author.objects.all()
#     return render(request, 'author_list.html', context={'authors': authors})


class BookDetail(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

# def book_detail(request, id):
#     book = get_object_or_404(Book, id=id)
#     return render(request, 'book_detail.html', context={'book': book})


class AuthorDetail(generic.DetailView):
    model = Author
    template_name = 'catalog/author_detail.html'

# def author_detail(request, id):
#     author = get_object_or_404(Author, id=id)
#     return render(request, 'author_detail.html', context={'author': author})


class MyBooks(LoginRequiredMixin, generic.ListView):
    template_name = 'catalog/my_books.html'

    def get_queryset(self, *args, **kwargs):
        return Book.objects.filter(author__first_name=self.request.user.username)


class UserBorrowedBooks(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/user_borrowed_books.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects\
            .filter(borrower=self.request.user)\
            .filter(status=BookInstance.LoanStatus.ON_LOAN)\
            .order_by('due_back')


class Borrowed(PermissionRequiredMixin, View):
    """
    get: show all borrowed books
    post: return a given book
    """
    permission_required = ('catalog.can_mark_returned',)

    def get(self, request):
        book_instances = BookInstance.objects.filter(status__exact='o')
        form = ReturnBookForm()
        return render(request, 'catalog/borrowed.html', {'book_instances': book_instances, 'form': form})

    def post(self, request):
        book_instances = BookInstance.objects.filter(status__exact='o')
        form = ReturnBookForm(request.POST)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            book_instance = get_object_or_404(BookInstance, pk=book_id)
            book_instance.status = BookInstance.LoanStatus.AVAILABLE
            book_instance.due_back = None
            book_instance.borrower = None
            book_instance.save()
        return render(request, 'catalog/borrowed.html', {'book_instances': book_instances, 'form': form})

    # def get(self, request):
    #     book_instances = BookInstance.objects.filter(status__exact='o')
    #     return render(request, 'catalog/borrowed.html', {'book_instances': book_instances})
    #
    # def post(self, request):
    #     pk = request.POST.get('pk', False)
    #     if not pk:
    #         return HttpResponse("Please enter book instance id")
    #     book_instance = get_object_or_404(BookInstance, pk=pk)
    #     book_instance.status = BookInstance.LoanStatus.AVAILABLE
    #     book_instance.due_back = None
    #     book_instance.borrower = None
    #     book_instance.save()
    #     return HttpResponse(f"{book_instance.book.title} is returned!")


class RenewBookLibrarian(PermissionRequiredMixin, LoginRequiredMixin, View):
    permission_required = ('catalog.can_mark_returned',)

    def get(self, request, pk):
        book_instance = get_object_or_404(BookInstance, pk=pk)
        proposed_due_back = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'due_back': proposed_due_back})
        context = {
            'form': form,
            'book_instance': book_instance,
        }
        return render(request, 'catalog/book_renew_librarian.html', context)

    def post(self, request, pk):
        form = RenewBookForm(request.POST)
        book_instance = get_object_or_404(BookInstance, pk=pk)
        if form.is_valid():
            form.save()
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()
            return HttpResponseRedirect(reverse_lazy('all-borrowed'))
        context = {
            'form': form,
            'book_instance': book_instance,
        }
        return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, generic.CreateView):
    # default template name would be 'model_name_form.html'
    permission_required = ('catalog.can_mark_returned',)
    model = Author
    fields = '__all__'


class AuthorEdit(PermissionRequiredMixin, generic.UpdateView):
    permission_required = ('catalog.can_mark_returned',)
    model = Author
    fields = '__all__'


class AuthorDelete(PermissionRequiredMixin, generic.DeleteView):
    # default template name would be 'model_name_confirm_delete.html'
    permission_required = ('catalog.can_mark_returned',)
    model = Author
    success_url = reverse_lazy('author-list')


class BookCreate(PermissionRequiredMixin, generic.CreateView):
    # default template name would be 'model_name_form.html'
    permission_required = ('catalog.can_mark_returned',)
    model = Book
    fields = '__all__'


class BookEdit(PermissionRequiredMixin, generic.UpdateView):
    permission_required = ('catalog.can_mark_returned',)
    model = Book
    fields = '__all__'


class BookDelete(PermissionRequiredMixin, generic.DeleteView):
    # default template name would be 'model_name_confirm_delete.html'
    permission_required = ('catalog.can_mark_returned',)
    model = Book
    success_url = reverse_lazy('book-list')


@login_required()
def test(request):
    return HttpResponse("Hello World")

