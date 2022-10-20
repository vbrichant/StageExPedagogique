import calendar
from datetime import date, timedelta
import datetime
from django.utils.safestring import mark_safe
from django.views import generic

from formation.model.SessionFormation import SessionFormation
from formation.utils import Calendar


class CalendarView(generic.ListView):
    model = SessionFormation
    template_name = 'formation/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        calendar_object = Calendar()
        html_calendar = calendar_object.formatmonth(theyear=d.year, themonth=d.month, withyear=True)
        context['calendar'] = mark_safe(html_calendar)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def prev_month(d):
    first = d.replace(day=1)
    previous_month_object = first - timedelta(days=1)
    month = 'month=' + str(previous_month_object.year) + '-' + str(previous_month_object.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month_object = last + timedelta(days=1)
    month = 'month=' + str(next_month_object.year) + '-' + str(next_month_object.month)
    return month


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.date.today()
