from django.urls import path, include

urlpatterns = [
    path('main/', include(('main.urls', 'main'), namespace='main')),
]
