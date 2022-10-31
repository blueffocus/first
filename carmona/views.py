from django.shortcuts import render

# Create your views here.
from django.template.loader import get_template
from carmona.models import *
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from unicodedata import normalize, category
from carmona.forms import *
from django.shortcuts import redirect
from django.http import JsonResponse
from django.utils import timezone
import datetime


def ads(request):
    return render(request, 'ads.txt',{
        })


def now():
    now = datetime.datetime.now()
    return now


def ajax(request):
    rating = request.GET['rating']
    id = request.GET['id']
    error = True
    carrera_ajax = {}
    try:
        obj = Puntuacion.objects.get(usuario_id=request.user.id, carrera_id=id)
        obj.puntuacion = rating
        obj.fecha = now()
        obj.save()
    except Puntuacion.DoesNotExist:
        Puntuacion.objects.filter(carrera=id).filter(usuario_id=request.user.id).update(puntuacion=rating,
                                                                                        fecha=now())
        model_puntuacion = Puntuacion.objects.create(carrera_id=id, puntuacion=rating, fecha=now(),
                                                     usuario_id=request.user.id)
        model_puntuacion.save()
    if carrera_ajax:
        error = False

    carrera_ajax['id'] = id
    carrera_ajax['error'] = error
    carrera_ajax['rating'] = rating
    carrera_ajax['media'] = calcular_puntuacion(id)
    return JsonResponse(carrera_ajax)


def ajax_comentarios(request):
    mensaje = request.GET['mensaje']
    id = request.GET['id']
    usuario = request.user
    fecha = now()
    if len(mensaje) > 1:
        mensaje_ajax = {}
        obj = Comentario.objects.create(carrera_id=id, comentario=mensaje, fecha=now(), usuario_id=usuario.id)
        obj.save()
    mensaje_ajax['id'] = id
    mensaje_ajax['mensaje'] = mensaje
    mensaje_ajax['usuario_nombre'] = usuario.username
    mensaje_ajax['usuario_id'] = usuario.id
    mensaje_ajax['fecha'] = fecha.strftime('%d/%m/%Y - %H:%M:%S')
    mensaje_ajax['error'] = "Debe de tener mas de 2 caracteres"
    mensaje_ajax['mensaje_id'] = obj.id
    return JsonResponse(mensaje_ajax)


def ajax_borrar_mensajes(request):
    id_carrera = request.GET['id']
    mensaje_id = request.GET['mensaje_id']
    borrar_ajax = {}
    comentario = Comentario.objects.get(pk=mensaje_id)
    comentario.delete()
    borrar_ajax['id'] = mensaje_id
    return JsonResponse(borrar_ajax)


