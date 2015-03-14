from django.shortcuts import render


def persons_list(request):
    return render(request, 'bare.html', {})
