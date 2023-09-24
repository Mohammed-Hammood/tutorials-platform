from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import  ProductStatisticsSerializer, LessonSerializer
from rest_framework.response import Response
from .models import Lesson, Product, ProductAccess, LessonProgress
from django.db.models import Sum

"""

Реализовать API для выведения списка всех уроков по всем продуктам к которым пользователь имеет доступ, с выведением информации о статусе и времени просмотра.
1. Implement an API to display a list of all lessons for all products to which the user has access,  displaying information about the status and viewing time.


Реализовать API с выведением списка уроков по конкретному продукту к которому пользователь имеет доступ, с выведением информации о статусе и времени просмотра, а также датой последнего просмотра ролика.
2. Implement an API that displays a list of lessons for a specific product to which the user has access, 
   displaying information about the status and time of viewing, as well as the date of the last viewing of the video.


Реализовать API для отображения статистики по продуктам. Необходимо отобразить список всех продуктов на платформе, к каждому продукту приложить информацию:
3. Implement an API to display product statistics. 
It is necessary to display a list of all products on the platform, attaching information to each product:


Количество просмотренных уроков от всех учеников.
a. Number of lessons watched by all students.


Сколько в сумме все ученики потратили времени на просмотр роликов.
b. How much time did all students spend watching the videos in total?

Количество учеников занимающихся на продукте.
Процент приобретения продукта (рассчитывается исходя из количества полученных доступов к продукту деленное на общее количество пользователей на платформе).

c. Number of students working on the product.
Product acquisition percentage (calculated based on the number of accesses received to the product divided by the total number of users on the platform).

"""

class LessonsListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # returns list of products ids [1, 2, ..]
        products = ProductAccess.objects.filter(user=request.user).values_list('product', flat=True)
        lessons = Lesson.objects.filter(products__in=products).distinct()
        serializer = LessonSerializer(lessons, many=True)
        return Response({
            'lessons_count': lessons.count(),
            'lessons': serializer.data
        })
    


class ProductLessonsListAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id:int):
        try:
            access = ProductAccess.objects.get(product__id=int(product_id), user=request.user)
        except ProductAccess.DoesNotExist:
            return Response({
                'error': 'Product may not exist or you do not have access to this product'
            }, status=400)
        queryset:list[Lesson] = access.product.lessons
        serializer = LessonSerializer(queryset, many=True)
        return Response({
            'lessons_count': queryset.count(),
            'lessons': serializer.data,
        })
    

class ProductStatisticsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductStatisticsSerializer(products, many=True)
        total_watched_time = LessonProgress.objects.aggregate(total_watched_time=Sum('watched_time'))
        return Response({
            **total_watched_time,
            'products_count':products.count(),
            'products': serializer.data,
        })