# Vista del template inscripcion.html
def contactomail(request):
    formulario = FormularioContacto(initial={'comentario': ''})
    fail = "No se pudo enviar el email, compruebe que todos los campos están rellenos correctamente."
    if request.method == 'POST':
        formulario = FormularioContacto(request.POST, initial={'comentario': 'sin comentario'})
        if formulario.is_valid() and formulario.cleaned_data['evento'] == formulario.cleaned_data['confirmar_evento']:
            if validoDNI(formulario.cleaned_data['dni']):
                asunto = "INSCRIPCIÓN"
                html_message = "<div style='background-color: #fff; color:black; text-align:center; margin:40px auto;'>" \
                               "<br><h3>Email:<span style='color:#5050AF; padding-left:10px;'><a href='mailto:" + \
                               formulario.cleaned_data['email'] + "'>" + formulario.cleaned_data['email'] + "<a/></span></h3>" \
                                            "<br><h3>DNI:<span style='color:#5050AF; padding-left:10px;'>" + \
                               formulario.cleaned_data['dni'].upper() + "</span></h3>" \
                                                               "<br><h3>Nº Socio:<span style='color:#5050AF; padding-left:10px;'>" + str(
                               formulario.cleaned_data['socio']) + "</span></h3>" \
                                                        "<br><h3>Evento:<span style='color:#5050AF; padding-left:10px;'>" + str(
                               formulario.cleaned_data['evento']) + "</span></h3>" \
                                                         "<br><h3>Comentario:<span style='color:#5050AF; padding-left:10px;'>" + \
                               formulario.cleaned_data['comentario'] + "</span></h3></div>"

                email = EmailMultiAlternatives(asunto, html_message, to=['clubatletismocarmonapaez@gmail.com'], headers={'Reply-To':formulario.cleaned_data['email']})
                #email.attach_alternative(html_message, 'text/html')
                email.content_subtype = "html"
                email.send()
                ok = "El email se ha enviado con éxito."
                return render(request, 'club/inscripcion.html', {
                    'ok': ok,
                    'formulario': formulario,
                    'proximos': menuLateral()['proximos'],
                    'carreras': menuLateral()['carreras'],
                    'hoy': menuLateral()['hoy'], })
            else:
                fail='El DNI no es correcto'
        return render(request, 'club/inscripcion.html', {
            'fail':fail,
            'formulario': formulario,
            'proximos': menuLateral()['proximos'],
            'carreras': menuLateral()['carreras'],
            'hoy': menuLateral()['hoy'], })
    return render(request, 'club/inscripcion.html', {
        'formulario': formulario,
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'], })




def contacto(request):
    formulario = FormularioContacta(initial={'comentario': ''})
    fail = "No se pudo enviar el email, compruebe que todos los campos están rellenos correctamente."
    if request.method == 'POST':
        formulario = FormularioContacta(request.POST, initial={'comentario': 'sin comentario'})
        if formulario.is_valid():
            asunto = formulario.cleaned_data['asunto']
            mensaje = "EMAIL: " + formulario.cleaned_data['email'] \
                      + "\nNOMBRE: " + formulario.cleaned_data['nombre'] \
                      + "\n\nCOMENTARIO: " + formulario.cleaned_data['comentario']

            mail = EmailMessage(asunto, mensaje, to=['clubatletismocarmonapaez@gmail.com'], headers={'Reply-To':formulario.cleaned_data['email']})
            mail.send()
            ok = "El email se ha enviado con éxito."
            return render(request, 'club/contacta.html', {
                'ok': ok,
                'formulario': formulario,
                'proximos': menuLateral()['proximos'],
                'carreras': menuLateral()['carreras'],
                'hoy': menuLateral()['hoy'],
            })
        return render(request, 'club/contacta.html', {
            'fail': fail,
            'formulario': formulario,
            'proximos': menuLateral()['proximos'],
            'carreras': menuLateral()['carreras'],
            'hoy': menuLateral()['hoy'],
        })
    return render(request, 'club/contacta.html', {
        'formulario': formulario,
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
    })


# Vista del template calendario.html
def calendario(request):
    carrerastodas = Carrera.objects.filter(fecha__gte=now()).order_by('fecha')
    car = Carrera.objects.filter(fecha__gte=now()).filter(destacada=True).order_by('fecha')[:12]
    anio = list(range(now().year, now().year + 2))
    return render(request, 'club/calendario.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'anio': anio,
        'carrerastodas': carrerastodas,
        'car': car,
    })


# Vista del template calendario2.html
def calendario2(request):

    query = request.GET.get('sel')
    if query == None:
        query = str(now().year)

    form = FormularioCalendario2()
    car = Carrera.objects.filter(fecha__lt=now()).filter(destacada=True).order_by('-fecha')[:6]
    carreras2 = Carrera.objects.filter(fecha__lt=now()).order_by('-fecha')
    resul = Carrera.objects.filter(fecha__year=query).order_by('fecha')
    return render(request, 'club/calendario2.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'form': form,
        'query': query,
        'resul':resul,
        'carreras2': carreras2,
        'car': car,
    })


# Vista del template carrera.html
def carrera(request, id):
    carrera = Carrera.objects.get(pk=id)
    hasta_dia = now() + timedelta(days=30)
    diferencia = carrera.fecha.timestamp() - now().timestamp()  # optener la diferencia de dias entre el dia de hoy y el de la carrera
    carr = Carrera.objects.all().order_by('fecha')
    participantes = Participante.objects.filter(p_carrera_id__fecha__gte=now())
    fotos = GaleriaFoto.objects.filter(carrera_id=id)
    nota = calcular_puntuacion(id)
    comentario = Comentario.objects.filter(carrera=id).order_by('-fecha')
    puntos = Puntuacion.objects.filter(carrera_id=id).filter(usuario_id=request.user.id)
    value = 0
    for p in puntos:
        value = p.puntuacion
    usuario = request.user

    return render(request, 'club/carrera.html', {
        'fotos': fotos,
        'comentarios': comentario,
        'usuario': usuario,
        'd': hasta_dia,
        'nota': nota,
        'puntos': value,
        'vueltas': range(1, 11),
        'carrera': carrera,
        'id': carrera,
        'diferencia_dias': int(diferencia / 86400),
        # paso el numero unix a dias (86400 segundos que tiene un día) tomo la parte entera
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'carr': carr,
        'participantes': participantes})


# Vista del template ficha.html
def ficha(request, id):
    posts = Post.objects.filter(pk=id)
    return render(request, 'club/ficha.html', {'posts': posts,
                                               'proximos': menuLateral()['proximos'],
                                               'carreras': menuLateral()['carreras'],
                                               'hoy': menuLateral()['hoy'],
                                               'carrera': carrera, })


