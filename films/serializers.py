from rest_framework import serializers
from .models import Film, Director, Genre
from rest_framework.exceptions import ValidationError

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'



#2 [2] method fake serializator
#2 (ManyToMany)если хотим получить список то фейк сериализатор не моможет нужно написать свою функцию [3]
class DirectorSerializator(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio'.split()

class DirectorCreateSerializator(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = 'id fio birthday'.split()


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

# тут не пишем моделсер-р потому что там много функции, сейчас нам нужно только валидейт
class FilmValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=255) #обезательный false=необезательный
    text = serializers.CharField(required=False)
    release_year = serializers.IntegerField()
    rating = serializers.FloatField(min_value=1, max_value=10)
    is_hit = serializers.BooleanField(default=True)
    director_id = serializers.IntegerField()
    genres = serializers.ListField(child=serializers.IntegerField(min_value=1)) 
    # genres принимает только целые числа



    # def validate(self, attrs):
    #     director_id = attrs['director_id']
    #     try:
    #         Director.objects.get(id=director_id)
    #     except Director.DoesNotExist:
    #         raise ValidationError('Director does not exist')
    #     return attrs
    
    def validate_director_id(self, director_id):
        try:
            Director.objects.get(id=director_id)
        except Director.DoesNotExist:
            raise ValidationError('Director does not exist')
        return director_id
    
    def validate_genres(selg, genres):
        genres_from_db = Genre.objects.filter(id__in=genres) #фильтрует данные по списку 
        if len(genres) != len(genres_from_db):
            raise ValidationError('Genre does not exist!')
        return genres