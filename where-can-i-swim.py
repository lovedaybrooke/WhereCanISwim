import datetime
import os
import sys
for k in [k for k in sys.modules if k.startswith('django')]: 
    del sys.modules[k] 
from google.appengine.dist import use_library
use_library('django', '1.2')
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class Session(db.Model):
    pool = db.StringProperty()
    day = db.StringProperty()
    start_time = db.TimeProperty()
    end_time = db.TimeProperty()
    lanes = db.StringProperty()    
    
def make_table(day, pool, time=datetime.time(0)):
    q = Session.all().filter('day =', day).filter('pool =', pool).filter('end_time >',time).order('end_time')
    
    table = '<table>'
    for session in q:
        strstart_time = session.start_time.strftime('%H:%M').lstrip('0')
        strend_time = session.end_time.strftime('%H:%M').lstrip('0')
        timecell = "%s - %s" % (strstart_time, strend_time)
        table += '<tr><td>' + timecell + '</td><td>' + session.lanes + '</td></tr>'
    table += '</table>'
    return table
    
def correct_for_dst(today):
	spring2011 = datetime.datetime(2011,03,27,1,0)
	autumn2011 = datetime.datetime(2011,10,30,2,0)
	spring2012 = datetime.datetime(2012,03,25,1,0)
	autumn2011 = datetime.datetime(2012,10,28,2,0)
	spring2013 = datetime.datetime(2013,03,31,1,0)
	autumn2013 = datetime.datetime(2013,10,27,2,0)
	spring2014 = datetime.datetime(2014,03,30,1,0)
	autumn2014 = datetime.datetime(2014,10,26,2,0)
	spring2015 = datetime.datetime(2015,03,29,1,0)
	autumn2015 = datetime.datetime(2015,10,25,2,0)
	if today >= spring2011 and today <= autumn2011:
		return today + datetime.timedelta(0,3600)
	else:
		return today


class Today(webapp.RequestHandler):
    def get(self):
        todaynow = correct_for_dst(datetime.datetime.today())
        
        dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        today = dayofWeek[datetime.datetime.weekday(todaynow)]
        
        now = todaynow.time()
        earliest_end_time = (todaynow + datetime.timedelta(0,3600)).time()

        today_Highbury = make_table(today, 'Highbury Leisure Centre', earliest_end_time)
        today_Oasis_i = make_table(today, 'Oasis indoor', earliest_end_time)
        today_Oasis_o = make_table(today, 'Oasis outdoor', earliest_end_time)
        
        template_values = {
            'now' : now,
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