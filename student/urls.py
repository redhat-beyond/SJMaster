from django.urls import path
from student.views import update_student_account_settings_view, account_update_success

urlpatterns = [
    path('student/account_settings/', update_student_account_settings_view,
         name="student_account_settings"),
    path('account_update_success/', account_update_success,
         name="account_update_success"),
]
