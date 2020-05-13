from rest_framework import viewsets, status, generics, mixins, filters
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters import rest_framework as filters1
from events_api.filter import EventFilter
from events_api.models import Event
from events_api.permissions import IsAuthorOfEvents
from events_api.serializers import EventSerializer
from rest_framework.response import Response


# import django_filters.rest_framework


class EventGenericView(viewsets.GenericViewSet, mixins.ListModelMixin,
                       mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    serializer_class = EventSerializer
    # queryset = Event.objects.all()
    auth_methods = ('POST', 'PUT', 'DELETE', 'PATCH')
    search_fields = ['title']
    filter_backends = (filters.SearchFilter, filters1.DjangoFilterBackend)
    filter_class = EventFilter

    def get_queryset(self):
        queryset = Event.objects.all()
        # title = self.request.query_params.get('title').strip()
        event_date = self.request.query_params.get('event_date')

        if event_date:
            queryset.filter(event_date__contains=event_date)

        # if date_event:

        return queryset

    def get_permissions(self):
        if self.request.method in self.auth_methods:
            permission_classes = [IsAuthorOfEvents]
            return [permission() for permission in permission_classes]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            author = self.request.user
        except Exception as error:
            content = {'error': 'авторизируйтесь чтобы создать событие'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        serializer.save(author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
