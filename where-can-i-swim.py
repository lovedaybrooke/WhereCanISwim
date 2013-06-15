# coding=utf-8
import datetime
import os
import logging
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
    
    @classmethod
    def here_now_sessions(cls, day, pool, time):
        return Session.all().filter('day =', day).filter(
            'pool =', pool).filter('end_time >',time).order('end_time')
    
    @classmethod
    def make_table(cls, day, pool, time):
        if cls.here_now_sessions(day, pool, time).get():
            table = '<table>'
            for session in cls.here_now_sessions(day, pool, time):
                str_start_time = session.start_time.strftime(
                    '%H:%M').lstrip('0')
                str_end_time = session.end_time.strftime('%H:%M').lstrip('0')
                timecell = "%s - %s" % (str_start_time, str_end_time)
                table += '<tr><td>'
                table += timecell
                table += '</td><td>'
                table += session.lanes
                table += '</td></tr>'
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
    spring2016 = datetime.datetime(2015,03,27,1,0)
    autumn2016 = datetime.datetime(2015,10,30,2,0)
    if today >= spring2011 and today <= autumn2011:
        return today + datetime.timedelta(0,3600)
    else:
        return today


class Day(webapp.RequestHandler):
    def get(self, urlday):
        dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
            'Saturday', 'Sunday']
        earliest_end_time = datetime.time(0)
        day = urlday 
        
        if urlday == 'today' or urlday == '':
            todaynow = correct_for_dst(datetime.datetime.today())
            day = dayofWeek[datetime.datetime.weekday(todaynow)]
            now = todaynow.time()
            earliest_end_time = (todaynow + datetime.timedelta(hours=1)).time()
        elif urlday == 'tomorrow':
            if datetime.datetime.weekday(datetime.date.today()) < 6:
                day = dayofWeek[datetime.datetime.weekday(
                    datetime.date.today()) + 1]
            else:
                day = 'Monday'

        Mile = Session.make_table(day, "Mile End Pools", earliest_end_time)
        York = Session.make_table(day, 'York Hall Leisure Centre',
            earliest_end_time)
        London = Session.make_table(day, 'London Fields Lido',
            earliest_end_time)
        Iron = Session.make_table(day, 'Ironmonger Row', earliest_end_time)
        
        template_values = {
            'day' : day,
            'Mile': Mile,
            'Iron': Iron,
            'York': York,
            'London' : London
            }

        if urlday == 'today' or urlday == '':
            path = os.path.join(os.path.dirname(__file__),'today.html')
            self.response.out.write(template.render(path, template_values))
        elif urlday == 'tomorrow':
            path = os.path.join(os.path.dirname(__file__),'tomorrow.html')
            self.response.out.write(template.render(path, template_values))
        else:
            today_index = dayofWeek.index(day)
            template_values['previous'] = dayofWeek[(today_index-1)%7]
            template_values['next'] = dayofWeek[(today_index+1)%7]
            path = os.path.join(os.path.dirname(__file__),'day.html')
            self.response.out.write(template.render(path, template_values))

       
