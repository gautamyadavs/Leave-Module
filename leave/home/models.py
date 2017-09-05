from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

LEAVE_TYPE = (
    ('casual', 'Casual Leave'),
    ('vacation', 'Vacation Leave'),
    ('commuted', 'Commuted Leave'),
    ('special_casual', 'Special Casual Leave'),
    ('restricted', 'Restricted Holiday'),
    ('earned', 'Earned Leave'),
)

PROCESSING_BY = (
    ('Head CSE', 'Head CSE'),
    ('Head ECE', 'Head ECE'),
    ('Head ME', 'Head ME'),
    ('Head NS', 'Head NS'),
    ('Head Design', 'Head Design'),
    ('Director', 'Director')
)

APPLICATION_STATUSES = (
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('processing', 'Being Processed')
)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    pf = models.IntegerField(default=0)
    name = models.CharField(max_length=200, default='')
    designation = models.CharField(max_length=100, default='', null=True, blank=True)
    section = models.CharField(max_length=100, default='')
    authority = models.CharField(max_length=100, default='')
    otherauthority = models.CharField(max_length=100, default='')
    mail = models.CharField(max_length=200, default='')
    jobtype = models.CharField(max_length=100, default='')

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)

class Leave(models.Model):
    leavetype = models.CharField(max_length=20, choices=LEAVE_TYPE, default='casual')
    station_leave = models.IntegerField(default='1')
    forward = models.IntegerField(default='0')
    start_date = models.DateField()
    end_date = models.DateField()
    station_start_date = models.DateField(null=True, blank=True)
    station_end_date = models.DateField(null=True, blank=True)
    no_of_days = models.IntegerField(default=0)
    purpose = models.CharField(max_length=500)
    comment = models.CharField(max_length=500, null=True, blank=True)
    leave_address = models.CharField(max_length=100, null=True, blank=True)
    applicant = models.ForeignKey(User, related_name='applied_for', on_delete=models.CASCADE)
    replacing_user = models.ForeignKey(User, related_name='replaced_for', on_delete=models.CASCADE)
    admin_user = models.ForeignKey(User, related_name='admin_for', on_delete=models.CASCADE)
    processing_status = models.CharField(max_length=20, default='Director', choices=PROCESSING_BY)
    application_status = models.CharField(max_length=20, default='processing', choices=APPLICATION_STATUSES)


class RemainingLeaves(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='remaining_leaves')
    casual = models.IntegerField(default=8)
    vacation = models.IntegerField(default=60, null=True, blank=True)
    commuted = models.IntegerField(default=20)
    special_casual = models.IntegerField(default=15)
    restricted = models.IntegerField(default=2)
    earned = models.IntegerField(default=30, null=True)
    year = models.IntegerField(default=2017)
