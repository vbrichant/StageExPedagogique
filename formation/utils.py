from datetime import datetime
from calendar import HTMLCalendar
from .models import SessionFormation


class Calendar(HTMLCalendar):
    def __int__(self, year=None, month=None):
        self.year = datetime.today().year
        self.month = datetime.today().month
        super(Calendar, self).__init__()

    def formatday(self, day, session):
        session_per_day = session.filter(date__day=day)
        d = ''
        for session in session_per_day:
            d += f"<li> {session.formation.name} </li>"
            # d += f"<li><a href='{% url 'formation:session_detail' session.id %}'> {session.formation.name} </a></li>"

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul class='days_list'> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek: list, session):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, session)
        return f'<tr> {week} </tr>'

    def formatmonth(self, theyear, themonth, withyear=True):
        session = SessionFormation.objects.filter(date__year=theyear, date__month=themonth)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(theyear, themonth, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(theyear, themonth):
            cal += f'{self.formatweek(theweek=week, session=session)}\n'
        return cal
