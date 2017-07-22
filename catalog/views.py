from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
import datetime
from django.views import generic
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from .models import Author
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView,DeleteView

# Create your views here.

from .models import Book, Author, BookInstance, Genre
from .forms import RenewBookForm

def index(request):
    """
    View function for homepage of site
    """
    #Generate count of some main objects
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()

    #Available BookInstance
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  #the all() is implied by default
    num_genre=Genre.objects.count()
    num_books=Book.objects.filter(title__icontains='ka').count()

    #Render the html
    return render(request,'index.html',context={'num_books':num_books,'num_genre':num_genre,'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,'num_authors':num_authors},)

class BookListView(generic.ListView):
    model=Book
    paginate_by=3

class BookDetailView(generic.DetailView):
    model=Book
    paginate_by=10

class AuthorListView(generic.ListView):
    model=Author
    paginate_by=5

class AuthorDetailView(generic.DetailView):
    model=Author
    paginate_by=5

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model=BookInstance
    template_name='catalog/bookinstance_lis_borrowed_user.html'
    paginate_by=2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllLoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    permission_required='catalog.can_mark_returned'
    model=BookInstance
    template_name='catalog/all_borrowed_books_list_view.html'
    paginate_by=1

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request,pk):
    book_inst=get_object_or_404(BookInstance,pk=pk)
    if request.method=='POST':
        form=RenewBookForm(request.POST)
        if form.is_valid():
            book_inst.due_back=form.cleaned_data['renewal_date']
            book_inst.save()

            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        proposed_renewal_date=datetime.date.today()+datetime.timedelta(weeks=3)
        form=RenewBookForm(initial={'renewal_date':proposed_renewal_date,})

    return render(request,'catalog/book_renew_librarian.html',{'form':form,'bookinst':book_inst})

class AuthorCreate(PermissionRequiredMixin,CreateView):
    permission_required='catalog.can_mark_returned'
    model=Author
    fields='__all__'
    initial={'date_of_death':'12/10/2016'}

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    permission_required='catalog.can_mark_returned'
    model=Author
    fields=['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    permission_required='catalog.can_mark_returned'
    model=Author
    success_url=reverse_lazy('authors')

class BookUpdate(PermissionRequiredMixin,UpdateView):
    permission_required='can_mark_returned'
    model=Book
    fields=['title','author','summary','isbn','genre']

class BookCreate(PermissionRequiredMixin,CreateView):
    permission_required='can_mark_returned'
    model=Book
    fields='__all__'
    initial={'author':'Teibok'}

class BookDelete(PermissionRequiredMixin,DeleteView):
    permission_required='can_mark_returned'
    model=Book
    success_url=reverse_lazy('books')
