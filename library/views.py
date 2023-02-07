from django.shortcuts import render
from django.http import HttpResponse

from library.forms import ReadingClubForm


# Create your views.py here.

def index(request):
    return render(request, 'library/index.html')

def reading_clubs(request):
    return render(request, 'library/reading-clubs/index.html')

def create_reading_club(request):
    if not request.user.is_staff:
        return index(request)

    if request.method == 'POST':
        form = ReadingClubForm(request.POST)
        if form.is_valid():
            # Create reading club and insert into database
            reading_club = form.save()
            return HttpResponse('Reading club created')

        else:
            return HttpResponse('Reading club not created')
    else:
        form = ReadingClubForm()
        return render(request, 'library/reading-clubs/create.html', {'form': form})