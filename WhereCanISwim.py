import os
import datetime

from google.appengine.ext.webapp import template
from google.appengine.ext import db
import webapp2


class Session(db.Model):
    pool = db.StringProperty()
    day = db.StringProperty()
    start_time = db.TimeProperty()
    end_time = db.TimeProperty()
    details = db.StringProperty()

    @classmethod
    def create_session_record(cls, pool, day, start, end, details):
        a = Session(pool=pool, day=day, details=details)
        a.start_time = (datetime.datetime.strptime(start, '%H.%M')).time()
        a.end_time = (datetime.datetime.strptime(end, '%H.%M')).time()
        db.put(a)

    @classmethod
    def here_now_sessions(cls, day, pool, time):
        return Session.all().filter('day =', day).filter(
            'pool =', pool).filter('end_time >', time).order('end_time').fetch(
            100)

    @classmethod
    def get_all_session_data(cls, day, time):
        session_data = {}
 
        pools = [session.pool for session in Session.all()]

        for pool in pools:
            pool_sessions = cls.here_now_sessions(day, pool, time)
            shortname = pool[:4]
            # If there are sessions still going on this day at this pool, add
            # them into a dictionary to be used by the template
            if pool_sessions:
                session_data[shortname] = [] 
                for ps in pool_sessions:
                    session_time = "{0} - {1}".format(
                        ps.start_time.strftime('%H:%M').lstrip('0'), 
                        ps.end_time.strftime('%H:%M').lstrip('0'))
                    session_data[shortname].append({'time': session_time,
                        'details': ps.details})

            # If no sessions are available for this pool, on this day, at this
            # time, then stick in a marker to represent this.
            else:
                session_data[shortname] = 'ended'
        return session_data


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
            day_str = day_of_week[(today.weekday() + 1) % 7]
            html_page = 'tomorrow.html'
        else:
            day_str = urlday
            html_page = 'day.html'

        template_values = Session.get_all_session_data(day_str,
            earliest_end_time)
        template_values['day'] = day_str
        template_values['previous'] = day_of_week[(
            day_of_week.index(day_str) - 1) % 7]
        template_values['next'] = day_of_week[(
            day_of_week.index(day_str) + 1) % 7]

        path = os.path.join(os.path.dirname(__file__), html_page)
        self.response.out.write(template.render(path, template_values))

    @staticmethod
    def correct_for_dst(today):
        clock_switches = {
            2013: {
                "spring": datetime.datetime(2013, 03, 31, 1),
                "autumn": datetime.datetime(2013, 10, 27, 2)
                },
            2014: {
                "spring": datetime.datetime(2014, 03, 30, 1),
                "autumn": datetime.datetime(2014, 10, 26, 2)
                },
            2015: {
                "spring": datetime.datetime(2015, 03, 29, 1),
                "autumn": datetime.datetime(2015, 10, 25, 2)
                },
            2016: {
                "spring": datetime.datetime(2015, 03, 27, 1),
                "autumn": datetime.datetime(2015, 10, 30, 2)
                }
            }
        this_year = today.year

        in_daylight_savings_time = (
            today >= clock_switches[this_year]["spring"] and 
            today <= clock_switches[this_year]["autumn"])

        if in_daylight_savings_time:
            return today + datetime.timedelta(hours=1)
        else:
            return today


application = webapp2.WSGIApplication([(r'/(.*)', Day)],
                                     debug=True)
