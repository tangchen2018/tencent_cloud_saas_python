
from django.urls import path,include
from .saas import urls as saas_urls

urlpatterns = [
    path('saas/', include(saas_urls))
]
