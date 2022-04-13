# signals imports
from django.core.mail import EmailMessage
from django.dispatch import receiver
from django.db.models.signals import (
        post_save,
)
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.checks.messages import Error

from django.contrib.auth.tokens import default_token_generator

from app.settings import EMAIL_HOST_USER


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Email address is required')

        if not username:
            raise ValueError('User name is required')

        # Tạo đối tượng user mới
        user = self.model(
            email=self.normalize_email(email=email),  # Chuyển email về dạng bình thường
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email=email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class NomalUser(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'  # Trường quyêt định khi login
    REQUIRED_FIELDS = ['username', 'first_name',
                       'last_name']  # Các trường yêu cầu khi đk tài khoản (mặc định đã có email), mặc định có password

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin  # Admin có tất cả quyền trong hệ thống

    def has_module_perms(self, add_label):
        return True

    def full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

@receiver(post_save, sender=NomalUser)
def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    """
    after saved in the database
    """
    current_site = Site.objects.get_current()
    if created:
        print("Send email to", instance.email)
        mail_subject = 'Activate your Aram Account'
        text_message = render_to_string('user/active_email.html', {
            'user': instance,
            'current_site' : current_site,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
            'token': default_token_generator.make_token(instance),
        })
        message = EmailMessage(mail_subject, text_message, EMAIL_HOST_USER, [instance.email])
        message.send()
    else:
        print(instance.email, "was just saved")
