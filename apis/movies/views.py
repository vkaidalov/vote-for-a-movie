from flask_restplus import Namespace, Resource, fields
from mongoengine import ValidationError
from flask import request

from .models import Movie

api = Namespace("movies", description="Movies related operations.")

movie_fields = api.model("Movie", {
    "id": fields.String(readonly=True),
    "title": fields.String(required=True),
    "releaseDate": fields.Date(attribute="release_date"),
    "actors": fields.List(fields.String(required=True)),
    "genres": fields.List(fields.String(required=True)),
    "sumOfMarks": fields.Integer(readonly=True, attribute="sum_of_marks"),
    "numberOfMarks": fields.Integer(readonly=True, attribute="number_of_marks")
})

mark_data_fields = api.model("Mark Data", {
    "mark": fields.Integer(required=True, min=1, max=100, example=75)
})

movie_action_fields = api.model("Movie Action", {
    "type": fields.String(required=True, example="rate"),
    "data": fields.Nested(mark_data_fields, required=True)
})


def create_or_update_movie_with_payload(movie_id=None):
    if movie_id is not None:
        movie = Movie.objects.get_or_404(id=movie_id)
    else:
        movie = Movie()

    movie.title = api.payload.get("title", movie.title)
    movie.release_date = api.payload.get("releaseDate", movie.release_date)
    movie.actors = api.payload.get("actors", movie.actors)
    movie.genres = api.payload.get("genres", movie.genres)

    try:
        movie.save()
    except ValidationError as error:
        api.abort(
            400, "Input payload validation failed",
            errors=error.to_dict()
        )

    return movie


@api.route("/")
class MovieList(Resource):
    @api.marshal_list_with(movie_fields)
    def get(self):
        kwargs = {}
        actors = request.args.getlist("actor")
        genres = request.args.getlist("genre")
        title_contains = request.args.get("title_contains")
        if actors:
            kwargs["actors__in"] = actors
        if genres:
            kwargs["genres__in"] = genres
        if title_contains:
            kwargs["title__icontains"] = title_contains
        return list(Movie.objects(**kwargs))

    @api.expect(movie_fields, validate=True)
    @api.marshal_with(movie_fields, 201)
    def post(self):
        return create_or_update_movie_with_payload(), 201


@api.route("/<movie_id>")
class MovieDetail(Resource):
    @api.marshal_with(movie_fields)
    def get(self, movie_id):
        return Movie.objects.get_or_404(id=movie_id)

    @api.response(204, "Movie patched")
    @api.expect(movie_fields, validate=False)
    def patch(self, movie_id):
        create_or_update_movie_with_payload(movie_id)
        return "", 204

    @api.response(204, "Movie deleted")
    def delete(self, movie_id):
        Movie.objects.get_or_404(id=movie_id).delete()
        return "", 204


@api.route("/<movie_id>/actions/")
class MovieActionList(Resource):
    @api.expect(movie_action_fields, validate=True)
    def post(self, movie_id):
        action_data = api.payload["data"]

        if movie_action["type"] != "rate":
            api.abort(400, "Action type not supported.")

        movie = Movie.objects.get_or_404(id=movie_id)

        movie.rate(mark=action_data["mark"])

        return {"message": "Action performed."}, 201
