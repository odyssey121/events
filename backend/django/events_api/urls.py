from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter
from events_api.views import EventGenericView

router = DefaultRouter()
router.register('events', EventGenericView, basename='events')

urlpatterns = [
    url('', include(router.urls)),
]
