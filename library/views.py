from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from library.forms import ReadingClubForm, ReadingClubSessionForm, BookForm
from library.models import ReadingClub, ReadingClubSession

from .models import Book, Bookstore, Emprunt, Exemplaires
from django.db.models import Q
from django.core.paginator import Paginator



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
    return render(request, "library/books/index.html", {'books': books, 'page': page})
    # return render(request, 'library/index.html')

def detail(request, livre_id):
    book = Book.objects.get(id=livre_id)
    bookstores = book.bookstore_set.all()
    try:
        mon_emprunts = Emprunt.objects.get(
            user_id=request.user.id, exemplaire__id_book=livre_id)
    except Emprunt.DoesNotExist:
        mon_emprunts = None

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
            messages.success(request, "Votre emprunt a été effectué avec succès")
            return redirect('home')
            # bookstores = book.bookstore_set.filter(exemplaires__quantity__gte=exemplaire)
    return render(request, "library/books/show.html", {'book': book, 'bookstores': bookstores, 'mon_emprunts': mon_emprunts })

def backoffice(request):
    return render(request, "./backoffice/home.html", {})

@login_required
def backoffice_create_book(request):
    if not request.user.is_staff:
        return redirect('library')

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            addBook = form.save()
            if addBook:
                messages.success(request, "Book added.")
                return redirect('backoffice_create_book')
            else:
                messages.error(request, form.errors)
                return redirect('backoffice_create_book')
        else:
            messages.error(request, form.errors)
            return redirect('backoffice_create_book')
    else:
        form = BookForm()
        return render(request, './backoffice/books/create.html', {'form': form})

def reading_clubs(request):
    # Get all reading clubs
    reading_clubs_object = ReadingClub.objects.all()
    return render(request, 'library/reading-clubs/index.html', {'reading_clubs': reading_clubs_object})

@login_required
def create_reading_club(request):
    if not request.user.is_staff:
        return redirect('reading_clubs')

    if request.method == 'POST':
        form = ReadingClubForm(request.POST)
        if form.is_valid():
            reading_club = form.save()
            if reading_club:
                messages.success(request, "Reading club created.")
                return redirect('reading_clubs')
            else:
                messages.error(request, form.errors)
                return redirect('create_reading_club')
        else:
            messages.error(request, form.errors)
            return redirect('create_reading_club')
    else:
        form = ReadingClubForm()
        return render(request, 'library/reading-clubs/create.html', {'form': form})


def reading_club(request, reading_club_id):
    reading_club_object = ReadingClub.objects.get(id=reading_club_id)
    if not reading_club_object:
        return redirect('reading_clubs')

    sessions = ReadingClubSession.objects.filter(reading_club=reading_club_object.id)
    return render(request, 'library/reading-clubs/show.html',
                  {'reading_club': reading_club_object, 'sessions': sessions})



@login_required
def create_reading_club_session(request, reading_club_id):
    if not request.user.is_staff:
        return reading_club(request, reading_club_id=reading_club_id)

    reading_club_object = ReadingClub.objects.get(id=reading_club_id)
    if not reading_club_object:
        return redirect('reading_clubs')

    if request.method == 'POST':
        form = ReadingClubSessionForm(request.POST)
        if form.is_valid():
            reading_club_session_object = form.save(commit=False)
            reading_club_session_object.reading_club = reading_club_object
            reading_club_session_object.save()
            if reading_club_session_object:
                messages.success(request, "Reading club session created.")
                return redirect('reading_club', reading_club_id=reading_club_id)
            else:
                messages.error(request, form.errors)
                return redirect('create_reading_club_session', reading_club_id=reading_club_id)
        else:
            messages.error(request, form.errors)
            return redirect('create_reading_club_session', reading_club_id=reading_club_id)

    else:
        form = ReadingClubSessionForm()
        return render(request, 'library/reading-clubs/sessions/create.html',
                      {'form': form, 'reading_club': reading_club_object})

@login_required
def join_reading_club_session(request, reading_club_id, reading_club_session_id):
    reading_club_object = ReadingClub.objects.get(id=reading_club_id)
    if not reading_club_object:
        return redirect('reading_clubs')

    reading_club_session_object = ReadingClubSession.objects.get(id=reading_club_session_id)
    if not reading_club_session_object:
        return redirect('reading_club', reading_club_id=reading_club_id)

    reading_club_session_object.users.add(request.user)
    reading_club_session_object.save()

    messages.success(request, "You have joined the reading club session.")
    return redirect('reading_club', reading_club_id=reading_club_id)


def leave_reading_club_session(request, reading_club_id, reading_club_session_id):
    reading_club_object = ReadingClub.objects.get(id=reading_club_id)
    if not reading_club_object:
        return redirect('reading_clubs')

    reading_club_session_object = ReadingClubSession.objects.get(id=reading_club_session_id)
    if not reading_club_session_object:
        return redirect('reading_club', reading_club_id=reading_club_id)

    reading_club_session_object.users.remove(request.user)
    reading_club_session_object.save()

    messages.success(request, "You have left the reading club session.")
    return redirect('reading_club', reading_club_id=reading_club_id)

