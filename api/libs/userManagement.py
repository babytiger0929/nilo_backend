from django.contrib.auth.models import BaseUserManager
from django.utils import timezone

import hashlib
from datetime import datetime


class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, email):
        case_insensitive_email_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_email_field: email})

    def create_user(self, email, password=None, **extra_fields):
        today = timezone.now()

        if not email:
            raise ValueError('Email is mandatory')

        email = CustomUserManager.normalize_email(email)

        if 'fullname' in extra_fields and extra_fields['fullname'] != '' and extra_fields['fullname'] is not None:
            fullname = extra_fields['fullname'].strip().upper()
        else:
            fullname = ''

        user = self.model(
            email=email,
            fullname=fullname,
            is_staff=True,
            is_active=True
        )
        p = hashlib.sha256()
        if password is None:
            p = hashlib.sha256()
            now = datetime.now()
            newPass = now.strftime("%m-%d-%Y %H:%M%p")
            p.update(newPass.encode('utf-8'))
            password = str(p.hexdigest()[:6])

        user.is_active = True
        user.activation_key = p.hexdigest()
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_admin = True
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


def set_password(user):
    p = hashlib.sha256()
    now = datetime.now()
    newPass = (now.strftime('%Y%m%d%H%M%S%f')).encode('utf-8')
    p.update(newPass)
    password = str(p.hexdigest()[:6])
    user.activation_key = p.hexdigest()
    user.set_password(password)
    user.save()
    return password


def set_hash_password(_string):
    p = hashlib.sha256()
    p.update(_string.encode('utf-8'))
    hash_password = str(p.hexdigest())
    return hash_password
