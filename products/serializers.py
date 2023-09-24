from rest_framework import serializers
from .models import Product, Lesson, LessonProgress


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



class ProductStatisticsSerializer(serializers.Serializer):
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'owner']