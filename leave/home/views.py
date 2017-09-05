import datetime
from django.shortcuts import render, HttpResponse
from home.models import UserProfile, RemainingLeaves, Leave
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone

# Create your views here.
def auth(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = authenticate(username = username, password = password)
    request.session['username'] = username
    if user is not None:
        login(request, user)
        remaining_leaves = RemainingLeaves.objects.get(user=request.user.id)
        if remaining_leaves.year != timezone.now().year:
            remaining_leaves.year = timezone.now().year
            remaining_leaves.casual = 8
            remaining_leaves.restricted = 2
            remaining_leaves.earned += remaining_leaves.vacation/2
            remaining_leaves.vacation = 60
            remaining_leaves.commuted += 20
            remaining_leaves.special_casual += 15
            remaining_leaves.save()
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/home/incorrectinfo')

@login_required
def home(request):
    if 'username' in request.session:
        username = request.session['username']
    if 'leave_id' in request.session:
        lid = request.session['leave_id']
        leave_obj = Leave.objects.get(id=lid)
        flag = leave_obj.no_of_days
        ltype = leave_obj.leavetype
        remaining_leaves = RemainingLeaves.objects.get(user=request.user.id)
        if ltype == "casual":
            remaining_leaves.casual += flag
        if ltype == "restricted":
            remaining_leaves.restricted += flag
        if ltype == "special_casual":
            remaining_leaves.special_casual += flag
        if ltype == "earned":
            remaining_leaves.earned += flag
        if ltype == "commuted":
            remaining_leaves.commuted += flag
        if ltype == "vacation":
            remaining_leaves.vacation += flag
        remaining_leaves.save()
        leave_obj.delete()
        del request.session['leave_id']
    current_user = request.user
    lists = ["Head CSE","Head ME","Head ECE","Director","Head Design"]
    return render(request, 'leave/landing.html', {'profiles' :UserProfile.objects.all(),
                                                    'profile' :UserProfile.objects.get(user=current_user.id),
                                                    'username' :username,
                                                    'lists' :lists})

@login_required
def newleave(request):
    if 'username' in request.session:
        username = request.session['username']
        current_user = request.user
        user_profile = UserProfile.objects.get(user=current_user.id)
        remaining_leaves = RemainingLeaves.objects.get(user=current_user.id)
    return render(request, 'leave/newleave.html',  {'user_profile' :user_profile,
                                                    'profiles' :UserProfile.objects.all(),
                                                    'remaining_leaves' :remaining_leaves,
                                                    'username' :username})

@login_required
def insufficientleaves(request):
    if 'username' in request.session:
        username = request.session['username']
    return render(request, 'leave/insufficientleaves.html', {'username' :username})

@login_required
def rejectapplication(request):
    if 'username' in request.session:
        username = request.session['username']
    return render(request, 'leave/rejectapplication.html', {'username' :username})

@login_required
def confirmsanction(request):
    if 'username' in request.session:
        username = request.session['username']
    return render(request, 'leave/confirmsanction.html', {'username' :username})

@login_required
def forwardsanction(request):
    if 'username' in request.session:
        username = request.session['username']
    return render(request, 'leave/forwardsanction.html', {'username' :username})

@login_required
def rejectleave(request):
    comment = request.POST.get('message','')
    lid = request.session['leave']
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user.id)
    leave_obj = Leave.objects.get(id=lid)
    leave_obj.comment = comment
    leave_obj.processing_status = user_profile.designation
    leave_obj.application_status = "rejected"
    leave_obj.save()
    remaining_leaves = RemainingLeaves.objects.get(user=current_user.id)
    if leave_obj.leavetype == "casual":
        flag = remaining_leaves.casual + leave_obj.no_of_days
        remaining_leaves.casual = flag
    if leave_obj.leavetype == "restricted":
        flag = remaining_leaves.restricted + leave_obj.no_of_days
        remaining_leaves.restricted = flag
    if leave_obj.leavetype == "special_casual":
        flag = remaining_leaves.special_casual + leave_obj.no_of_days
        remaining_leaves.special_casual = flag
    if leave_obj.leavetype == "earned":
        flag = remaining_leaves.earned + leave_obj.no_of_days
        remaining_leaves.earned = flag
    if leave_obj.leavetype == "commuted":
        flag = remaining_leaves.commuted + leave_obj.no_of_days
        remaining_leaves.commuted = flag
    if leave_obj.leavetype == "vacation":
        flag = remaining_leaves.vacation + leave_obj.no_of_days
        remaining_leaves.vacation = flag
    remaining_leaves.save();
    return HttpResponseRedirect('/home/')

