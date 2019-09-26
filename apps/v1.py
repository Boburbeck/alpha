from django.urls import path, include

urlpatterns = [
    path('main/', include(('main.urls', 'main'), namespace='main')),
    path('stats/', include(('stats.urls', 'stats'), namespace='stats')),
    path('stock/', include(('stock.urls', 'stock'), namespace='stock')),
    path('finance/', include(('finance.urls', 'finance'), namespace='finance')),
]
