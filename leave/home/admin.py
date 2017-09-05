from django.contrib import admin
from home.models import UserProfile, RemainingLeaves, Leave
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'section', 'designation', 'jobtype')

class LeaveAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'leavetype', 'application_status')

class RemainingLeavesAdmin(admin.ModelAdmin):
    list_display = ('user','casual','vacation','earned','commuted','restricted','special_casual')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(RemainingLeaves, RemainingLeavesAdmin)
