from __future__ import unicode_literals

from django.conf import settings

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from  django.core.validators import RegexValidator
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username = username,
            email=self.normalize_email(email),
            # date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username,
            email,
            password=password,
            # date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

USERNAME_REGEX = '^[a-zA-Z0-9.@+-]*$'

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=120,
                                validators=[
                                RegexValidator(
                                    regex = USERNAME_REGEX,
                                    message = "Username must be alphanumeric.",
                                    code = "invalid_username"
                                )],
                                unique = True,)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    # date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    # USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['date_of_birth']
    REQUIRED_FIELDS = ['email']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

def download_media_location(isinstance, nombre_archivo):
    return "%s/%s" %(isinstance.id, nombre_archivo)

class Producto(models.Model):
    #usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
    administradores = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                             related_name='administradores_producto',
                                             blank=True)#related_name=administradores_producto
    media = models.FileField(blank=True, null=True,
                             upload_to=download_media_location,
                             storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    nombre  = models.CharField(max_length = 40)
    slug  = models.SlugField(blank=True, unique=True)
    descripcion = models.TextField(null=True)
    precio = models.DecimalField(max_digits=9999, decimal_places=2)
    precio_oferta = models.DecimalField(max_digits=9999, decimal_places=2,
                                        null=True, blank=True)
    tipo = models.CharField(max_length = 40, blank=True, null=True, default="foto")

    def __unicode__(self):
        return self.nombre

    def get_absolute_url(self):
        print "URL absoluto"
        view_name = "productos:detalle_slug"
        return reverse(view_name, args=[str(self.slug)])

    def get_download(self):
        view_name = "productos:download_slug"
        url = reverse(view_name, args=[str(self.slug)])
        return url


def create_slug(instance, nuevo_slug=None):
    slug = slugify(instance.nombre)
    if nuevo_slug is not None:
        slug = nuevo_slug

    qs = Producto.objects.filter(slug=slug)
    existe = qs.exists()
    if existe:
        nuevo_slug = "%s-%s" %(slug, qs.last().id)
        return create_slug(instance, nuevo_slug=nuevo_slug)

    return slug

def producto_pre_save_reciever(sender, instance, *args, **kwargs):
    print sender
    print instance

    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(producto_pre_save_reciever, sender=Producto)


class MisProductos(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL)
    productos = models.ManyToManyField(Producto, blank=True)

    def __unicode__(self):
        return "%s" %(self.productos.count())

    class Meta:
        verbose_name = "Mis Productos"
        verbose_name_plural = "Mis Productos"
