import os
import datetime
import logging
from google.appengine.ext.webapp import template
import webapp2
from google.appengine.ext import db

import databank

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
        
    @classmethod
    def make_all_tables(cls, day, time):
        pools = [session.pool for session in Session.all()]
        return {pool[:4]: cls.make_table(day, pool, time) for pool in pools}
        

class Day(webapp2.RequestHandler):
    def get(self, urlday):
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 
            'Saturday', 'Sunday']
        earliest_end_time = datetime.time(0)
        today = Day.correct_for_dst(datetime.datetime.today())
        
        if urlday == 'today' or urlday == '':
            day_str = day_of_week[today.weekday()]
            html_page = 'today.html'
            earliest_end_time = (today + datetime.timedelta(hours=1)).time()
        elif urlday == 'tomorrow':
            day_str = day_of_week[(today.weekday()+1)%7]
            html_page = 'tomorrow.html'
        else:
            day_str = urlday
            html_page = 'day.html'
        
        template_values = Session.make_all_tables(day_str, earliest_end_time)
        template_values['day'] = day_str
        template_values['previous'] = day_of_week[(
            day_of_week.index(day_str)-1)%7]
        template_values['next'] = day_of_week[(day_of_week.index(day_str)+1)%7]
        
        logging.info(template_values)
        
        path = os.path.join(os.path.dirname(__file__), html_page)
        self.response.out.write(template.render(path, template_values))
    
    @staticmethod
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
            return today + datetime.timedelta(hour=1)
        else:
            return today

       
class gimmedata(webapp2.RequestHandler):
    def get(self):
        for lane in databank.lanes:
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


application = webapp2.WSGIApplication([('/gimmedata', gimmedata),
                                     (r'/(.*)', Day)
                                      ],
                                     debug=True)