from django.db import models
from django.contrib.auth.models import User

# Create your models here.
select_documentos = [
    ('Estudio','Estudio'),
    ('Actividades de Aprendizaje','Actividades de Aprendizaje'),
    ('Reuniones','Reuniones'),
    ('Resumenes','Resumenes'),
    ('Experiencias','Experiencias')
    ] 


class Documentos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_doc = models.AutoField(primary_key=True)
    tipo_doc = models.CharField(max_length=50, choices=select_documentos)
    link_doc = models.CharField(max_length=250)

    def __str__(self):
        texto = "{0}({1})"
        return texto.format(self.user, self.id_doc, self.tipo_doc, self.link_doc)