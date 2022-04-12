from django.test import TestCase

from .healcheck import HealChecker

class FukuViewTest(TestCase):
    def test_fuku(self,**kwargs):
        # self.assertEqual(FukuView.get_json(), None)
        result = HealChecker()
        result.get_json()
        response_json = result.render_to_response_json()
        some_database_is_not_working = "working" not in response_json.values()
        if some_database_is_not_working:
            print("some_database_is_not_working")
        print(response_json)
        expexcted_result = {
                            'Cache backend: default':           'working', 
                            'CeleryHealthCheckCelery':          'working', 
                            'CeleryPingHealthCheck':            'working', 
                            'DatabaseBackend':                  'working', 
                            'DefaultFileStorageHealthCheck':    'working', 
                            'MigrationsHealthCheck':            'working', 
                            'RedisHealthCheck':                 'working'
                            }
        self.assertEqual(response_json, expexcted_result)
        