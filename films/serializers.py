from rest_framework import serializers
from .models import Film, Director

#2 [2] method fake serializator
#2 (ManyToMany)если хотим получить список то фейк сериализатор не моможет нужно написать свою функцию [3]
class DirectorSerializator(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio'.split()

class FilmListSerializers(serializers.ModelSerializer):
    director = DirectorSerializator(many=False)
    #3 когда он работает он ишет функцию get_genres
    genres = serializers.SerializerMethodField()
    #4 тут genre_list от функции в модельке
    class Meta:
        model = Film
        fields = 'id title rating release_year director genres genre_list reviews'.split()
        #1 method 
        depth = 1
    #3 тут он берет толко значение i.name 
    def get_genres(self, film):
        return [i.name for i in film.genres.all()]


class FilmDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'