from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json


from .models import CustomUser, Staffs, Courses, Subjects, Students, SessionYearModel,  FeedBackStaffs_GV,Staffs_GV_HP


def staff_gv_home(request):
    return render(request, "staff_gv_template/staff_home_template.html")
def staff_gv_feedback(request):
    staff_obj = Staffs_GV_HP.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs_GV.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "staff_gv_template/staff_feedback_template.html", context)


def staff_gv_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_gv_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs_GV_HP.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs_GV(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_gv_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_gv_feedback')
def staff_gv_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs_GV_HP.objects.get(admin=user)

    context={
        "user": user,
        "staff": staff
    }
    return render(request, 'staff_gv_template/staff_profile.html', context)


def staff_gv_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('staff_gv_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            staff = Staffs_GV_HP.objects.get(admin=customuser.id)
            staff.address = address
            staff.save()

            messages.success(request, "Cập Nhật Thành Công")
            return redirect('staff_profile')
        except:
            messages.error(request, "Cập Nhật Thất Bại")
            return redirect('staff_gv_profile')
