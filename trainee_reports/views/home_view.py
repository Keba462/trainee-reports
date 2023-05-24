from django.apps import apps as django_apps
from django.views.generic.base import TemplateView

from edc_base.view_mixins import EdcBaseViewMixin
from edc_navbar import NavbarViewMixin
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from edc_constants.constants import MALE, FEMALE


class HomeView(NavbarViewMixin, EdcBaseViewMixin, TemplateView):
    template_name = 'trainee_reports/home.html'
    navbar_selected_item = 'Enrollments Reports'
    navbar_name = 'trainee_reports'

    subject_screening_model = 'trainee_subject.subjectscreening'
    subject_consent_model = 'trainee_subject.subjectconsent'
    


    @property
    def subject_screening_cls(self):
        return django_apps.get_model(self.subject_screening_model)

    @property
    def subject_consent_cls(self):
        return django_apps.get_model(self.subject_consent_model)
    

    @property
    def enrollment_timeseries_statistics(self):
        """Time series data from the first consent

        Returns:
            list: Data calculate from 2020, up-to-date
        """
        current_year = datetime.now()
        months = []
        initial_date = self.subject_consent_cls.objects.latest('-report_datetime').report_datetime.date()
        
        while True:
            
            if initial_date.year == current_year.year and initial_date.month == current_year.month:
                break
            
            months.append(initial_date)
            initial_date += relativedelta(months=1)
        
        enrollment_data = list()
        
        
        
        for date in months:
            consents_count = self.subject_consent_cls.objects.filter(
                report_datetime__year=date.year, report_datetime__month=date.month).count()
            
            date_year = date.year
            date_month = date.month
            
            enrollment_data.append(
                (f"{date_year}-{date_month}",  consents_count),
            )
        
        return enrollment_data
    
    @property
    def enrollment_timeseries_statistics_by_gender(self):
        """Time series data from the first consent

        Returns:
            list: Data calculate from 2020, up-to-date
        """
        current_year = datetime.now()
        months = []
        initial_date = self.subject_consent_cls.objects.latest('-report_datetime').report_datetime.date()
        
        while True:
            
            if initial_date.year == current_year.year and initial_date.month == current_year.month:
                break
            
            months.append(initial_date)
            initial_date += relativedelta(months=1)
        
        enrollment_dates = list()
        gender_statistics = list()
        
        
        for date in months:
            female_consents_count = self.subject_consent_cls.objects.filter(
                report_datetime__year=date.year, report_datetime__month=date.month, gender=FEMALE).count()
            
            male_consents_count = self.subject_consent_cls.objects.filter(
                report_datetime__year=date.year, report_datetime__month=date.month, gender=MALE).count()
            
            date_year = date.year
            date_month = date.month
            
            enrollment_dates.append(
                f"{date_year}-{date_month}"
            )
            gender_statistics.append(
                (female_consents_count, male_consents_count)
            )
            
            
        
        return (enrollment_dates, gender_statistics)
            

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        screened_subjects = self.subject_screening_cls.objects.all().count()
        consented_subjects = self.subject_consent_cls.objects.all().count()
        enrolled_subjects = self.subject_consent_cls.objects.all().count()
        not_enrolled_subjects = self.subject_screening_cls.objects.filter(is_eligible=False).count()
        
        enrollments = [
            ['Screening',screened_subjects],
            ['Consented',consented_subjects],
            ['Not Enrolled',not_enrolled_subjects],
            ['Enrolled',enrolled_subjects],
        ]
    

        context.update(
            screened_subjects=screened_subjects,
            consented_subjects=consented_subjects,
            not_enrolled_subjects=not_enrolled_subjects,
            enrolled_subjects=enrolled_subjects,
            
            enrollments=enrollments,
            enrollment_timeseries_statistics = self.enrollment_timeseries_statistics,
            enrollment_timeseries_statistics_by_gender=self.enrollment_timeseries_statistics_by_gender
            
            
        )

        return context
