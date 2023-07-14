from rest_framework import viewsets, permissions
from .models import PageView
from .serializers import PageViewSerializer


class PageViewViewSet(viewsets.ModelViewSet):
    queryset = PageView.objects.all()
    serializer_class = PageViewSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'update', 'partial_update', 'destroy'):
            # Только администратор может читать, обновлять и удалять
            return [permissions.IsAdminUser(), ]
        return [permissions.AllowAny(), ]

