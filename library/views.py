from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from library.forms import ReadingClubForm, ReadingClubSessionForm
from library.models import ReadingClub, ReadingClubSession



def index(request):
    return render(request, 'library/index.html')

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