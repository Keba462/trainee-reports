from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name ='trainee_reports'
    verbose_name = 'Trainee Reports'
    admin_site_name = 'trainee_reports_admin'
    extra_assignee_choices = ()
    assignable_users_group = 'assignable users'