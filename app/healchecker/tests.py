from django.test import TestCase

from health_check.mixins import CheckMixin

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

class FukuView(CheckMixin):

    @method_decorator(never_cache)
    def get_json(self):
        rep = self.run_check()
        print(rep)

    def render_to_response_json(self):
        return {str(p.identifier()): str(p.pretty_status()) for p in self.plugins}
            

class FukuViewTest(TestCase):
    def test_fuku(self,**kwargs):
        # self.assertEqual(FukuView.get_json(), None)
        result = FukuView()
        result.run_check()
        render_to_response_json = result.render_to_response_json()
        some_database_is_not_working = "working" not in render_to_response_json.values()
        if some_database_is_not_working:
            print("some_database_is_not_working")
        print(render_to_response_json)
        self.assertEqual(result, None)