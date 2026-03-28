from os import name
import uuid
from django.db import models
#from django.contrib.postgres.fields import JSONField  # если PostgreSQL

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255) 
    details = models.CharField(max_length=1000)# найти подходящий максимальный размер
    #specifications = JSONField(default=dict, blank=True, help_text="Характеристики книги в формате JSON")
    
    def __str__(self):
        return self.title
    
class bookstore(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=255)#, unique=True) 

    def __str__(self):
        return self.address

# class StoreStorage(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     store_id= bookstore.id

    
    
