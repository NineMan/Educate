from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Subject(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='courses_created')
    subject	= models.ForeignKey(Subject, on_delete=models.DO_NOTHING, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    module = models.ForeignKey(Module, on_delete=models.DO_NOTHING, related_name='contents')
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.DO_NOTHING,
                                     limit_choices_to={'model__in': ('text',
                                                                     'video',
                                                                     'image',
                                                                     'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='%(class)s_related')
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    content = models.FileField(upload_to='files')


class Image(ItemBase):
    content = models.FileField(upload_to='images')


class Video(ItemBase):
    models.URLField()

