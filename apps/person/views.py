from django.shortcuts import render

# Create your views here.
from apps.main.models import User

def index(request):
    return render(request,'person_index.html')


def information(request):

    if request.method == 'GET':
        uid = request.GET.get('uid')
        user = User.objects.get(id=uid)
        return render(request, 'information.html', locals())

    elif request.method == 'POST':
        try:
            uid = request.GET.get('uid')
            user = User.objects.get(id=uid)
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            user.first_name = first_name
            user.last_name = last_name
            user.phone = phone
            user.email = email
            user.save()
            return render(request, 'information.html', locals())
        except Exception as e:
           return render(request,'404.html')


def address(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        user = User.objects.get(id=uid)
        return render(request, 'address.html',locals())
    elif request.method == 'POST':
        pass
