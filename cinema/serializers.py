from rest_framework import serializers
from cinema.models import Movie, Actor, Genre, CinemaHall


class ActorSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    last_name = serializers.CharField(max_length=255, required=True)
    first_name = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        return Actor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.save()
        return instance


class GenreSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class CinemaHallSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)
    rows = serializers.IntegerField(min_value=1)
    seats_in_row = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        return CinemaHall.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.rows = validated_data.get("rows", instance.rows)
        instance.seats_in_row = validated_data.get(
            "seats_in_row", instance.seats_in_row
        )
        instance.save()
        return instance


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    duration = serializers.IntegerField()
    actors = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Actor.objects.all()
    )
    genres = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Genre.objects.all()
    )
    duration = serializers.IntegerField(min_value=1)

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)
        actors = validated_data.pop("actors")
        genres = validated_data.pop("genres")
        movie = Movie.objects.create(**validated_data)
        movie.actors.set(actors)
        movie.genres.set(genres)
        return movie

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.duration = validated_data.get("duration", instance.duration)

        instance.duration = validated_data.get(
            "duration", instance.duration
        )
        instance.save()

        if "actors" in validated_data:
            instance.actors.set(validated_data["actors"])
        if "genres" in validated_data:
            instance.genres.set(validated_data["genres"])
            return instance
