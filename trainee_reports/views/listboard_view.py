
from django_pandas.io import read_frame
from edc_constants.constants import CLOSED, OPEN
from edc_data_manager.views.listboard_view import ListBoardView as EdcDataManagerListBoardView
#from edc_data_manager import QueryName

class ListBoardView(EdcDataManagerListBoardView):

    listboard_template = 'trainee_reports/data_reports'
    listboard_url = 'data_manager_listboard_url'

    @property
    def query_summary(self):
        """Return a summary of quesries
        """
        data = []
        qs_categories = QueryName.objects.values_list('query_name', flat=True)
        qs_categories = list(set(qs_categories))
        active_queries = DataActionItem.objects.filter(
            status__in=['resolved', 'stalled', OPEN])
        for query_name in qs_categories:
            qs = active_queries.filter(query_name=query_name)
            data.append([
                query_name, qs.count()])
            #breakpoint()
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        open_action_items = DataActionItem.objects.filter(
            status=OPEN, site_id=self.site_id)
        stalled_action_items = DataActionItem.objects.filter(
            status='stalled', site_id=self.site_id)
        resolved_action_items = DataActionItem.objects.filter(
            status='resolved', site_id=self.site_id)
        closed_action_items = DataActionItem.objects.filter(
            status=CLOSED, site_id=self.site_id)
        #breakpoint()
        context.update(
            resolved_last_week=self.resolved_last_week,
            closed_last_week=self.closed_last_week,
            query_summary=self.query_summary,
            export_add_url=self.model_cls().get_absolute_url(),
            open_action_items=open_action_items.count(),
            stalled_action_items=stalled_action_items.count(),
            resolved_action_items=resolved_action_items.count(),
            closed_action_items=closed_action_items.count(),
            query_names=self.get_query_names)
        return context


    def extra_search_options(self, search_term):
        q = Q()
        if re.match('^[A-Z]+$', search_term):
            q = Q(first_name__exact=search_term)
        return q

    @property
    def get_query_names(self):
        query_names = QueryName.objects.values_list('query_name',flat=True).distinct()
        return query_names


