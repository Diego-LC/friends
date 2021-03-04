from django.shortcuts import render, redirect
from session_register_app.models import *

def show_friends(request):
    val = request.session.get('id')
    u = Users.objects.filter(id=val)
    if u:
        context = {
            'user': u[0],
            'amigos':u[0].friends.all(),
            'no_amigos':Users.objects.exclude(friends2__u_id__id=u[0].id),
        }
        # if not context['amigos']:
        #     context['no_amigos'] = Users.objects.all().exclude(id=u[0].id)
        # else:
        #     context['no_amigos'] = Users.objects.exclude(all__friend__id=u[0].id)
        return render(request,'friends.html', context)
    return redirect('/main')

def add_friend(request, num):
    val = request.session.get('id')
    u = Users.objects.filter(id=val)
    f = Users.objects.filter(id=num)
    if u and f:
        friend = f[0]
        user = u[0]
        Friends.objects.create(u_id=user, friend_id=friend)
        Friends.objects.create(u_id=friend, friend_id=user)
    return redirect('/friends')

def remove_friend(request, num):
    val = request.session.get('id')
    u = Users.objects.filter(id=val)
    f = Users.objects.filter(id=num)
    if u and f:
        friend = f[0]
        user = u[0]
        fr=Friends.objects.get(friend_id=friend)
        fr2=Friends.objects.get(friend_id=user)
        fr.delete()
        fr2.delete()
    return redirect('/friends')

def show_user(request, num):
    val = request.session.get('id')
    u = Users.objects.filter(id=val)
    user = Users.objects.filter(id=num)
    if u and user:
        context = {
            'user': user[0]
        }
        return render(request,'show_user.html', context)
    return redirect('/main')

