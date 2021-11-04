from django.shortcuts import render, redirect


def board(request):
    return render(request, 'jobboard/board.html')
