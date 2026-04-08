from django.db import models

class Director(models.Model):
    fio = models.CharField(max_length=100)
    birthday = models.DateField()

    def __str__(self):
        return self.fio


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Film(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(null=True, blank=True)
    release_year = models.IntegerField()
    rating = models.FloatField()
    is_hit = models.BooleanField(default=True)
    created = models. DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    director = models.ForeignKey(Director, on_delete=models.CASCADE, null=True)
    genres = models.ManyToManyField(Genre, blank=True)


    def __str__(self):
        return self.title
    
    #4 method написать функцию в модельке
    def genre_list(self):
        return [i.name for i in self.genres.all()]

    
class Review(models.Model):
    text = models.TextField()
    # 1:10
    stars = models.IntegerField(choices=((i,i) for i in range(1,11)), default=5)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return self.text