from rest_framework.decorators import api_view  # POST GET 
from rest_framework.response import Response   # return Response
from rest_framework import status
from .models import Film
from .serializers import FilmListSerializers, FilmDetailSerializers


@api_view(['GET'])
def film_detail_api_view(request, id):
    try:
        film = Film.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = FilmDetailSerializers(film, many=False).data
    return Response(data=data)



@api_view(['GET'])
def film_list_api_view(request):
    #1 collect all films
    films = Film.objects.select_related('director').prefetch_related('reviews', 'genres').all()
    #2 serialiozer data
    list_film = FilmListSerializers(films, many=True).data # .data-превращает это в наши данные
    #3 return response
    return Response(data=list_film, status=status.HTTP_200_OK)
