from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/products/")
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True, max_length=5000)

    def __str__(self) -> str:
        return self.title


    def get_absolute_url(self):
        return reverse("products:product-detail", kwargs={"pk": self.pk})


class Lesson(models.Model):

    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video_url = models.URLField()
    products = models.ManyToManyField(Product, related_name='lessons')
    image = models.ImageField(null=True, blank=True, upload_to="images/lessions/")
    duration = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(null=True, blank=True, max_length=5000)

    def __str__(self) -> str:
        return self.title

 

    def get_absolute_url(self):
        return reverse("products:lession-detail", kwargs={"pk": self.pk})


class ProductAccess(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'user {self.user.id} has access to product {self.product.title}'


class LessonProgress(models.Model):
    view_choices = (
        ('not_viewed', 'Not viewed'),
        ('viewed', 'Viewed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='info')
    watched_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_status = models.CharField(max_length=100, choices=view_choices, default=view_choices[0])

    def __str__(self):
        return self.lesson.title
    
    def save(self, *args, **kwargs):
        if self.view_status == 'not_viewed' and self.watched_time / self.lesson.duration >= 0.8:
            self.view_status = 'viewed'
        super(LessonProgress, self).save(*args, **kwargs)
