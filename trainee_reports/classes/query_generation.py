from django.apps import apps as django_apps
from django.conf import settings
from edc_appointment.constants import NEW_APPT
from edc_constants.constants import OPEN
from django.db.models import Q

class QueryGeneration:
    
    screening_eligibility_model = 'trainee_subject.subjectscreening'
    consent_model = 'trainee_subject.subjectconsent'
    subject_visit_model = 'trainee_subject.subjectvisit'



    @property
    def consent_model_cls(self):
        return django_apps.get_model(self.consent_model)

    @property
    def screening_eligibility_cls(self):
        return django_apps.get_model(self.screening_eligibility_model)
    
    @property
    def subject_visit_cls(self):
        return django_apps.get_model(self.subject_visit_model)
    

    @property
    def query_name_cls(self):
        return django_apps.get_model('edc_data_manager.queryname')

    @property
    def action_item_cls(self):
        return django_apps.get_model('edc_data_manager.dataactionitem')
    
    @property
    def site_id(self):
        return settings.SITE_ID

    def create_query_name(self, query_name=None):
        obj, created = self.query_name_cls.objects.get_or_create(query_name=query_name)
        return obj
    

    def create_action_item(
            self, site=None, subject_identifier=None, query_name=None,
            assign=None, status=OPEN, subject=None, comment=None):
        defaults = {
            'assigned': assign,
            'status': status,
            'subject': subject,
            'comment': comment,
            'site': site
        }
        obj, created = self.action_item_cls.objects.update_or_create(
            subject_identifier=subject_identifier,
            query_name=query_name,
            defaults=defaults
        )
        return obj
    
    @property
    def site_issue_assign_opts(self):
        options = {
            40: 'gabs_clinic',
            41: 'maun_clinic',
            42: 'serowe_clinic',
            43: 'gheto_clinic',
            44: 'sphikwe_clinic',
        }
        return options



    def check_appt_status(self, required_crf=None):
        appointment_model_cls = django_apps.get_model(
            required_crf.schedule.appointment_model)
        try:
            appt = appointment_model_cls.objects.get(
                subject_identifier=required_crf.subject_identifier,
                visit_code=required_crf.visit_code,
                visit_code_sequence=required_crf.visit_code_sequence,
                schedule_name=required_crf.schedule_name)
        except appointment_model_cls.DoesNotExist:
            return False
        else:
            return False if appt.appt_status == NEW_APPT else True
        
    
    def check_missing_screening(self):
        subject = 'Missing Screenings',
        comment =('The data for the missing screenings needs to be recaptured')
        query_name = "Missing Screenings"
        self.create_query_name(query_name)
        missing_screenings = self.consent_model_cls.objects.filter(screening_identifier__isnull=True)
        if missing_screenings.exists():
            for miss in missing_screenings:
              assign = self.site_issue_assign_opts(40)
              self.create_action_item( 
                #f"Missing screenings found: {missing_screenings.count()}",
                subject_identifier=miss.subject_identifier,
                site=miss.site,
                query_name=query_name,
                assign=assign,
                subject=subject,
                comment=comment,
                )




    def check_incomplete_visits(self):
        
        subject = 'Incomplete Visits',
        comment =('The visits need to be completed and marked as complete')
        query_name = "Incomplete Visits"
        query = self.create_query_name(query_name)

        """
        1. for each visit query appointment where status is completed
        2. for thos visits check if there exists a crf meta data object with entry status on REQUIRED
        3. if crfmetadata query returns objects then create data action item saying there are incomplete vists

        """

        """
        query all the visits
        for each visits get the coresponding appointment
        if appointment is complete 
        and the crf meta data for that visit is on required create an action item saying the crf is missing for this participant
        """
        crfmetadata = django_apps.get_model('edc_metadata.crfmetadata')
        visits = self.subject_visit_cls.objects.filter(appointment__appt_status='Done')
        for visit in visits:
            required_crfs = crfmetadata.objects.filter(
            subject_identifier=visit.subject_identifier,
            visit_code=visit.visit_code,
            entry_status='REQUIRED')
            if required_crfs.exists():
                for required in required_crfs:
                    assign = self.site_issue_assign_opts(40)
                    self.create_action_item(
                        #f"Incomplete visits found: {incomplete_visits.count()}",
                        subject_identifier=required.subject_identifier,
                        site=required.site,
                        query_name=query.query_name,
                        assign=assign,
                        subject=subject,
                        comment=comment
                        )

    """def check_eligible_participants(self):
        subject = 'Eligible participants',
        comment =('The data for candidates who are eligible  needs to be recaptured')
        query_name = "Eligible Participants"
        query=self.create_query_name(query_name)
        eligible_participants = self.consent_model_cls.objects.filter(eligibility=True)
    
        if eligible_participants.exists():
            for eligible in eligible_participants:
                
                assign = self.site_issue_assign_opts(40)
                self.create_action_item(
                    #f"Eligible participants found: {eligible_participants.count()}",
                    subject_identifier=eligible.subject_identifier,
                    site=40,
                    query_name=query.query_name,
                    assign=assign,
                    subject=subject,
                    comment=comment
                    )
            """