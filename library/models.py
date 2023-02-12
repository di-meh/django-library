from django.contrib.auth.models import User
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        return self.name

class Editor(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a book editor (e.g. Hachette)')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateField()
    cover = models.ImageField(upload_to='covers/', blank=True)
    editor = models.ForeignKey(Editor, on_delete=models.SET_NULL, null=True)
    isbn = models.CharField(max_length=13)
    tags = ArrayField(models.CharField(max_length=100), blank=False, null=False, default=list)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    def __str__(self):
        return self.title

class Bookstore(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()
    books = models.ManyToManyField(Book, help_text='Select a book for this bookstore')

    def __str__(self):
        return self.name

class Exemplaires(models.Model):
    id_book = models.ForeignKey(Book, on_delete=models.CASCADE)
    id_bookstore = models.ForeignKey(Bookstore, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __int__(self):
        return self.quantity


class Emprunt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exemplaire = models.ForeignKey(Exemplaires, on_delete=models.CASCADE)
    date_emprunt = models.DateField()
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateField(null=True, blank=True)

class ReadingClub(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name

class ReadingClubSession(models.Model):
    date = models.DateTimeField()
    description = models.TextField()
    reading_club = models.ForeignKey(ReadingClub, on_delete=models.SET_NULL, null=True)
    users = models.ManyToManyField(User, help_text='Select a user for this session')

    def __str__(self):
        return self.date