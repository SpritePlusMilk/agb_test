from rest_framework.routers import DefaultRouter

from parser import views

router = DefaultRouter()
router.register('sources', views.SourceViewSet, 'sources')

urlpatterns = []
urlpatterns += router.urls
