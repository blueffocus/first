from django.urls import path

import carmona.views

urlpatterns = [
    path('', carmona.views.post_list, name='noticias'),
]
'''url(r'^$', views.post_list, name='noticias'),
    url(r'^calendario$', views.calendario, name='calendario'),
    url(r'^calendario2$', views.calendario2, name='calendario2'),
    url(r'^ficha/(?P<id>[0-9]+)$', views.ficha, name='ficha'),
    url(r'^carrera/(?P<id>[0-9]+)$', views.carrera, name='carrera'),
    url(r'^club$', views.club, name='club'),
    url(r'^galeria$', views.galeria, name='galeria'),
    url(r'^static/img', views.imagenes, name='img'),
    url(r'^resultados$', views.resultados, name='resultados'),
    url(r'^inscripcion', views.contactomail, name='inscripcion'),
    url(r'^contacta', views.contacto, name='contacta'),
    url(r'^listaparticipantes', views.participantes, name='participantes'),
    url(r'^buscar', views.buscar, name='buscar'),
    url(r'^search-', views.buscarFiltro, name='buscarF'),
    url(r'^liga', views.liga, name='liga'),
    url(r'^haztesocio', views.socio, name='haztesocio'),
    url(r'^montaña', views.seccion, name='montaña'),
    url(r'^triatlon', views.seccion, name='triatlon'),
    url(r'^entrenamiento', views.seccion, name='entrenamiento'),
    url(r'^escuela', views.seccion, name='escuela'),
    url(r'^jet/', include('jet.urls', 'jet')),
    url(r'^puntuar/$', views.ajax, name='puntuar'),
    url(r'^mensaje/$', views.ajax_comentarios, name='mensaje'),
    url(r'^borrar_mensaje/$', views.ajax_borrar_mensajes, name='borrar_mensaje'),
    url(r'^estadisticas/$', views.estadisticas, name='estadisticas'),
    url(r'^patrocinadores/$', views.patrocinadores, name='patrocinador'),
    url(r'^ads.txt$', views.ads, name='ads'),'''
