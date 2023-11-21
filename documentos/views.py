from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from django.contrib import messages
from documentos.forms import LoginForm
from django.contrib.auth.decorators import login_required
from .forms import CreaDocForm, iniciarSesionForm
from .models import Documentos
# Create your views here.

def home_vista(request):
    return render(request,'home.html')
    


def login_vista(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def logout_vista(request):
    logout(request)
    return redirect('login')

def create_user(request):
    if request.method == 'GET':
        return render(request, 'create_user.html',{
        'form': iniciarSesionForm
        })
    else:
        #Compara las contraseñas si son iguales
        if request.POST['password1']==request.POST['password2']:
            #Guarda los datos en la BD
            try:
                user=User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    email=request.POST['email'],)
                user.save()
                #login(request, user)
                return redirect('home')
            except:
                return render(request, 'create_user.html',{
                    'form': iniciarSesionForm,
                    "error":'Usuario ya existe'
                })
        return render(request,'create_user.html',{
            'form': iniciarSesionForm,
            "error":'Password no coincide'
        })

@login_required
def create_doc(request):
    if request.method == 'GET':
        return render(request, 'create_doc.html', {'form': CreaDocForm})
    else:
        try:
            form= CreaDocForm(request.POST) 
            nuevo_documento = form.save(commit=False)
            nuevo_documento.user = request.user
            nuevo_documento.save()  
            return redirect('home')
            
        except ValueError:
            return render(request, 'create_doc.html',{
                'form': CreaDocForm,
                'error': 'Por favor entrega datos válidos.'
            })
        
@login_required            
def doc_lista(request):
    listaD= Documentos.objects.filter(user=request.user)
    return render(request,'doc_lista.html',{'documentos':listaD})

        

@login_required
def doc_detalle(request, id):
    if request.method =='GET':
        documentosList= get_object_or_404(Documentos, pk=id, user=request.user)
        form = CreaDocForm(instance=documentosList)
        return render(request,'doc_detalle.html',{'documentos':documentosList, 'form':form})
    else:
        try:
            documentosList= get_object_or_404(Documentos, pk=id, user=request.user)
            form = CreaDocForm(request.POST, instance= documentosList)
            form.save()
            return redirect('doc_lista')
        except ValueError:
            return render(request,'doc_detalle.html',{'documentos':documentosList, 'form':form, 'error': "Error al actualizar Tabla Documentos"})

@login_required
def doc_delete(request, id):
    documentosList= get_object_or_404(Documentos, pk=id, user=request.user)
    if request.method =='POST':
        documentosList.delete()
        return redirect('doc_lista')    
