from django.shortcuts import render, redirect, get_object_or_404
from .models import Student
from .forms import UpdateStudentAccountSettingsForm


def account_update_success(request):
    context = {}
    add_is_student_to_context(request, context)
    return render(request, 'account_settings_update_success.html', context)


def update_student_account_settings_view(request):
    context = {}
    student_object = get_object_or_404(Student, user_id=request.user.id)
    update_student_form = UpdateStudentAccountSettingsForm(request.POST or None, instance=student_object)
    add_is_student_to_context(request, context)
    context["form"] = update_student_form
    if request.method == 'GET':
        return render(request, "student_account_settings.html", context)

    elif request.method == "POST" and update_student_form.is_valid():
        update_student_form.save()
        return redirect("/account_update_success/", context)

    elif request.method == "POST" and not update_student_form.is_valid():
        return render(request, "student_account_settings.html", context)


def add_is_student_to_context(request, context):
    context["is_student"] = Student.is_student(request.user.id)
