from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import  ProductStatisticsSerializer, LessonSerializer
from rest_framework.response import Response
from .models import Lesson, Product, ProductAccess

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
    
"""
This Class returns API with the following:
A list of all products on the platform, width an attached information to each product:
    a. Number of lessons watched by all students.
    b. How much time did all students spend watching the videos in total?
    c. Number of students working on the product. Product purchage percentage (calculated based on the number of accesses received to the product divided by the total number of users on the platform).
"""

class ProductStatisticsAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductStatisticsSerializer(products, many=True)
        return Response({
            'products_count':products.count(),
            'products': serializer.data,
        })
