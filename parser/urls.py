from rest_framework.routers import DefaultRouter

from parser.views import views

router = DefaultRouter()
router.register('sources', views.SourceViewSet, 'sources')

urlpatterns = []
urlpatterns += router.urls
