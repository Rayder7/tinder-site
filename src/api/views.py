from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.filters import UserSetFilter
from api.serializers import UserCreateSerializer, UserSerializer
from api.utils import send_message
from users.models import Follow

User = get_user_model()

load_dotenv()


class RegistrationView(viewsets.ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

    @action(detail=False,
            methods=['post'],
            url_path='create',
            permission_classes=AllowAny)
    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['post'],
            url_path='match',
            permission_classes=IsAuthenticated)
    def match(self, request, id):
        if request.user.id == id:
            return Response({'message': 'Себя выбрать нельзя(('},
                            status=status.HTTP_409_CONFLICT)
        followed = User.objects.get(id=id)
        match_1, _ = Follow.objects.get_or_create(follower=request.user,
                                                  followed=followed)
        match_2 = Follow.objects.filter(follower__id=id,
                                        followed=request.user).first()
        if match_1 and match_2:
            send_message(match_1.follower, match_1.followed)
            send_message(match_2.follower, match_2.followed)
            return Response({'email': match_1.followed.email})
        return Response()


class UserViewSet(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = UserSetFilter
