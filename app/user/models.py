# signals imports
from __future__ import absolute_import, unicode_literals
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from app.my_celery import send_mai_to_kid
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.dispatch import receiver

from .my_signal import user_signup

from django.db.models.signals import (
        post_save,
        pre_save
)


# Create your models here.
class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None, first_name="", last_name="",is_from_google=False,*something,**extra_fields):
        
        if not email:
            raise ValueError('Email address is required')

        if not username:
            raise ValueError('User name is required')

        is_active = False
        
        if is_from_google:
            is_active = True

        # Tạo đối tượng user mới
        user = self.model(
            email=self.normalize_email(email=email),  # Chuyển email về dạng bình thường
            username=username,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_active=is_active,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        # print("User created")
        user_signup.send(sender=self.__class__, instance=user, email=email, first_name=first_name, last_name=last_name)
        # print("Signal sent")

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
    phone_number = models.CharField(max_length=50)

    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=False)

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

    # def is_authenticated(self):
        # return True

@receiver(user_signup, sender=NomalUser)
def user_signup_receiver(sender, instance, *args, **kwargs):
    # DEBUG HERE
    if instance.social_auth.exists():
        instance.is_active = True


@receiver(user_signup, sender=MyAccountManager)
def user_signup_receiver(sender, instance, *args, **kwargs):
    """
    after saved in the database
    """

    # print("user_post_save_receiver")
    # print(sender)
    # print(instance)
    # print(args)
    # print(kwargs)

    uid = urlsafe_base64_encode(force_bytes(instance.pk))
    current_site = Site.objects.get_current()
    token = default_token_generator.make_token(instance)
    email = instance.email
    send_mai_to_kid.delay(
                    current_site=str(current_site), 
                    email=email,
                    domain=str(current_site.domain),
                    uid=uid,
                    token=token
                    )
