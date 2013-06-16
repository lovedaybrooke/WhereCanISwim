import os
import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import db
import webapp2

from WhereCanISwim import *
import databank


class updateSessions(webapp2.RequestHandler):
    def get(self):
        for session in Session.all():
            session.delete()

        for session in databank.sessions:
            try:
                if not session.get("details"):
                    session["details"] = ''
                Session.create_session_record(**session)
            except:
                logging.info("Couldn't create: {0}, {1}, {2}, {3}".format(
                    session["pool"], session["day"], session["start"],
                    session["end"]))
        self.redirect('/')


application = webapp2.WSGIApplication([('/update-sessions', updateSessions)],
                                     debug=True)