class gimmedata(webapp.RequestHandler):
    def get(self): 
        lanes = [
            {'pool': 'York Hall Leisure Centre', 'day': 'Monday', 
            'start': '7.00', 'end': '9.00'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Monday',
            'start': '9.00', 'end': '12.20', 'descrip': 'Shared with school'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Monday',
            'start': '12.20', 'end': '13.20', 'descrip': u'♀'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Monday',
            'start': '13.20', 'end':'20.30'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
            'start': '7.00', 'end': '9.00'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
            'start': '9.00', 'end': '12.30', 'descrip': 'Shared with school'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
            'start': '12.30', 'end': '13.30'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
            'start': '13.30', 'end':'15.30', 'descrip': 'Shared with school'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
            'start': '15.30', 'end':'17.30'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Wednesday',
            'start': '7.00', 'end': '9.00'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Wednesday',
            'start': '9.00', 'end': '12.20', 'descrip': 'Shared with school'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Wednesday',
            'start': '12.20', 'end': '13.20', 'descrip': u'♀'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Wednesday',
            'start': '13.30', 'end':'17.30'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
            'start': '7.00', 'end': '9.00'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
            'start': '9.00', 'end': '12.30', 'descrip': 'Shared with school'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
            'start': '12.30', 'end': '13.30'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
            'start': '13.30', 'end':'19.30', 'descrip': 'Shared with school'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
            'start': '19.30', 'end': '21.30'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
            'start': '7.00', 'end': '9.00'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
            'start': '9.00', 'end': '12.30', 'descrip': 'Shared with school'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
            'start': '12.30', 'end': '13.30'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
            'start': '13.30', 'end':'15.30', 'descrip': 'Shared with school'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
            'start': '15.30', 'end': '17.30'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Saturday',
            'start': '8.00', 'end': '12.00'},
            {'pool': 'York Hall Leisure Centre', 'day': 'Sunday',
            'start': '8.00', 'end': '15.30'},
            {'pool': 'Mile End Pools', 'day': 'Monday', 'start': '6.30',
            'end': '10.15'},
            {'pool': 'Mile End Pools', 'day': 'Monday', 'start': '10.15',
            'end': '12.15', 'descrip': u'♀'},
            {'pool': 'Mile End Pools', 'day': 'Monday', 'start': '12.15',
            'end': '22.00'},
            {'pool': 'Mile End Pools', 'day': 'Tuesday', 'start': '6.30',
            'end': '13.30'},
            {'pool': 'Mile End Pools', 'day': 'Tuesday', 'start': '13.30',
            'end': '15.30', 'descrip': u'♀'},
            {'pool': 'Mile End Pools', 'day': 'Tuesday', 'start': '15.30',
            'end': '22.00'},
            {'pool': 'Mile End Pools', 'day': 'Wednesday', 'start': '6.30',
            'end': '22.00'},
            {'pool': 'Mile End Pools', 'day': 'Thursday', 'start': '6.30',
            'end': '19.00'},
            {'pool': 'Mile End Pools', 'day': 'Thursday', 'start': '19.00',
            'end': '22.00', 'descrip': u'♀'},
            {'pool': 'Mile End Pools', 'day': 'Friday', 'start': '6.30',
            'end': '22.00'},
            {'pool': 'Mile End Pools', 'day': 'Saturday', 'start': '9.00',
            'end': '17.00'},
            {'pool': 'Mile End Pools', 'day': 'Sunday', 'start': '9.00',
            'end': '17.00'},
            {'pool': 'Ironmonger Row', 'day': 'Monday', 'start': '6.30',
            'end': '21.30'},
            {'pool': 'Ironmonger Row', 'day': 'Tuesday', 'start': '6.30',
            'end': '14.00'},
            {'pool': 'Ironmonger Row', 'day': 'Tuesday', 'start': '14.00',
            'end': '15.00', 'descrip': 'Shared with school'},
            {'pool': 'Ironmonger Row', 'day': 'Tuesday', 'start': '15.00',
            'end': '19.30'},
            {'pool': 'Ironmonger Row', 'day': 'Tuesday', 'start': '19.30',
            'end': '21.30', 'descrip': u'♀'},
            {'pool': 'Ironmonger Row', 'day': 'Wednesday', 'start': '6.30',
            'end': '21.30'},
            {'pool': 'Ironmonger Row', 'day': 'Thursday', 'start': '6.30',
            'end': '20.00'},
            {'pool': 'Ironmonger Row', 'day': 'Friday', 'start': '6.30',
            'end': '19.00'},
            {'pool': 'Ironmonger Row', 'day': 'Saturday', 'start': '9.00',
            'end': '10.00'},
            {'pool': 'Ironmonger Row', 'day': 'Saturday', 'start': '10.00',
            'end': '18.00', 'descrip': 'Shared with fun swim'},
            {'pool': 'Ironmonger Row', 'day': 'Sunday', 'start': '9.00',
            'end': '10.00'},
            {'pool': 'Ironmonger Row', 'day': 'Sunday', 'start': '10.00',
            'end': '18.00', 'descrip': 'Shared with fun swim'},
            {'pool': 'London Fields Lido', 'day': 'Monday', 'start': '6.30',
            'end': '20.00'},
            {'pool': 'London Fields Lido', 'day': 'Tuesday', 'start': '6.30',
            'end': '19.00'},
            {'pool': 'London Fields Lido', 'day': 'Tuesday', 'start': '19.00',
            'end': '20.00', 'descrip': u'♀'},
            {'pool': 'London Fields Lido', 'day': 'Wednesday', 'start': '6.30',
            'end': '19.00'},
            {'pool': 'London Fields Lido', 'day': 'Thursday', 'start': '6.30',
            'end': '20.00'},
            {'pool': 'London Fields Lido', 'day': 'Friday', 'start': '6.30',
            'end': '20.00'},
            {'pool': 'London Fields Lido', 'day': 'Saturday', 'start': '8.00',
            'end': '10.00'},
            {'pool': 'London Fields Lido', 'day': 'Saturday', 'start': '10.00',
            'end': '17.00', 'descrip': 'Shared with fun swim'},
            {'pool': 'London Fields Lido', 'day': 'Sunday', 'start': '8.00',
            'end': '10.00'},
            {'pool': 'London Fields Lido', 'day': 'Sunday', 'start': '10.00',
            'end': '17.00', 'descrip': 'Shared with fun swim'}
            ]
        for lane in lanes:
            try:
                if not lane.get("descrip"):
                    lane["descrip"] = ''
                Session.create_session_record(lane["pool"], lane["day"],
                    lane["start"], lane["end"], lane["descrip"])
            except:
                logging.info(lane["pool"] + ", " + lane["day"] + ", " +
                    lane["start"] + ", " + lane["end"] + ", " +
                    lane["descrip"])
        self.redirect('/')


application = webapp.WSGIApplication(
                                     [('/gimmedata', gimmedata),
                                     (r'/(.*)', Day)],
                                     debug=True)


def main():
    run_wsgi_app(application)


if __name__ == "__main__":
    main()


datetime.datetime.weekday(datetime.date.today())