@login_required
def forwardapplication(request):
    lid = request.session['leave']
    leave_obj = Leave.objects.get(id=lid)
    leave_obj.forward = 1
    leave_obj.processing_status = "Director"
    leave_obj.save()
    return HttpResponseRedirect('/home/')

@login_required
def confirmapplication(request):
    lid = request.session['leave']
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user.id)
    leave_obj = Leave.objects.get(id=lid)
    leave_obj.processing_status = user_profile.designation
    leave_obj.application_status = "accepted"
    leave_obj.save()
    return HttpResponseRedirect('/home/')

@login_required
def approveleave(request):
    if 'username' in request.session:
        username = request.session['username']
    leave = Leave.objects.get(id=request.POST.get('submitleave',''))
    request.session['leave'] = request.POST.get('submitleave','')
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user.id)
    applicant_profile = UserProfile.objects.get(user=leave.applicant_id)
    return render(request, 'leave/leaveapprove.html', {'profiles' :UserProfile.objects.all(),
                                                        'leave' :leave,
                                                        'profile' :user_profile,
                                                        'applicant' :applicant_profile,
                                                        'username' :username})

@login_required
def confirmleave(request):
    leavetype = request.POST.get('leavetype','')
    start_date = request.POST.get('stdate','')
    end_date = request.POST.get('enddate','')
    days = request.POST.get('nodays','')
    station_leave = request.POST.get('stationleave','')
    leave_address = request.POST.get('leave_address','')
    station_start_date = request.POST.get('stationleavestdate','')
    station_end_date = request.POST.get('stationleaveenddate','')
    purpose = request.POST.get('purpose','')
    acadresponsibilty = UserProfile.objects.get(user=request.POST.get('acadresponsibilty',''))
    adminresponsibility = UserProfile.objects.get(user=request.POST.get('adminresponsibility',''))
    nodays = int(days)
    if (station_leave == "on"):
        sl = 1
    else:
        sl = 0
    if (station_start_date == ''):
        station_start_date = None
    if (station_end_date == ''):
        station_end_date = None
    if 'username' in request.session:
        username = request.session['username']
        current_user = request.user
        remaining_leaves = RemainingLeaves.objects.get(user=current_user.id)
        user_profile = UserProfile.objects.get(user=current_user.id)
        if leavetype == '1' or leavetype == '2':
            if user_profile.section == "CSE":
                processing_by = "Head CSE"
            elif user_profile.section == "ECE":
                processing_by = "Head ECE"
            elif user_profile.section == "ME":
                processing_by = "Head ME"
            elif user_profile.section == "NS":
                processing_by = "Head NS"
            elif user_profile.section == "Design":
                processing_by = "Head Design"
            else:
                processing_by = "Registrar"
        else:
            processing_by = "Director"
        if leavetype == '1':
            flag = remaining_leaves.casual - nodays
            ltype = "casual"
            if user_profile.authority == "Head":
                forward = 0
            else:
                forward = 1
            remaining_leaves.casual = flag
        if leavetype == '2':
            flag = remaining_leaves.restricted - nodays
            ltype = "restricted"
            if user_profile.authority == "Head":
                forward = 0
            else:
                forward = 1
            remaining_leaves.restricted = flag
        if leavetype == '3':
            flag = remaining_leaves.special_casual - nodays
            ltype = "special_casual"
            forward = 1
            remaining_leaves.special_casual = flag
        if leavetype == '4':
            flag = remaining_leaves.earned - nodays
            ltype = "earned"
            forward = 1
            remaining_leaves.earned = flag
        if leavetype == '5':
            flag = remaining_leaves.commuted - nodays
            ltype = "commuted"
            forward = 1
            remaining_leaves.commuted = flag
        if leavetype == '6':
            flag = remaining_leaves.vacation - nodays
            ltype = "vacation"
            forward = 1
            remaining_leaves.vacation = flag
        if flag >= 0:
            leave_obj = Leave(leavetype = ltype, station_leave = sl, forward = forward, start_date = start_date, end_date = end_date, station_start_date = station_start_date, station_end_date = station_end_date, no_of_days = nodays, purpose = purpose, comment = "", leave_address = leave_address, applicant = request.user, replacing_user = acadresponsibilty.user, admin_user  = adminresponsibility.user, processing_status = processing_by, application_status = "processing")
            leave_obj.save()
            remaining_leaves.save()
            request.session['leave_id'] = leave_obj.id
            return render(request, 'leave/leaveconfirm.html', {'profiles' :UserProfile.objects.all(),
                                                                'profile' :user_profile,
                                                                'username' :username,
                                                                'leave' :leave_obj})
        else:
            return HttpResponseRedirect('/home/insufficientleaves')

