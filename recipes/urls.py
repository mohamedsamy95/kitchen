'''
Written by Samy <m.elsisi1995@gmail.com> on Wed 09.05.2023
Version 1.0
'''
from . import views as v
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'api/recipes', v.RecipeViewSet, basename='recipe')
urlpatterns = router.urls