from django.conf import settings

from edc_navbar import NavbarItem, site_navbars, Navbar

trainee_reports = Navbar(name='trainee_reports')

no_url_namespace = True if settings.APP_NAME == 'trainee_reports' else False

trainee_reports.append_item(
    NavbarItem(name='Enrollments Reports',
               label='Enrollments Reports',
               fa_icon='fa-cogs',
               url_name='trainee_reports:home_url'))


site_navbars.register(trainee_reports)
