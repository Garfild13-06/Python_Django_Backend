from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from users.views import CustomLimitOffsetPagination
from tobaccos.models import Tobaccos
from tobaccos.serializers import TobaccosListSerializer, TobaccosSerializer


# Create your views here.
# TobaccoViewSet
class TobaccoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Tobaccos.objects.all()
    serializer_class = TobaccosListSerializer
    pagination_class = CustomLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        search_query = request.data.get('search', None)

        if search_query:
            queryset = self.queryset.filter(
                Q(taste__icontains=search_query) | Q(description__icontains=search_query)
            )
        else:
            queryset = self.queryset

        queryset = queryset.order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "status": "ok",
            "code": 200,
            "message": "Список табаков успешно получен",
            "data": serializer.data
        }, status=200)


# 🔹 Создание табака
class TobaccoCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tobaccos.objects.all()
    serializer_class = TobaccosSerializer
