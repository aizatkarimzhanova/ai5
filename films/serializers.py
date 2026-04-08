from rest_framework import serializers
from .models import Film

class FilmListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = 'id title rating release_year'.split()


class FilmDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'