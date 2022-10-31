from django.contrib import admin

# Register your models here.
from datetime import datetime, timedelta
from django.contrib import admin
from .models import Post, Carrera, Album, Tipo, Seccion, Participante, Liga, GaleriaFoto, Imagen, Resultado, Comentario, Puntuacion, Patrocinador


def now():
    now = datetime.now()
    return now



class AdminGaleria(admin.ModelAdmin):

    def galeria_titulo(obj):
        return  obj.carrera.titulo.upper()
    def galeria_fecha(obj):
        return  format(obj.carrera.fecha,('%d/%m/%Y'))

    list_display = ('carrera',galeria_fecha,'detalles')
    ordering = ('-carrera_id__fecha','-id')
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'carrera':
            kwargs["queryset"] = Carrera.objects.filter(fecha__gte=now()-timedelta(days=90)).filter(fecha__lte=now()).order_by('-fecha')
        return super(AdminGaleria, self).formfield_for_foreignkey(db_field, request, **kwargs)



class GaleriaInlineAdmin(admin.TabularInline):
    model = GaleriaFoto


class Admincarrera(admin.ModelAdmin):
    list_display=('titulo','ciudad','fecha','destacada')
    list_filter=('fecha','tipo')
    ordering=('-fecha',)
    search_fields=('titulo','fecha','ciudad')
    readonly_fields=('cartel',)
    inlines = [GaleriaInlineAdmin,]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "foto":
            kwargs["queryset"] = Imagen.objects.filter(tipo=1)
        return super(Admincarrera, self).formfield_for_foreignkey(db_field, request, **kwargs)



class Adminpost(admin.ModelAdmin):
    list_display=('titulo','seccion','fecha_publicacion','visible')
    list_filter=('fecha_publicacion','seccion')
    ordering=('-fecha_publicacion','visible')
    search_fields=('titulo','fecha_publicacion')
    readonly_fields=('cartel',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "foto":
            kwargs["queryset"] = Imagen.objects.filter(tipo=2)
        return super(Adminpost, self).formfield_for_foreignkey(db_field, request, **kwargs)

class Adminpatro(admin.ModelAdmin):
    list_display=('titulo',)
    readonly_fields=('cartel',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "foto":
            kwargs["queryset"] = Imagen.objects.filter(tipo=4)
        return super(Adminpatro, self).formfield_for_foreignkey(db_field, request, **kwargs)

class AdminSeccion(admin.ModelAdmin):
    list_display=('titulo','fecha')
    ordering=('fecha',)
    search_fields=('titulo','fecha')



class AdminParticipantes(admin.ModelAdmin):

    def ciudad(obj):
        return obj.p_carrera_id.ciudad
    def fechaC(obj):
        return obj.p_carrera_id.fecha.strftime("%d/%m/%Y")
    def carrera(obj):
        return obj.p_carrera_id.titulo.upper()

    def caducada(modeladmin, request, queryset):
            queryset.update(Caducada=True)

    search_fields = ['p_carrera_id__titulo','p_carrera_id__ciudad']
    ciudad.short_description = 'Ciudad'
    fechaC.short_description = 'Fecha'
    list_filter = ('Caducada','p_carrera_id__fecha')
    list_display =(carrera,fechaC,ciudad,'Caducada')
    ordering =('-p_carrera_id__fecha','Caducada')
    actions = [caducada]


class AdminResultado(admin.ModelAdmin):
    ordering = ('-resultado',)
    search_fields = ('resultado',)

    r = Resultado.objects.all()
    listaresultados = []
    import  os
    lista = (os.listdir(path=""))
    for re in r:
        listaresultados.append(re.resultado.__str__()[18:])

    for l in lista:
        if l not in listaresultados:
            model_resultados = Resultado.objects.create(resultado=''+ l)
            model_resultados.save()

class AdminImagen(admin.ModelAdmin):
    list_display=('__str__','tipo','imagen',)
    search_fields=('imagen',)
    list_filter = ('tipo',)
    ordering = ('-imagen',)

class AdminComentario(admin.ModelAdmin):
    list_display = ('fecha','carrera_id','usuario_id','comentario')
    readonly_fields = ('comentario','fecha','carrera','usuario')
    ordering = ('-fecha',)
    exclude =('usuario','carrera')


class AdminPuntuacion(admin.ModelAdmin):
    list_display = ('fecha','carrera_id','usuario_id','puntuacion')
    readonly_fields = ('puntuacion','fecha','carrera','usuario')
    ordering = ('-fecha',)

admin.site.register(Post, Adminpost)
admin.site.register(Carrera, Admincarrera)
admin.site.register(Comentario, AdminComentario)
admin.site.register(Puntuacion, AdminPuntuacion)
admin.site.register(Album)
admin.site.register(Liga)
admin.site.register(Tipo)
admin.site.register(Seccion)
admin.site.register(GaleriaFoto,AdminGaleria)
admin.site.register(Participante, AdminParticipantes)
admin.site.register(Imagen,AdminImagen)
admin.site.register(Resultado, AdminResultado)
admin.site.register(Patrocinador, Adminpatro)
#admin.site.register(Provincia)

