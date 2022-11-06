from django.shortcuts import render

main_info = [
    {'left': 'Birthday', 'right': '13.03.1978'},
    {'left': 'Nationality', 'right': 'Australian / British'},
    {'left': 'Residing', 'right': 'Berlin, Germany'},
    {'left': 'Languages', 'right': 'English (native)'},
    {'left': '', 'right': 'German (intermediate)'},
]

def home(request):
    return render(request, 'main/main.html', {'info': main_info})

def max(request):
    return render(request, 'main/max.html', {})
