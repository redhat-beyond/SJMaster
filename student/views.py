from django.shortcuts import render, HttpResponseRedirect
from .models import Student
from .forms import UpdateStudentAccountSettingsForm


def account_update_success(request):
    is_student = Student.is_student(request.user.id)
    return render(request, 'account_settings_update_success.html', {"is_student": is_student})


def update_student_account_settings_view(request):
    context = {}
    try:
        student_object = Student.objects.get(user_id=request.user.id)
    except Student.DoesNotExist:
        return render(request, "dead_end.html")
    update_student_form = UpdateStudentAccountSettingsForm(request.POST or None, instance=student_object)
    if update_student_form.is_valid():
        update_student_form.save()
        return HttpResponseRedirect("/account_update_success/")
    context["form"] = update_student_form
    add_is_student_to_context(request, context)
    return render(request, "student_account_settings.html", context)


def add_is_student_to_context(request, context):
    context["is_student"] = Student.is_student(request.user.id)
