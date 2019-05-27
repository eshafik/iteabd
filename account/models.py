from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.core.validators import RegexValidator


class Profile(models.Model):
    """User detail information model"""

    STATUS_CHOICES = ( 
        ('student', 'Student'), 
        ('employed', 'Employed'),
        ('unemployed', 'Unemployed'),
    )
    ITEA_STATUS = (
        ('member', 'General Member'),
        ('executive', 'Executive Member'),
        ('public', 'Public'),
    )
    BLOOD_GROUP = (
        ('a_positive', 'A+'),
        ('b_positive', 'B+'),
        ('0_positive', 'O+'),
        ('ab_positive', 'AB+'),
        ('a_negative', 'A-'),
        ('b_negative', 'B-'),
        ('o_negative', 'O-'),
        ('ab_negative', 'AB-'),

    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, 
                                on_delete=models.CASCADE)
    current_status = models.CharField(max_length=10,
                                      choices=STATUS_CHOICES,
                                      default='student') 
    joining_date = models.DateField(blank=True, null=True)
    status_details = models.TextField(blank=True, null=True)
    mobile_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                  message="Phone number must be entered in the format: '+8801'. Up to 15 digits allowed.")
    mobile = models.CharField(validators=[mobile_regex],
                              max_length=17, null=True,
                              blank=True) 
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/',
                              blank=True, null=True)
    current_address = models.TextField(blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    itea_status = models.CharField(max_length=20, choices=ITEA_STATUS,
                                   default='public')
    finance = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    father_name = models.TextField(max_length=250, blank=True)
    father_occupation = models.TextField(max_length=250, blank=True)
    father_mobile = models.CharField(validators=[mobile_regex],
                                     max_length=17, null=True,
                                     blank=True)
    mother_name = models.TextField(max_length=250, blank=True)
    mother_occupation = models.TextField(max_length=250, blank=True)
    mother_mobile = models.CharField(validators=[mobile_regex],
                                     max_length=17, null=True,
                                     blank=True)
    blood_group = models.CharField(max_length=20, choices=BLOOD_GROUP,
                                   default='o_positive')
    nid = models.CharField(validators=[mobile_regex], max_length=17,
                           null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('profile_details', args=[self.user.username])

    def is_executive(self):
        if str(self.itea_status) == 'executive':
            return True
        else:
            return False

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
