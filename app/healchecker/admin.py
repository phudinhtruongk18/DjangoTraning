from django.urls import path
from django.contrib import admin
from django.db import models
from health_check.views import MainView
from django.contrib.auth.decorators import user_passes_test

class DummyModel(models.Model):
    class Meta:
        verbose_name = 'Heal Check Manually'

def check_admin(user):
   return user.is_superuser

@user_passes_test(check_admin)
def dummy_view(request):
    return MainView.as_view()(request)

@admin.register(DummyModel)
class DummyModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
                DummyModel._meta.app_label, DummyModel._meta.model_name)
        return [
            path('healcheck/', dummy_view, name=view_name)
        ]