from django.shortcuts import render
from student.views import add_is_student_to_context


def board(request):
    context = {}
    add_is_student_to_context(request, context)
    return render(request, 'jobboard/board.html', context)
