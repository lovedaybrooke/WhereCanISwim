import datetime
import os
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Session(db.Model):
    pool = db.StringProperty()
    day = db.StringProperty()
    start_time = db.DateTimeProperty()
    end_time = db.DateTimeProperty()
    lanes = db.StringProperty()
    
    
def make_table(today, pool):
    q = Session.all().filter('day =', today).filter('pool =', pool).order('start_time')
    
    table = '<table>'
    for session in q:
        strstart_time = session.start_time.strftime('%H:%M').lstrip('0')
        strend_time = session.end_time.strftime('%H:%M').lstrip('0')
        timecell = "%s - %s" % (strstart_time, strend_time)
        table += '<tr><td>' + timecell + '</td><td>' + session.lanes + '</td></tr>'
    table += '</table>'
    return table


class Today(webapp.RequestHandler):
    def get(self):
        dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        today = dayofWeek[datetime.datetime.weekday(datetime.date.today())]
        today_Highbury = make_table(today, 'Highbury Leisure Centre')
        today_Oasis_i = make_table(today, 'Oasis indoor')
        today_Oasis_o = make_table(today, 'Oasis outdoor')

        template_values = {
            'today' : today,
            'today_Highbury' : today_Highbury,
            'today_Oasis_i' : today_Oasis_i,
            'today_Oasis_o' : today_Oasis_o
            }

        path = os.path.join(os.path.dirname(__file__),'where-can-i-swim-today.html')
        self.response.out.write(template.render(path, template_values))


class Tomorrow(webapp.RequestHandler):
    def get(self):
        dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        tomorrow = dayofWeek[datetime.datetime.weekday(datetime.date.today()) + 1]
        tomorrow_Highbury = make_table(tomorrow, 'Highbury Leisure Centre')
        tomorrow_Oasis_i = make_table(tomorrow, 'Oasis indoor')
        tomorrow_Oasis_o = make_table(tomorrow, 'Oasis outdoor') 
       
        template_values = {
            'tomorrow' : tomorrow,
            'tomorrow_Highbury' : tomorrow_Highbury,
            'tomorrow_Oasis_i' : tomorrow_Oasis_i,
            'tomorrow_Oasis_o' : tomorrow_Oasis_o
            }

        path = os.path.join(os.path.dirname(__file__),'where-can-i-swim-tomorrow.html')
        self.response.out.write(template.render(path, template_values))


application = webapp.WSGIApplication(
                                     [('/', Today),
                                     ('/tomorrow', Tomorrow)],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()


datetime.datetime.weekday(datetime.date.today())