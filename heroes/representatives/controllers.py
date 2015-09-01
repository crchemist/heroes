from flask import Blueprint, session, jsonify

from google.appengine.ext import ndb

from flask_restful import Api, url_for, marshal_with, reqparse

from heroes.helpers import Api, Resource, make_response, admin_required

from heroes.teams.models import Team
from .models import Representative

representatives_bp = Blueprint('representatives', __name__)
representatives_api = Api(representatives_bp)



@representatives_api.resource('/')
class RepresentativeListView(Resource):

    def get(self):
        representative_dbs = Representative.get_dbs()
        return make_response(representative_dbs, Representative.FIELDS)


    @admin_required
    def post(self):
        parser = self._make_parser(('name', {'required': True}),
                                   ('team', {'required': True}),
                                   ('event', {'required': True}),
                                   ('role', {'required': True}))


        args = parser.parse_args()
        representative = Representative(name=args.get('name'),
                                        role=args.get('role'))
        representative.add_team(args.get('team', ''))
        representative.add_event(args.get('event', ''))
        representative.put()
        return make_response(representative, Representative.FIELDS)


@representatives_api.resource('/<int:representative_id>/')
class RepresentativeView(Resource):

    def get(self, representative_id):
        representative = Representative.get_by_id(representative_id)
        return make_response(representative, Representative.FIELDS)


    @admin_required
    def put(self, representative_id):
        parser = self._make_parser(('name', {'required': True}),
                                   ('teams', {'required': True}),
                                   ('events', {'required': True}),
                                   ('role', {'required': True}))
                                   
        args = parser.parse_args()

        representative = Representative.get_by_id(representative_id)
        representative.name = args.get('name')
        representative.role = args.get('role')
        representative.put()
        return make_response(representative, Representative.FIELDS)


    @admin_required
    def delete(self, representative_id):
        representative = Representative.get_by_id(event_id)
        representative.key.delete()
