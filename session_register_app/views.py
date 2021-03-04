from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request,'inicio.html')



def register(request):
    errors = Users.objects.validations(request.POST)
    print(errors)
    print(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        return redirect('/')
    else:
        passw = request.POST['password']
        hash = bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
        print(hash)
        u=Users.objects.create(fname=request.POST['fname'], lname=request.POST['lname'], 
        email=request.POST['email'], fday=request.POST['date'], password=hash)
        u.active = True
        request.session['id'] = u.id
        request.session['registrado'] = 'ok'
        messages.error (request, 'Registro exitoso')
    return redirect('/')



def login(request):
    try:
        usuario = Users.objects.filter(email=request.POST.get('email'))
        if len(usuario) > 0:

            hash = usuario[0].password
            password = request.POST['password'].encode()

            if bcrypt.checkpw(password, hash.encode()):

                usuario[0].active = True
                usuario[0].save()
                request.session['id'] = usuario[0].id
                return redirect('/main/success')

            else:
                messages.error (request, 'Error contraseña incorrecta')
                return redirect('/')

        elif len(usuario) == 0:
            messages.error (request, 'Email no registrado')
            return redirect('/')
    except:
        return redirect('/')



def success_login(request):
    usuario = Users.objects.filter(id=request.session.get('id'))
    if len(usuario) > 0 :
        if usuario[0].active == True:

            usuario[0]
            context = {
                    'usuario': usuario[0].fname + ' ' + usuario[0].lname,
                    'tipo_sesion':'logueado/a', 
                    'fecha': usuario[0].create_at
                }
            if 'registrado' in request.session:
                context['tipo_sesion'] = 'registrado/a'
            return redirect('/friends')
    messages.error (request,'Debe iniciar sesión o registrarse para ingresar')
    return redirect('/')


def validate_email(request):
    if 'email' in request.POST:
        email = request.POST.get('email')
        if len(Users.objects.filter(email=email)) > 0:
            return HttpResponse ('El Email ya se encuntra registrado')
    return HttpResponse('')


def logout(request):
    if 'id' in request.session:
        print('si habia id: ', request.session['id'])
        try:
            c = Users.objects.get(id=request.session['id'])
            c.active = False
            c.save()
        
            request.session.flush()
            messages.error(request,'Se ha cerrado sesión de manera exitosa')
        except:
            print('error')
            pass
    else:
        print('no habia id')
    return redirect('/')
