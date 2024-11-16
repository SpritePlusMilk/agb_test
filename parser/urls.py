from django.urls import path
from rest_framework.routers import DefaultRouter

from parser import views

router = DefaultRouter()
router.register('sources', views.SourceViewSet, 'sources')

urlpatterns = [
    path('example', views.example_view),
]
urlpatterns += router.urls
