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
    
    @classmethod
    def create_session_record(cls, pool, day, start_time, end_time, lanes):
        a = Session(pool = pool, day = day, lanes = lanes)
        a.start_time = (datetime.datetime.strptime(start_time,'%H.%M')).time()
        a.end_time = (datetime.datetime.strptime(end_time,'%H.%M')).time()
        db.put(a)
    
    
def make_table(day, pool, time=datetime.time(0)):
    q = Session.all().filter('day =', day).filter('pool =', pool).filter('end_time >',time).order('end_time')
    
    if Session.all().filter('day =', day).filter('pool =', pool).filter('end_time >',time).order('end_time').get():
        table = '<table>'
        for session in q:
            strstart_time = session.start_time.strftime('%H:%M').lstrip('0')
            strend_time = session.end_time.strftime('%H:%M').lstrip('0')
            timecell = "%s - %s" % (strstart_time, strend_time)
            table += '<tr><td>' + timecell + '</td><td>' + session.lanes + '</td></tr>'
        table += '</table>'
        return table
    else:
        return "<p>No more swimming here today, I'm afraid.</p>"
    
    
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
        today_London = make_table(today, 'London Fields Lido', earliest_end_time)
        
        template_values = {
            'now' : now,
            'today' : today,
            'today_Highbury' : today_Highbury,
            'today_Oasis_i' : today_Oasis_i,
            'today_Oasis_o' : today_Oasis_o,
            'today_London' : today_London
            }

        path = os.path.join(os.path.dirname(__file__),'where-can-i-swim-today.html')
        self.response.out.write(template.render(path, template_values))


class Tomorrow(webapp.RequestHandler):
    def get(self):
        dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        if datetime.datetime.weekday(datetime.date.today()) < 6:
            tomorrow = dayofWeek[datetime.datetime.weekday(datetime.date.today()) + 1]
        else:
            tomorrow = 'Monday'
        tomorrow_Highbury = make_table(tomorrow, 'Highbury Leisure Centre')
        tomorrow_Oasis_i = make_table(tomorrow, 'Oasis indoor')
        tomorrow_Oasis_o = make_table(tomorrow, 'Oasis outdoor')
        tomorrow_London = make_table(tomorrow, 'London Fields Lido')
       
        template_values = {
            'tomorrow' : tomorrow,
            'tomorrow_Highbury' : tomorrow_Highbury,
            'tomorrow_Oasis_i' : tomorrow_Oasis_i,
            'tomorrow_Oasis_o' : tomorrow_Oasis_o,
            'tomorrow_London' : tomorrow_London
            }

        path = os.path.join(os.path.dirname(__file__),'where-can-i-swim-tomorrow.html')
        self.response.out.write(template.render(path, template_values))
        