@login_required
def saveleave(request):
    if 'username' in request.session:
        username = request.session['username']
    del request.session['leave_id']
    return HttpResponseRedirect('/home/')

@login_required
def viewleaves(request):
    if 'username' in request.session:
        username = request.session['username']
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user.id)
    leaves = Leave.objects.filter(applicant=current_user.id, application_status="processing")
    past_leaves = Leave.objects.filter(applicant=current_user.id).exclude(application_status="processing")
    return render(request, 'leave/viewleaves.html', {'profile' :user_profile,
                                                    'past_leaves' :past_leaves,
                                                    'leaves' :leaves,
                                                    'username' :username})

@login_required
def deleteleave(request):
    if 'username' in request.session:
        username = request.session['username']
    leave_obj = Leave.objects.get(id=request.POST.get('deleteleave',''))
    current_user = request.user
    remaining_leaves = RemainingLeaves.objects.get(user=current_user.id)
    if leave_obj.leavetype == "casual":
        flag = remaining_leaves.casual + leave_obj.no_of_days
        remaining_leaves.casual = flag
    if leave_obj.leavetype == "restricted":
        flag = remaining_leaves.restricted + leave_obj.no_of_days
        remaining_leaves.restricted = flag
    if leave_obj.leavetype == "special_casual":
        flag = remaining_leaves.special_casual + leave_obj.no_of_days
        remaining_leaves.special_casual = flag
    if leave_obj.leavetype == "earned":
        flag = remaining_leaves.earned + leave_obj.no_of_days
        remaining_leaves.earned = flag
    if leave_obj.leavetype == "commuted":
        flag = remaining_leaves.commuted + leave_obj.no_of_days
        remaining_leaves.commuted = flag
    if leave_obj.leavetype == "vacation":
        flag = remaining_leaves.vacation + leave_obj.no_of_days
        remaining_leaves.vacation = flag
    remaining_leaves.save();
    leave_obj.delete()
    return HttpResponseRedirect('/home/viewleaves')

@login_required
def leavereject(request):
    if 'username' in request.session:
        username = request.session['username']
    leave_obj = Leave.objects.get(id=request.POST.get('submitleave',''))
    comment = leave_obj.comment
    return render(request, 'leave/leaverejectioninfo.html', {'comment' :comment,
                                                            'username' :username})

@login_required
def sanction(request):
    if 'username' in request.session:
        username = request.session['username']
    current_user = request.user
    user_profile = UserProfile.objects.get(user=current_user.id)
    if user_profile.designation == "Director":
        leave_obj = Leave.objects.filter(application_status = "processing", forward = 1)
        return render(request, 'leave/sanction.html', {'profiles' :UserProfile.objects.all(),
                                                        'leaves' :leave_obj,
                                                        'username' :username})
    elif user_profile.designation == "Head CSE":
        authority = "Head CSE"
        dep = "CSE"
    elif user_profile.designation == "Head ME":
        authority = "Head ME"
        dep = "ME"
    elif user_profile.designation == "Head ECE":
        authority = "Head ECE"
        dep = "ECE"
    elif user_profile.designation == "Head Design":
        authority = "Head Design"
        dep = "Design"
    elif user_profile.designation == "Head NS":
        authority = "Head NS"
        dep = "NS"
    leave_obj = Leave.objects.filter(Q(processing_status = authority), Q(leavetype = "casual") | Q(leavetype = "restricted"), Q(forward = 0))
    return render(request, 'leave/sanction.html', {'profiles' :UserProfile.objects.filter(section=dep),
                                                    'leaves' :leave_obj,
                                                    'username' :username})

def about(request):
    return render(request, 'leave/about.html')

def incorrectinfo(request):
    return render(request, 'leave/incorrectuserpass.html')

@login_required
def loggedout(request):
    logout(request)
    return HttpResponseRedirect('/home/login')
