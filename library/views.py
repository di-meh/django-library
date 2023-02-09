from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Bookstore
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views.py here.


def index(request):
    books = Book.objects.all().order_by('title')
    paginator = Paginator(books, 12)
    search = request.GET.get('search')
    page = request.GET.get('page') or 1

    if (search):
        books = Book.objects.filter(Q(title__icontains=search) | Q(
            author__icontains=search) | Q(tags__icontains=search))
    # if(page.isnumeric()):
    books = paginator.get_page(page)

    return render(request, "liste-livre.html", {'books': books, 'page': page})

def detail(request, livre_id):
    book = Book.objects.get(id=livre_id)
    bookstores = book.bookstore_set.all()
    return render(request, "detail-livre.html", {'book': book, 'bookstores': bookstores })

def backoffice(request):
    return render(request, "./backoffice/home.html", {})