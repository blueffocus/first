
# Create your models here.
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import post_delete
from django.dispatch import receiver
import datetime


def now():
    now = datetime.datetime.now()
    return now

# Create your models here.

tipo_imagen_choices=(
	(1,'cartel'),
	(2,'post'),
	(3,'varios'),
	(4,'patrocinador'),
)



class Seccion(models.Model):
	seccion = models.CharField(max_length=200)

	def __str__(self):
		return self.seccion
	class Meta:
		verbose_name_plural = "Secciones"

class Imagen(models.Model):
	id = models.IntegerField.auto_creation_counter
	imagen = models.ImageField(upload_to='./static/img/imagenes', default="static/img/imagenes/nofoto.jpg") #cartel de la carrera
	tipo = models.IntegerField(choices=tipo_imagen_choices, default=1)
	def __str__(self):
		return self.imagen.name[20:]
	class Meta:
		verbose_name_plural = "Imagenes"




class Post(models.Model):
	seccion = models.ForeignKey(Seccion, default='1',on_delete=models.DO_NOTHING, blank=True, null=True)
	titulo = models.CharField(max_length=250)
	foto = models.ForeignKey(Imagen, on_delete=models.DO_NOTHING, blank=True, null=True)
	cartel = models.CharField(max_length=250, blank=True, null=True)
	texto = RichTextField(max_length=99999999)
	fecha_publicacion = models.DateTimeField(blank=True, null=True, default=now())
	visible = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if self.foto != None:
			foto2 = Imagen.objects.filter(id=self.foto_id)
			self.cartel = '/'+foto2.get().imagen.name
		else:
			self.cartel = 'static/img/logo1.jpg'
		super(Post, self).save(*args, **kwargs)

	def __str__(self):
		return str(self.fecha_publicacion.strftime("%d/%m/%y"))+"  -  "+str(self.titulo)


class Tipo(models.Model):
	tipo = models.CharField(max_length=200)

	def __str__(self):
		return self.tipo

class Provincia(models.Model):
	provincia = models.CharField(max_length=50)
	def __str__(self):
		return self.provincia

class Resultado(models.Model):
	resultado = models.FileField(upload_to='./static/resultados')
	def __str__(self):
		return self.resultado.name[18:]

class Carrera(models.Model):
	titulo = models.CharField(max_length=250)
	fecha = models.DateTimeField(default=now()) #Fecha y hora de la carrera  de la carrera
	link = models.CharField(max_length=200, blank=True, null=True) # Enlace a la web oficial de la carrera encargada de las inscripciones
	foto = models.ForeignKey(Imagen, on_delete=models.DO_NOTHING, blank=True, null=True)
	cartel = models.CharField(max_length=250, blank=True, null=True)
	provincia = models.ForeignKey(Provincia, default=17,on_delete=models.DO_NOTHING)
	ciudad = models.CharField(max_length=200, blank=True, null=True) # Ciudad donde se celebra la carrera
	distancia = models.IntegerField(blank=True, null=True)
	precio = models.CharField(max_length=50, blank=True, null=True)
	tipo = models.ForeignKey(Tipo, on_delete=models.DO_NOTHING, blank=True, null=True)
	destacada = models.BooleanField(default=True)
	resultado = models.OneToOneField(Resultado, on_delete=models.DO_NOTHING, blank=True, null=True)
	texto = RichTextField(max_length=99999999, blank=True, null=True)# Descripción y detalles extras de la carrera

	def __str__(self):
		str = '%s - %s' % (self.fecha.strftime('%d/%m/%y'), self.titulo)
		return str.upper()

	def save(self, *args, **kwargs):
		if self.foto != None:
			foto2 = Imagen.objects.filter(id=self.foto_id)
			self.cartel = '/'+foto2.get().imagen.name
		else:
			self.cartel = '/static/img/imagenes/nofoto.jpg'
		super(Carrera, self).save(*args, **kwargs)


class Album(models.Model):
	nombre = models.CharField(max_length=250)
	direccion = models.CharField(max_length=400)
	foto = models.ImageField(default='nofoto.jpg',upload_to='static/img/fotografos', null=True)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name_plural = "Albumes"

class Participante(models.Model):
	p_carrera_id = models.ForeignKey(Carrera, on_delete=models.DO_NOTHING, blank=True, null=True)
	lista = RichTextField(max_length=99999999,blank=True, null=True)
	fecha = models.DateTimeField(auto_now=True)
	Caducada = models.BooleanField(default=False)
	def __str__(self):
		return str(self.p_carrera_id.fecha.strftime("%d/%m/%y"))+"  -  "+str(self.p_carrera_id.titulo)

class Liga(models.Model):
	lista = RichTextField(max_length=99999999,blank=True, null=True)
	fecha = models.DateTimeField(auto_now=True)

	def __str__(self):
		return str(self.fecha.strftime("%d/%m/%y"))+"  -  "+str('LIGA')

class GaleriaFoto(models.Model):
	carrera = models.ForeignKey(Carrera, on_delete=models.DO_NOTHING, blank=True, null=True)
	galeria = models.CharField(max_length=9999,blank=True, null=True)
	detalles = models.CharField(max_length=9999,blank=True, null=True)

	def __str__(self):
	    return str(self.carrera)

class Comentario(models.Model):
	comentario = models.TextField(max_length=9999)
	usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	carrera = models.ForeignKey(Carrera, on_delete=models.DO_NOTHING)
	fecha = models.DateTimeField(default=now())

	def __str__(self):
	    return str(self.fecha.strftime('%d/%m/%y ') + " - " + self.usuario.username + " - " +self.carrera.titulo)


lista= list(range(1,11))
puntos = [  (i,i) for i in lista ]


class Patrocinador(models.Model):
	titulo = models.CharField(max_length=250)
	foto = models.ForeignKey(Imagen, on_delete=models.DO_NOTHING, blank=True, null=True)
	cartel = models.CharField(max_length=250, blank=True, null=True)
	texto = RichTextField(max_length=99999999)

	def save(self, *args, **kwargs):
		if self.foto != None:
			foto2 = Imagen.objects.filter(id=self.foto_id)
			self.cartel = '/'+foto2.get().imagen.name
		else:
			self.cartel = 'static/img/logo1.jpg'
		super(Patrocinador, self).save(*args, **kwargs)

class Puntuacion(models.Model):
	puntuacion = models.IntegerField(choices=puntos, default=5)
	usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	carrera = models.ForeignKey(Carrera, on_delete=models.DO_NOTHING)
	fecha = models.DateTimeField(default=now())
	class Meta:
		unique_together=("usuario","carrera")

	def __str__(self):
	    return str(self.fecha.strftime('%d/%m/%y ') + " - " + self.usuario.username + " - " +self.carrera.titulo)

	class Meta:
		verbose_name_plural = "Puntuaciones"

@receiver(post_delete, sender=Imagen)
def imagen_delete(sender, instance, **kwargs):
    instance.imagen.delete(False)


@receiver(post_delete, sender=Resultado)
def resultado_delete(sender, instance, **kwargs):
    instance.resultado.delete(False)



