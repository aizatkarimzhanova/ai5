from django.db import transaction
from rest_framework.decorators import api_view  # POST GET 
from rest_framework.response import Response   # return Response
from rest_framework import status
from .models import Film
from .serializers import FilmListSerializers, FilmDetailSerializers, FilmValidateSerializer


@api_view(['GET', 'PUT', 'DELETE'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        data = FilmDetailSerializers(film, many=False).data
        return Response(data=data)
    
    elif request.method == 'DELETE':
        film.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method == 'PUT':
        film.title = request.data.get('title')
        film.text = request.data.get('text')
        film.release_year = request.data.get('release_year')
        film.rating = request.data.get('rating')
        film.is_hit = request.data.get('is_hit')
        film.director_id = request.data.get('director_id')
        film.genres.set(request.data.get('genres'))
        film.save()
        return Response(status=status.HTTP_201_CREATED,
                        data=FilmDetailSerializers(film).data)



@api_view(['GET', 'POST'])
def film_list_api_view(request):

    if request.method == 'GET':    
        #1 collect all films
        films = Film.objects.select_related('director').prefetch_related('reviews', 'genres').all()
        #2 serialiozer data
        list_film = FilmListSerializers(films, many=True).data # .data-превращает это в наши данные
        #3 return response
        return Response(data=list_film, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        # 0 validation(existing(существует ли), typing(типы данных), extra)
        serializer = FilmValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors) # тут получаем ошибки
        
        # тут уже берем проверенных данных(FilmValidateSerializer)
        # 1 recive data-получить данных
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        release_year = serializer.validated_data.get('release_year')
        rating = serializer.validated_data.get('rating')
        is_hit = serializer.validated_data.get('is_hit')
        director_id = serializer.validated_data.get('director_id')
        genres = serializer.validated_data.get('genres')
        # 2 create film
        # параметр - значение
        # transaction.atomic - если какой то из данных будет неправильно то объект не создастса
        with transaction.atomic():
            film = Film.objects.create(
                title=title,
                text=text,
                release_year=release_year,
                rating=rating,
                is_hit=is_hit,
                director_id=director_id
            )
            film.genres.set(genres)
            film.save()
        # 3 return response
        return Response(status=status.HTTP_201_CREATED,data=FilmDetailSerializers(film).data)
        #почему здес дата у говорить что мы отдаем какую ту часть данных но почему
        #во могих случеав клиент спросить айди(data={'id':film.id}),
        #в редких случаях отдается все данные(data=FilmDetailSerializers(film).data)