# Vista del template galeria.html
def galeria(request):
    album = Album.objects.all()
    fotos = GaleriaFoto.objects.all()
    dias = now() - timedelta(days=30 * 6)
    carrera = Carrera.objects.filter(galeriafoto__galeria__isnull=False).filter(fecha__gte=dias).distinct().order_by(
        '-fecha')
    color = ['forestgreen', 'blueviolet', 'coral', 'deeppink', 'darkorange', 'darkgreen', 'crimson', 'deepskyblue']
    return render(request, 'club/galeria.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'album': album,
        'color': color,
        'dias': dias,
        'fotos': fotos,
        'carrera': carrera,
    })


def club(request):
    return render(request, 'club/club.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
    })


# Vista del template socio.html
def socio(request):
    return render(request, 'club/haztesocio.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
    })





# Vista del template participantes.html
def participantes(request):
    carrera = Carrera.objects.all().order_by('fecha')
    participantes = Participante.objects.filter(p_carrera_id__fecha__gte=now()).order_by(
        'p_carrera_id__fecha')
    actualizado = Participante.objects.filter(fecha__lte=now()).order_by('-fecha')
    return render(request, 'club/participantes.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'participantes': participantes,
        'actualizado': actualizado,
        'carrera': carrera, })


# Vista del template liga.html
def liga(request):
    liga = Liga.objects.all()
    if liga:
        actualizado = liga.last().fecha
    else:
        actualizado = ""
    print(liga)
    li=[]
    for l in reversed(liga):
        li.append(l)
    print(li)
    return render(request, 'club/liga.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'liga': li,
        'actualizado': actualizado})



# Vista del template resultados.html
def resultados(request):
    query = request.GET.get('sel')
    if query == None:
        query = str(now().year)

    form = FormularioResultados()
    carrera = Carrera.objects.filter(resultado_id__isnull=False).order_by('-fecha')
    resul = Carrera.objects.filter(fecha__year=query).order_by('fecha')

    # Resultados de carreras antiguas.
    import os
    listaresultados = []
    if query < "2016":
        lista = (os.listdir(path="./static/resultados"))
        for l in lista:
            if l[:4] == query:
                listaresultados.append(l)

    return render(request, 'club/resultados.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'form': form,
        'query': query,
        'carreras2': carrera,
        'resul': resul,
        'lista': sorted(listaresultados), })


# Vista del template buscador
def buscar(request):
    carreras = Carrera.objects.filter(resultado_id__isnull=False).order_by('-fecha')
    query = request.GET.get(str('buscar'))
    query = normalizar(str(query).lower())
    if len(query) >= 1:
        carrera = Carrera.objects.all().order_by('-fecha')
        lista = []
        for c in carrera:
            tituloNormalizado = normalizar(c.titulo.lower())
            ciudadNormalizada = normalizar(c.ciudad.lower())
            if tituloNormalizado.__contains__(query):
                lista.append(c.id)
            elif ciudadNormalizada.__contains__(query):
                lista.append(c.id)
        carrera = Carrera.objects.filter(id__in=sorted(lista)).order_by('-fecha')
        post = Post.objects.filter(titulo__contains=query).order_by("-fecha_publicacion")
    else:
        carrera = ''
    return render(request, "club/buscador.html", {
        'proximos': menuLateral()['proximos'],
        'carrera': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'carreras': carreras,
        "buscar2": carrera,
        "query": query, })


# Vista del template buscador avanzado
def buscarFiltro(request):
    tipo = request.path[8:9:]
    query = request.path[10::]

    if tipo == '1':
        carrera = Carrera.objects.filter(fecha__gte=timezone.datetime.today()).order_by("fecha")
    elif tipo == '2':
        carrera = Carrera.objects.filter(fecha__lt=timezone.datetime.today()).order_by("-fecha")
    else:
        carrera = Carrera.objects.all().order_by('fecha')
    buscar = listasDeBusqueda(carrera, tipo, query)
    return render(request, "club/buscador.html", {
        'query': query,
        'keyword': tipo,
        'buscar2': buscar,
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
    })


# Almacena en una lista los resultados de la busqueda realizando la normalizacion de los caracteres
def listasDeBusqueda(carrera, tipo, query):
    lista = []
    for c in carrera:
        tituloNormalizado = normalizar(c.titulo.lower())
        ciudadNormalizada = normalizar(c.ciudad.lower())
        if tituloNormalizado.__contains__(query):
            lista.append(c.id)
        elif ciudadNormalizada.__contains__(query):
            lista.append(c.id)

    if tipo == '1':
        carreraF = Carrera.objects.filter(id__in=lista).order_by('fecha')
    else:
        carreraF = Carrera.objects.filter(id__in=lista).order_by('-fecha')

    return carreraF


# Para quitar tildes y caracteres especiales
def normalizar(cadena):
    return ''.join([x for x in normalize('NFD', cadena) if category(x) == 'Ll'])


