from google.appengine.ext import ndb

from heroes import fields
from heroes.models import Base
from heroes.teams.models import Team
from heroes.events.models import Event

class Representative(Base):
    name = ndb.StringProperty(required=True)
    role = ndb.StringProperty(required=True)
    events = ndb.KeyProperty(kind="Event", repeated=True)
    teams = ndb.KeyProperty(kind="Team", repeated=True)

    def add_team(self, team):
        self.teams.append(team.key)
        self.put()

    def add_event(self, event):
        self.events.append(event.key)
        self.put()

    def __repr__(self):
        return u'{}: {}'.format(self.name,
                                self.role)

    @property
    def link(self):
        return '/representatives/{}/'.format(self.key.urlsafe())

    # this is where Admin CRUD form lives
    class Meta:
        def __init__(self):
            from ndbadmin.admin import fields as admin_fields
            self.fields = [
                admin_fields.TextField("name", "Name", required=False),
                admin_fields.KeyField("team", "Team", required=True, query=Team.query()),
                admin_fields.KeyField("event", "Event", required=True, query=Event.query()),
                admin_fields.ChoiceField("role", "Role", initial=['Player', 'Captain', 'Coach'],
                                        query=['Player', 'Captain', 'Coach'])
            ]

    FIELDS = {
        'name': fields.String,
        'role': fields.String,
        'event': fields.Key,
        'team': fields.Key,
    }
    FIELDS.update(Base.FIELDS)
