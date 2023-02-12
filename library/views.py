from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Book, Emprunt, Exemplaires
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
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
    try:
        mon_emprunts = Emprunt.objects.get(
            user_id=request.user.id, exemplaire__id_book=livre_id)

    except Emprunt.DoesNotExist:
        mon_emprunts = None
    print()
    if request.method == 'POST':
        if request.POST.get('exemplaire'):
            exemplaire = Exemplaires.objects.get(
                id=request.POST.get('exemplaire'))
            exemplaire.quantity = exemplaire.quantity - 1
            exemplaire.save()
            emprunt = Emprunt.objects.create(
                user=request.user,
                exemplaire_id=exemplaire.id,
                date_emprunt=datetime.now(),
                date_retour_prevue=datetime.now() + timedelta(days=60)
            )
            emprunt.save()
            messages.success(request, "Register success.")
            return redirect('home')
            # bookstores = book.bookstore_set.filter(exemplaires__quantity__gte=exemplaire)
    return render(request, "detail-livre.html", {'book': book, 'bookstores': bookstores, 'mon_emprunts': mon_emprunts})
