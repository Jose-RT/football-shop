from django.shortcuts import render

def show_main(request):
    context = {
        'shop' : 'Football Shop',
        'name': 'Manchaland Store',
        'class': 'PBP E'
    }

    return render(request, "main.html", context)