class gimmedata(webapp.RequestHandler):
    def get(self): 
        Session.create_session_record('London Fields Lido', 'Monday', '6.30', '9.30',  'With lanes')
        Session.create_session_record('London Fields Lido', 'Monday', '9.30', '18.30',  'May be lanes')
        Session.create_session_record('London Fields Lido', 'Monday', '18.30', '19.30',  'With lanes')
        Session.create_session_record('London Fields Lido', 'Tuesday', '6.30', '9.30',  'With lanes')
        Session.create_session_record('London Fields Lido', 'Tuesday', '9.30', '18.30',  'May be lanes')
        Session.create_session_record('London Fields Lido', 'Wednesday', '6.30', '19.30',  'With lanes')
        Session.create_session_record('London Fields Lido', 'Thursday', '9.30', '19.30',  'With lanes')
        Session.create_session_record('London Fields Lido', 'Friday', '6.30', '19.30',  'With lanes')
        Session.create_session_record('London Fields Lido', 'Saturday', '8.00', '10.00',  'With lanes')
        Session.create_session_record('London Fields Lido', 'Saturday', '10.00', '17.00',  'May be lanes')
        Session.create_session_record('London Fields Lido', 'Sunday', '8.00', '10.00',  'With lanes')
        Session.create_session_record('London Fields Lido', 'Sunday', '10.00', '17.00',  'May be lanes')   
        Session.create_session_record('Oasis indoor', 'Monday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Monday', '11.30', '12.00',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Monday', '12.00', '14.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Monday', '14.00', '15.30',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Monday', '16.30', '18.30',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Monday', '18.30', '19.30',  'May be lanes')
        Session.create_session_record('Oasis outdoor', 'Monday', '6.30', '21.30',  'May be lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Monday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Monday', '12.00', '13.30',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Monday', '4.30', '5.00',  'Limited lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Monday', '18.00', '22.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Tuesday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Tuesday', '9.30', '12.00',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Tuesday', '12.00', '14.00',  'With lanes')
        Session.create_session_record('Oasis outdoor', 'Tuesday', '6.30', '21.30',  'May be lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Tuesday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Tuesday', '12.00', '13.30',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Tuesday', '18.00', '19.30',  'Limited lanes')
        Session.create_session_record('Oasis indoor', 'Wednesday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Wednesday', '9.00', '12.00',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Wednesday', '12.00', '14.30',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Wednesday', '17.30', '18.30',  'May be lanes')
        Session.create_session_record('Oasis outdoor', 'Wednesday', '6.30', '21.30',  'May be lanes')        
        Session.create_session_record('Highbury Leisure Centre', 'Wednesday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Wednesday', '12.00', '13.30',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Wednesday', '15.30', '16.30',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Wednesday', '16.30', '17.00',  'Limited lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Wednesday', '17.00', '18.00',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Wednesday', '18.00', '21.00',  'Limited lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Wednesday', '21.00', '22.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Thursday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Thursday', '9.00', '9.45',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Thursday', '11.30', '12.00',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Thursday', '12.00', '14.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Thursday', '15.00', '16.00',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Thursday', '17.00', '19.00',  'May be lanes')
        Session.create_session_record('Oasis outdoor', 'Thursday', '6.30', '21.30',  'May be lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Thursday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Thursday', '12.00', '13.30',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Thursday', '18.00', '19.30',  'Limited lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Thursday', '19.30', '22.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Friday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Friday', '9.00', '11.00',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Friday', '12.00', '14.00',  'With lanes')
        Session.create_session_record('Oasis indoor', 'Friday', '15.00', '16.00',  'May be lanes')
        Session.create_session_record('Oasis outdoor', 'Friday', '6.30', '21.30',  'May be lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Friday', '6.30', '9.00',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Friday', '12.00', '13.30',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Friday', '18.45', '20.00',  'Limited lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Friday', '20.00', '22.00', 'With lanes')
        Session.create_session_record('Oasis indoor', 'Saturday', '9.30', '15.30',  'May be lanes')
        Session.create_session_record('Oasis indoor', 'Saturday', '16.30', '17.00',  'May be lanes')
        Session.create_session_record('Oasis outdoor', 'Saturday', '9.30', '17.00',  'May be lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Saturday', '7.30', '10.00',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Saturday', '11.30', '12.00',  'Limited lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Saturday', '13.30', '19.30',  'Limited lanes')
        Session.create_session_record('Oasis indoor', 'Sunday', '9.30', '17.00',  'May be lanes')
        Session.create_session_record('Oasis outdoor', 'Sunday', '9.30', '17.00',  'May be lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Sunday', '7.30', '10.00',  'With lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Sunday', '10.00', '18.00',  'Limited lanes')
        Session.create_session_record('Highbury Leisure Centre', 'Sunday', '18.00', '22.00',  'With lanes')
        self.redirect('/')




application = webapp.WSGIApplication(
                                     [('/', Today),
                                     ('/tomorrow', Tomorrow),
                                     ('/gimmedata', gimmedata)],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()


datetime.datetime.weekday(datetime.date.today())