from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from tastecategories.models import TasteCategories
from tastecategories.serializers import TasteCategoriesSerializer


class TasteCategoryCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TasteCategories.objects.all()
    serializer_class = TasteCategoriesSerializer
