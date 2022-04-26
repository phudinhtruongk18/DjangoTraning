from typing import NoReturn
from health_check.mixins import CheckMixin

from mail.worker import mailing_healchecl

class HealChecker(CheckMixin):

    def render_to_response_json(self):
        return {str(p.identifier()): str(p.pretty_status()) for p in self.plugins}
            
def heal_check_pro() -> NoReturn:
    result = HealChecker()
    result.run_check()
    if result.errors:
        print("some_database_is_not_working", result.errors)
        # send mail here
        mailing_healchecl(result.plugins)
    else:
        print("working fine. Error:", result.errors)
    # return here
    
