from django import forms

class NewLeave(forms.Form):
    leavetype = forms.CharField(max_length=20, choices=LEAVE_CHOICE, default='casual')
    station_leave = forms.NullBooleanField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    station_start_date = forms.DateField(null=True)
    station_end_date = forms.DateField(null=True)
    no_of_days = forms.IntegerField(default=0)
    purpose = forms.CharField(max_length=500)
    leave_address = forms.CharField(max_length=100, null=True)
    applicant = forms.ForeignKey(User, related_name='applied_for', on_delete=forms.CASCADE)
    replacing_user = forms.ForeignKey(User, related_name='replaced_for', on_delete=forms.CASCADE)
    admin_user = forms.ForeignKey(User, related_name='admin_for', on_delete=forms.CASCADE)
    processing_status = forms.CharField(max_length=20, default='rep user', choices=PROCESSING_BY_CHOICES)
    application_status = forms.CharField(max_length=20, default='processing', choices=APPLICATION_STATUSES)