# Vista del template seccion.html
def seccion(request):
    path = request.path[1::]
    seccionMontania = Post.objects.filter(seccion=4).order_by('-fecha_publicacion')
    seccionTriatlon = Post.objects.filter(seccion=3).order_by('-fecha_publicacion')
    seccionEscuela = Post.objects.filter(seccion=2).order_by('-fecha_publicacion')
    seccionEntrenamiento = Post.objects.filter(seccion=5).order_by('-fecha_publicacion')

    return render(request, 'club/seccion.html', {
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        'path': path,
        'seccion1': seccionMontania,
        'seccion2': seccionEscuela,
        'seccion3': seccionTriatlon,
        'seccion4': seccionEntrenamiento,
    })


# pagina de noticias la principal, utiliza pagination con scroll
"""@el_pagination.decorators.page_template('club/noticias.html')"""
def post_list(request, template='club/post_list.html', extra_context=None):
    context = {
        'entries': Post.objects.filter(seccion_id=1).order_by('-fecha_publicacion'),
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

def patrocinadores(request):
    return render(request, 'club/patrocinadores.html',{
    'patrocinador': Patrocinador.objects.all,
    'proximos': menuLateral()['proximos'],
    'carreras': menuLateral()['carreras'],
    'hoy': menuLateral()['hoy'],
    })


# carga las imagenes de los albumes
def imagenes(request):
    a = Album.objects.all()
    return (request, 'club/galeria.html', {'a': a})


# Calcula la puntuacion media de cada carrera y la redondea.
def calcular_puntuacion(id):
    punt = Puntuacion.objects.filter(carrera=id)
    num = 0
    for p in punt:
        num = num + p.puntuacion
    if num > 0:
        nota = num / len(punt)
    else:
        nota = 0
    return round(nota, 1)


def validoDNI(dni):
    tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
    dig_ext = "XYZ"
    reemp_dig_ext = {'X':'0', 'Y':'1', 'Z':'2'}
    numeros = "1234567890"
    dni = dni.upper()
    if len(dni) == 9:
        dig_control = dni[8]
        dni = dni[:8]
        if dni[0] in dig_ext:
            dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
        return len(dni) == len([n for n in dni if n in numeros]) \
            and tabla[int(dni)%23] == dig_control
    return False


# Carga de información el listado de proximos eventos y de resultados.
def menuLateral():
    proximos = Carrera.objects.filter(fecha__gte=now()).order_by('fecha')[:7]
    carreras = Carrera.objects.filter(resultado_id__isnull=False).order_by('-fecha')
    hoy = now()
    return {'proximos': proximos, 'hoy': hoy, 'carreras': carreras}


# Vista del template estadisticas.html
def estadisticas(request):

    total = Carrera.objects.all()

    listaAnios = ['2016','2017','2018','2019','2020','2021','2022']
    coleccionAnios = []
    n=0
    p=0
    for a in listaAnios:
        for c in Carrera.objects.filter(fecha__year=a):
            n=n+1
            p=round(n/total.count()*100,1)

        coleccionAnios.append([format(n, "03d"),p])
        n=0
        p=0
    print(coleccionAnios)

    coleccionProvincias = []
    coleccionCiudad = []
    coleccionTipo = []

    for tip in Tipo.objects.all():
        for c in Carrera.objects.filter(tipo=tip):
            n=n+1
        coleccionTipo.append([tip,n])
        n=0
    ti = sorted(coleccionTipo, key=lambda objeto: objeto[1])
    ti.reverse()

    totalNoticias = Post.objects.all()
    totalGalerias = GaleriaFoto.objects.all()


    for pro in Provincia.objects.all():
        for c in Carrera.objects.filter(provincia=pro):
            n=n+1
        coleccionProvincias.append([pro,n])
        n=0
    print(coleccionProvincias)
    p = sorted(coleccionProvincias, key=lambda objeto: objeto[1])
    p.reverse()


    """for pro in Carrera.objects.all():
        for c in Carrera.objects.filter(ciudad=pro.ciudad):
            n=n+1
        if ([pro.ciudad,n]) not in coleccionCiudad:
            coleccionCiudad.append([pro.ciudad,n])
        n=0
    ciu = sorted(coleccionCiudad, key=lambda objeto: objeto[1])
    ciu.reverse()"""






    return render(request, 'club/estadisticas.html', {
        'total':total,
        'totalG':totalGalerias,
        'porAnio':coleccionAnios,
        'totalN':totalNoticias,
        'porTipo':ti,
        'porProvincias':p,
        'proximos': menuLateral()['proximos'],
        'carreras': menuLateral()['carreras'],
        'hoy': menuLateral()['hoy'],
        })
"""'porCiudad':ciu,"""
