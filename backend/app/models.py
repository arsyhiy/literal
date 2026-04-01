import uuid

from django.db import models


class author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255, default="anonymous"
    )  # было решено оставить так как не вижу смысла делать несколько полей может конечно будет причина пока невижу.
    image = models.ImageField(blank=True)  #  надо написать дефолтный вариант

    def __str__(self):
        return self.name


class publisher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default="noname")
    image = models.ImageField(blank=True)  #  надо написать дефолтный вариант

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, default="noname")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default="unknown")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(null=False, blank=False)
    description = models.TextField(
        null=False,
        blank=False,
        max_length=1000,  # решил оставить один милион как максимальное значение
    )
    image = models.ImageField(blank=True)  #  надо написать дефолтный вариант
    weight = models.DecimalField(
        max_digits=1000, decimal_places=2, null=False, blank=False
    )
    ageRestrictions = models.IntegerField(null=False, blank=False)
    yearOfPublication = models.IntegerField(null=False, blank=False)
    size = models.CharField(null=False, blank=False)
    manufacturer = models.ForeignKey(
        publisher, on_delete=models.CASCADE, related_name="product"
    )

    def __str__(self):
        return self.name


class Book(Product):
    author = models.ForeignKey(author, on_delete=models.CASCADE, related_name="author")
    isbn = models.CharField(
        max_length=20, blank=False
    )  # честно представления не имею какая должна быть длина isbn

    coverType = models.CharField(max_length=100, null=False, blank=False)
    numberOfPages = models.IntegerField(default=1)


class BoardGame(Product):
    players = models.CharField(
        max_length=255
    )  # кто его знает сколько может играть в одну игру множество людей

    timeOfPlaying = models.IntegerField(default=1)
