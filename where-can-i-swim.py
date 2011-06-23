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
        
class gimmedata(webapp.RequestHandler):
    def get(self): 
        a1 = Session(pool = 'Oasis indoor', day = 'Monday')
        a1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        a1.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        a1.lanes = 'With lanes'
        db.put(a1)
        
        b1 = Session(pool = 'Oasis indoor', day = 'Monday')
        b1.start_time = (datetime.datetime.strptime('11.30','%H.%M')).time()
        b1.end_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        b1.lanes = 'May be lanes'
        db.put(b1)
        
        c1 = Session(pool = 'Oasis indoor', day = 'Monday')
        c1.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        c1.end_time = (datetime.datetime.strptime('14.00','%H.%M')).time()
        c1.lanes = 'With lanes'
        db.put(c1)
        
        d1 = Session(pool = 'Oasis indoor', day = 'Monday')
        d1.start_time = (datetime.datetime.strptime('14.00','%H.%M')).time()
        d1.end_time = (datetime.datetime.strptime('15.30','%H.%M')).time()
        d1.lanes = 'May be lanes'
        db.put(d1)
        
        e1 = Session(pool = 'Oasis indoor', day = 'Monday')
        e1.start_time = (datetime.datetime.strptime('16.30','%H.%M')).time()
        e1.end_time = (datetime.datetime.strptime('18.30','%H.%M')).time()
        e1.lanes = 'May be lanes'
        db.put(e1)
        
        f1 = Session(pool = 'Oasis indoor', day = 'Monday')
        f1.start_time = (datetime.datetime.strptime('18.30','%H.%M')).time()
        f1.end_time = (datetime.datetime.strptime('19.30','%H.%M')).time()
        f1.lanes = 'May be lanes'
        db.put(f1)
        
        g1 = Session(pool = 'Oasis outdoor', day = 'Monday')
        g1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        g1.end_time = (datetime.datetime.strptime('21.30','%H.%M')).time()
        g1.lanes = 'May be lanes'
        db.put(g1)
        
        h1 = Session(pool = 'Highbury Leisure Centre', day = 'Monday')
        h1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        h1.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        h1.lanes = 'With lanes'
        db.put(h1)
        
        i1 = Session(pool = 'Highbury Leisure Centre', day = 'Monday')
        i1.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        i1.end_time = (datetime.datetime.strptime('13.30','%H.%M')).time()
        i1.lanes = 'With lanes'
        db.put(i1)
        
        j1 = Session(pool = 'Highbury Leisure Centre', day = 'Monday')
        j1.start_time = (datetime.datetime.strptime('4.30','%H.%M')).time()
        j1.end_time = (datetime.datetime.strptime('5.00','%H.%M')).time()
        j1.lanes = 'Limited lanes'
        db.put(j1)
        
        k1 = Session(pool = 'Highbury Leisure Centre', day = 'Monday')
        k1.start_time = (datetime.datetime.strptime('18.00','%H.%M')).time()
        k1.end_time = (datetime.datetime.strptime('22.00','%H.%M')).time()
        k1.lanes = 'With lanes'
        db.put(k1)
        
        l1 = Session(pool = 'Oasis indoor', day = 'Tuesday')
        l1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        l1.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        l1.lanes = 'With lanes'
        db.put(l1)
        
        m1 = Session(pool = 'Oasis indoor', day = 'Tuesday')
        m1.start_time = (datetime.datetime.strptime('9.30','%H.%M')).time()
        m1.end_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        m1.lanes = 'May be lanes'
        db.put(m1)
        
        n1 = Session(pool = 'Oasis indoor', day = 'Tuesday')
        n1.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        n1.end_time = (datetime.datetime.strptime('14.00','%H.%M')).time()
        n1.lanes = 'With lanes'
        db.put(n1)
        
        o1 = Session(pool = 'Oasis outdoor', day = 'Tuesday')
        o1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        o1.end_time = (datetime.datetime.strptime('21.30','%H.%M')).time()
        o1.lanes = 'May be lanes'
        db.put(o1)
        
        p1 = Session(pool = 'Highbury Leisure Centre', day = 'Tuesday')
        p1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        p1.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        p1.lanes = 'With lanes'
        db.put(p1)
        
        q1 = Session(pool = 'Highbury Leisure Centre', day = 'Tuesday')
        q1.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        q1.end_time = (datetime.datetime.strptime('13.30','%H.%M')).time()
        q1.lanes = 'With lanes'
        db.put(q1)
        
        r1 = Session(pool = 'Highbury Leisure Centre', day = 'Tuesday')
        r1.start_time = (datetime.datetime.strptime('18.00','%H.%M')).time()
        r1.end_time = (datetime.datetime.strptime('19.30','%H.%M')).time()
        r1.lanes = 'Limited lanes'
        db.put(r1)
        
        s1 = Session(pool = 'Oasis indoor', day = 'Wednesday')
        s1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        s1.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        s1.lanes = 'With lanes'
        db.put(s1)
        
        t1 = Session(pool = 'Oasis indoor', day = 'Wednesday')
        t1.start_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        t1.end_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        t1.lanes = 'May be lanes'
        db.put(t1)
        
        u1 = Session(pool = 'Oasis indoor', day = 'Wednesday')
        u1.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        u1.end_time = (datetime.datetime.strptime('14.30','%H.%M')).time()
        u1.lanes = 'With lanes'
        db.put(u1)
        
        v1 = Session(pool = 'Oasis indoor', day = 'Wednesday')
        v1.start_time = (datetime.datetime.strptime('17.30','%H.%M')).time()
        v1.end_time = (datetime.datetime.strptime('18.30','%H.%M')).time()
        v1.lanes = 'May be lanes'
        db.put(v1)
        
        w1 = Session(pool = 'Oasis outdoor', day = 'Wednesday')
        w1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        w1.end_time = (datetime.datetime.strptime('21.30','%H.%M')).time()
        w1.lanes = 'May be lanes'
        db.put(w1)
                
        x1 = Session(pool = 'Highbury Leisure Centre', day = 'Wednesday')
        x1.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        x1.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        x1.lanes = 'With lanes'
        db.put(x1)
        
        y1 = Session(pool = 'Highbury Leisure Centre', day = 'Wednesday')
        y1.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        y1.end_time = (datetime.datetime.strptime('13.30','%H.%M')).time()
        y1.lanes = 'With lanes'
        db.put(y1)
        
        z1 = Session(pool = 'Highbury Leisure Centre', day = 'Wednesday')
        z1.start_time = (datetime.datetime.strptime('15.30','%H.%M')).time()
        z1.end_time = (datetime.datetime.strptime('16.30','%H.%M')).time()
        z1.lanes = 'With lanes'
        db.put(z1)
        
        a2 = Session(pool = 'Highbury Leisure Centre', day = 'Wednesday')
        a2.start_time = (datetime.datetime.strptime('16.30','%H.%M')).time()
        a2.end_time = (datetime.datetime.strptime('17.00','%H.%M')).time()
        a2.lanes = 'Limited lanes'
        db.put(a2)
        
        b2 = Session(pool = 'Highbury Leisure Centre', day = 'Wednesday')
        b2.start_time = (datetime.datetime.strptime('17.00','%H.%M')).time()
        b2.end_time = (datetime.datetime.strptime('18.00','%H.%M')).time()
        b2.lanes = 'With lanes'
        db.put(b2)
        
        c2 = Session(pool = 'Highbury Leisure Centre', day = 'Wednesday')
        c2.start_time = (datetime.datetime.strptime('18.00','%H.%M')).time()
        c2.end_time = (datetime.datetime.strptime('21.00','%H.%M')).time()
        c2.lanes = 'Limited lanes'
        db.put(c2)
        
        d2 = Session(pool = 'Highbury Leisure Centre', day = 'Wednesday')
        d2.start_time = (datetime.datetime.strptime('21.00','%H.%M')).time()
        d2.end_time = (datetime.datetime.strptime('22.00','%H.%M')).time()
        d2.lanes = 'With lanes'
        db.put(d2)
        
        e2 = Session(pool = 'Oasis indoor', day = 'Thursday')
        e2.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        e2.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        e2.lanes = 'With lanes'
        db.put(e2)
        
        f2 = Session(pool = 'Oasis indoor', day = 'Thursday')
        f2.start_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        f2.end_time = (datetime.datetime.strptime('9.45','%H.%M')).time()
        f2.lanes = 'May be lanes'
        db.put(f2)
        
        g2 = Session(pool = 'Oasis indoor', day = 'Thursday')
        g2.start_time = (datetime.datetime.strptime('11.30','%H.%M')).time()
        g2.end_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        g2.lanes = 'May be lanes'
        db.put(g2)
        
        h2 = Session(pool = 'Oasis indoor', day = 'Thursday')
        h2.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        h2.end_time = (datetime.datetime.strptime('14.00','%H.%M')).time()
        h2.lanes = 'With lanes'
        db.put(h2)
        
        i2 = Session(pool = 'Oasis indoor', day = 'Thursday')
        i2.start_time = (datetime.datetime.strptime('15.00','%H.%M')).time()
        i2.end_time = (datetime.datetime.strptime('16.00','%H.%M')).time()
        i2.lanes = 'May be lanes'
        db.put(i2)
        
        j2 = Session(pool = 'Oasis indoor', day = 'Thursday')
        j2.start_time = (datetime.datetime.strptime('17.00','%H.%M')).time()
        j2.end_time = (datetime.datetime.strptime('19.00','%H.%M')).time()
        j2.lanes = 'May be lanes'
        db.put(j2)
        
        k2 = Session(pool = 'Oasis outdoor', day = 'Thursday')
        k2.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        k2.end_time = (datetime.datetime.strptime('21.30','%H.%M')).time()
        k2.lanes = 'May be lanes'
        db.put(k2)
        
        l2 = Session(pool = 'Highbury Leisure Centre', day = 'Thursday')
        l2.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        l2.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        l2.lanes = 'With lanes'
        db.put(l2)
        
        m2 = Session(pool = 'Highbury Leisure Centre', day = 'Thursday')
        m2.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        m2.end_time = (datetime.datetime.strptime('13.30','%H.%M')).time()
        m2.lanes = 'With lanes'
        db.put(m2)
        
        n2 = Session(pool = 'Highbury Leisure Centre', day = 'Thursday')
        n2.start_time = (datetime.datetime.strptime('18.00','%H.%M')).time()
        n2.end_time = (datetime.datetime.strptime('19.30','%H.%M')).time()
        n2.lanes = 'Limited lanes'
        db.put(n2)
        
        o2 = Session(pool = 'Highbury Leisure Centre', day = 'Thursday')
        o2.start_time = (datetime.datetime.strptime('19.30','%H.%M')).time()
        o2.end_time = (datetime.datetime.strptime('22.00','%H.%M')).time()
        o2.lanes = 'With lanes'
        db.put(o2)
        
        p2 = Session(pool = 'Oasis indoor', day = 'Friday')
        p2.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        p2.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        p2.lanes = 'With lanes'
        db.put(p2)
        
        q2 = Session(pool = 'Oasis indoor', day = 'Friday')
        q2.start_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        q2.end_time = (datetime.datetime.strptime('11.00','%H.%M')).time()
        q2.lanes = 'May be lanes'
        db.put(q2)
        
        r2 = Session(pool = 'Oasis indoor', day = 'Friday')
        r2.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        r2.end_time = (datetime.datetime.strptime('14.00','%H.%M')).time()
        r2.lanes = 'With lanes'
        db.put(r2)
        
        s2 = Session(pool = 'Oasis indoor', day = 'Friday')
        s2.start_time = (datetime.datetime.strptime('15.00','%H.%M')).time()
        s2.end_time = (datetime.datetime.strptime('16.00','%H.%M')).time()
        s2.lanes = 'May be lanes'
        db.put(s2)
        
        t2 = Session(pool = 'Oasis outdoor', day = 'Friday')
        t2.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        t2.end_time = (datetime.datetime.strptime('21.30','%H.%M')).time()
        t2.lanes = 'May be lanes'
        db.put(t2)
        
        u2 = Session(pool = 'Highbury Leisure Centre', day = 'Friday')
        u2.start_time = (datetime.datetime.strptime('6.30','%H.%M')).time()
        u2.end_time = (datetime.datetime.strptime('9.00','%H.%M')).time()
        u2.lanes = 'With lanes'
        db.put(u2)
        
        v2 = Session(pool = 'Highbury Leisure Centre', day = 'Friday')
        v2.start_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        v2.end_time = (datetime.datetime.strptime('13.30','%H.%M')).time()
        v2.lanes = 'With lanes'
        db.put(v2)
        
        w2 = Session(pool = 'Highbury Leisure Centre', day = 'Friday')
        w2.start_time = (datetime.datetime.strptime('18.45','%H.%M')).time()
        w2.end_time = (datetime.datetime.strptime('20.00','%H.%M')).time()
        w2.lanes = 'Limited lanes'
        db.put(w2)
        
        x2 = Session(pool = 'Highbury Leisure Centre', day = 'Friday')
        x2.start_time = (datetime.datetime.strptime('20.00','%H.%M')).time()
        x2.end_time = (datetime.datetime.strptime('22.00','%H.%M')).time()
        x2.lanes = 'With lanes'
        db.put(x2)
        
        y2 = Session(pool = 'Oasis indoor', day = 'Saturday')
        y2.start_time = (datetime.datetime.strptime('9.30','%H.%M')).time()
        y2.end_time = (datetime.datetime.strptime('15.30','%H.%M')).time()
        y2.lanes = 'May be lanes'
        db.put(y2)
        
        z2 = Session(pool = 'Oasis indoor', day = 'Saturday')
        z2.start_time = (datetime.datetime.strptime('16.30','%H.%M')).time()
        z2.end_time = (datetime.datetime.strptime('17.00','%H.%M')).time()
        z2.lanes = 'May be lanes'
        db.put(z2)
        
        a3 = Session(pool = 'Oasis outdoor', day = 'Saturday')
        a3.start_time = (datetime.datetime.strptime('9.30','%H.%M')).time()
        a3.end_time = (datetime.datetime.strptime('17.00','%H.%M')).time()
        a3.lanes = 'May be lanes'
        db.put(a3)
        
        b3 = Session(pool = 'Highbury Leisure Centre', day = 'Saturday')
        b3.start_time = (datetime.datetime.strptime('7.30','%H.%M')).time()
        b3.end_time = (datetime.datetime.strptime('10.00','%H.%M')).time()
        b3.lanes = 'With lanes'
        db.put(b3)
        
        c3 = Session(pool = 'Highbury Leisure Centre', day = 'Saturday')
        c3.start_time = (datetime.datetime.strptime('11.30','%H.%M')).time()
        c3.end_time = (datetime.datetime.strptime('12.00','%H.%M')).time()
        c3.lanes = 'Limited lanes'
        db.put(c3)
        
        d3 = Session(pool = 'Highbury Leisure Centre', day = 'Saturday')
        d3.start_time = (datetime.datetime.strptime('13.30','%H.%M')).time()
        d3.end_time = (datetime.datetime.strptime('19.30','%H.%M')).time()
        d3.lanes = 'Limited lanes'
        db.put(d3)
        
        e3 = Session(pool = 'Oasis indoor', day = 'Sunday')
        e3.start_time = (datetime.datetime.strptime('9.30','%H.%M')).time()
        e3.end_time = (datetime.datetime.strptime('17.00','%H.%M')).time()
        e3.lanes = 'May be lanes'
        db.put(e3)
        
        f3 = Session(pool = 'Oasis outdoor', day = 'Sunday')
        f3.start_time = (datetime.datetime.strptime('9.30','%H.%M')).time()
        f3.end_time = (datetime.datetime.strptime('17.00','%H.%M')).time()
        f3.lanes = 'May be lanes'
        db.put(f3)
        
        g3 = Session(pool = 'Highbury Leisure Centre', day = 'Sunday')
        g3.start_time = (datetime.datetime.strptime('7.30','%H.%M')).time()
        g3.end_time = (datetime.datetime.strptime('10.00','%H.%M')).time()
        g3.lanes = 'With lanes'
        db.put(g3)
        
        h3 = Session(pool = 'Highbury Leisure Centre', day = 'Sunday')
        h3.start_time = (datetime.datetime.strptime('10.00','%H.%M')).time()
        h3.end_time = (datetime.datetime.strptime('18.00','%H.%M')).time()
        h3.lanes = 'Limited lanes'
        db.put(h3)
        
        i3 = Session(pool = 'Highbury Leisure Centre', day = 'Sunday')
        i3.start_time = (datetime.datetime.strptime('18.00','%H.%M')).time()
        i3.end_time = (datetime.datetime.strptime('22.00','%H.%M')).time()
        i3.lanes = 'With lanes'
        db.put(i3)
        
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