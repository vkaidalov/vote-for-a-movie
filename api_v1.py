from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(
    blueprint,
    title="Vote for a Movie",
    version="0.1.0",
    description="A REST API for the \"Vote for a Movie\" app."
)
