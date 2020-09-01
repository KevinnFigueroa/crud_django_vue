from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from gestion_crud.models import usuarios
from django.forms.models import model_to_dict


def index(request):
    """
     .Retorna página principal.
    """
    return render(request, "index.html")


def read(request):
    """
     .Retorna todos los usuarios registrados en la base de datos.
    """
    usuario = list(usuarios.objects.values())
    return JsonResponse({"tasks": usuario}, status=200)


@csrf_exempt
def create(request):
    """
    . Recibe información desde el cliente.
    . Inserta datos del usuario dentro de la base de datos.
    . Retorna el usuario que se insertó.
    """
    if request.method == "POST":
        peticion = json.loads(request.body)
        usuario = usuarios(
            nombre=peticion.get("nombre"),
            apellido=peticion.get("apellido"),
            email=peticion.get("email"),
            telefono=peticion.get("telefono"),
        )
        usuario.save()
        return JsonResponse({"insertado": True, "consulta": model_to_dict(usuario)})


@csrf_exempt
def delete(request):
    """
    . Recibe id del usuario que se desea eliminar.
    . Elimina el usuario de la base de datos.
    . Retorna el usuario que fue eliminado.
    """
    if request.method == "DELETE":
        peticion = json.loads(request.body)
        usuario_eliminado = model_to_dict(usuarios.objects.get(id=peticion.get("id")))
        usuarios.objects.get(id=peticion.get("id")).delete()
        return JsonResponse({"borrado": True, "usuario_eliminado": usuario_eliminado})


@csrf_exempt
def update(request):
    """
    . Recibe información del usuario que se desea actualizar en la base de datos.
    . Con el id recibido se prepara el usuario a ser actualizado.
    . Se actualizan los datos ingresados por cliente.
    . Retorna el usuario actualizado.
    """
    if request.method == "PUT":
        peticion = json.loads(request.body)
        usuario_a_updatear = usuarios.objects.get(id=peticion.get("id"))
        usuario_a_updatear.nombre = peticion.get("nombre")
        usuario_a_updatear.apellido = peticion.get("apellido")
        usuario_a_updatear.email = peticion.get("email")
        usuario_a_updatear.telefono = peticion.get("telefono")
        usuario_a_updatear.save()
        return JsonResponse(
            {"actualizado": True, "usuario_nuevo": model_to_dict(usuario_a_updatear)}
        )
