import uuid
from django.db import models

class author(models.Model):
    name = models.CharField(max_length=255)




    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255) 
    details = models.CharField(max_length=1000)# найти подходящий максимальный размер
    #specifications = models.JSONField(default=dict, blank=True, help_text="Характеристики книги в формате JSON")
    image = models.ImageField(blank=True)
    author = models.ForeignKey(author, on_delete=models.CASCADE, related_name='books')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title



