import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(null=True, blank=True, default="images/default.png")

    def __str__(self):
        return self.name


class Publisher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    image = models.ImageField(null=True, blank=True, default="images/default.png")

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField(null=False, blank=False)
    description = models.TextField(max_length=1000, default="no description")
    image = models.ImageField(null=True, blank=True, default="images/default.png")

    weight = models.DecimalField(
        max_digits=1000, decimal_places=2, null=False, blank=False
    )
    ageRestrictions = models.IntegerField(null=False, blank=False)
    yearOfPublication = models.IntegerField(null=False, blank=False)
    size = models.CharField(null=False, blank=False)
    manufacturer = models.ForeignKey(
        Publisher, on_delete=models.CASCADE, related_name="product"
    )
    created_at = models.DateTimeField(default=timezone.now)
    sold_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Book(Product):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")
    isbn = models.CharField(max_length=20, null=False, blank=False)

    coverType = models.CharField(max_length=100, null=False, blank=False)
    numberOfPages = models.IntegerField(null=False, blank=False)


class BoardGame(Product):
    players = models.CharField(max_length=255)

    timeOfPlaying = models.IntegerField(null=False, blank=False)


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "Новый"
        PROCESSING = "processing", "В обработке"
        SHIPPED = "shipped", "Отправлен"
        DONE = "done", "Завершён"
        CANCELED = "canceled", "Отменён"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders"
    )

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)

    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def update_total(self):
        self.total = sum(item.get_total_price() for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Order {self.id} ({self.status})"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="order_items"
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.price * self.quantity

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
