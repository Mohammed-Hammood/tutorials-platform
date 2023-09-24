from rest_framework import serializers
from .models import Product, Lesson, LessonProgress, ProductAccess
from django.db.models import Sum
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('__all__')

 
class LessonProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = ['id', 'watched_time', 'view_status', ]


class LessonSerializer(serializers.ModelSerializer):
    info = LessonProgressSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ('__all__')


class ProductStatisticsSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()
    owner = serializers.StringRelatedField()
    
    def get_lessons(self, product:Product):
        count:int = product.lessons.filter(info__view_status='viewed').count()
        lessons_ids = product.lessons.values_list("id")
        total_watched_time:dict[str, int] = LessonProgress.objects.filter(lesson_id__in=lessons_ids).aggregate(total_watched_time=Sum('watched_time'))
        total_students_count:int = ProductAccess.objects.filter(product=product).count()
        total_users_count:int = User.objects.count()
        product_purchase_percentage:float =  round(100 * (total_students_count / total_users_count), 2)
        return {
            **total_watched_time,
            'viewed_lessons_count': count,
            'total_students_count': total_students_count,
            'product_purchase_percentage': product_purchase_percentage,
            }
    
    class Meta:
        model = Product
        fields = ['id', 'owner', 'title', 'lessons', 'created_at', 'updated_at']