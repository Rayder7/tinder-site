from django.urls import include, path

from api.views import RegistrationView, UserViewSet

urlpatterns = [
    #  api
    path('list', UserViewSet.as_view(), name='list'),
    path('clients/create',
         RegistrationView.as_view({'post': 'create'}),
         name='create'),
    path('clients/<int:id>/match',
         RegistrationView.as_view({'post': 'match'}),
         name='match'),
    #  auth
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls.authtoken')),
]
