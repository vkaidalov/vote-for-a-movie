from datetime import datetime

from aniso8601 import parse_datetime
from aniso8601.exceptions import LeapSecondError
from bson.objectid import ObjectId
from flask_restplus import Namespace, Resource, fields
from mongoengine import ValidationError

from .models import Voting, Choice

api = Namespace("votings", description="Votings related operations.")

choice_fields = api.model("Choice", {
    "id": fields.String(readonly=True),
    "title": fields.String(required=True, max_length=128),
    "votes": fields.Integer(readonly=True)
})

voting_fields = api.model("Voting", {
    "id": fields.String(readonly=True),
    "choices": fields.List(fields.Nested(choice_fields), required=True),
    "currentVotes": fields.Integer(readonly=True, attribute="current_votes"),
    "maxVotes": fields.Integer(attribute="max_votes", min=1),
    "startDate": fields.DateTime(attribute="start_date"),
    "finishDate": fields.DateTime(attribute="finish_date")
})

choice_action_fields = api.model("Choice Action", {
    "type": fields.String(required=True, example="vote")
})


def _abort_with_validation_errors(errors):
    api.abort(
        400, "Input payload validation failed",
        errors=errors
    )


def _try_parse_datetime_field(field_name):
    dt_string = api.payload.get(field_name)

    if not dt_string:
        return None

    try:
        return parse_datetime(dt_string)
    except (ValueError, LeapSecondError):
        _abort_with_validation_errors(
            {field_name: f"Can't parse datetime {dt_string}"}
        )


@api.route("/")
class VotingList(Resource):
    @api.expect(voting_fields, validate=True)
    @api.marshal_with(voting_fields, code=201)
    def post(self):
        voting = Voting()

        for choice in api.payload.get("choices"):
            voting.choices.append(
                Choice(title=choice.get("title"))
            )

        voting.max_votes = api.payload.get("maxVotes")
        voting.start_date = _try_parse_datetime_field("startDate")
        voting.finish_date = _try_parse_datetime_field("finishDate")

        try:
            voting.save()
        except ValidationError as error:
            _abort_with_validation_errors(error.to_dict())

        return voting


@api.route("/<voting_id>")
class VotingDetail(Resource):
    @api.marshal_with(voting_fields)
    def get(self, voting_id):
        return Voting.objects.get_or_404(id=voting_id)


@api.route("/<voting_id>/choices/<choice_id>/actions/")
class ChoiceActionList(Resource):
    @api.expect(choice_action_fields, validate=True)
    def post(self, voting_id, choice_id):
        action_type = api.payload.get("type")

        if action_type != "vote":
            api.abort(400, "Action type not supported.")

        voting = Voting.objects.get_or_404(id=voting_id)

        current_date = datetime.utcnow()

        if voting.start_date and current_date < voting.start_date:
            api.abort(403, "Voting isn't started yet.")

        if voting.finish_date and current_date > voting.finish_date:
            api.abort(403, "Voting is finished.")

        if voting.max_votes and voting.current_votes == voting.max_votes:
            api.abort(403, "Maximum number of votes is reached.")

        choice_object_id = ObjectId(choice_id)
        for choice in voting.choices:
            if choice.id == choice_object_id:
                choice.votes += 1
                voting.current_votes += 1

                voting.save()

                return "", 204

        api.abort(404, "Choice with specified ID not found.")
