from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        account = self.model(
            email=AccountManager.normalize_email(email)
        )

        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        account = self.create_user(email,
            password=password
        )
        account.is_admin = True
        account.save(using=self._db)
        return account

class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_absolute_url(self):
        return "/accounts/%s/" % urlquote(self.email)

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Author(models.Model):
    account = models.OneToOneField(Account, verbose_name=_('account'))
    name = models.CharField(_('name'), max_length=30, blank=True)
    main_image = models.OneToOneField('common.Image', null=True, blank=True, related_name='+', verbose_name=_('main image'))

    def __unicode__(self): return self.name
