from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from disciplinas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('disciplinas/', include('disciplinas.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),

    path('', RedirectView.as_view(url='/accounts/login/', permanent=True), name='home'),
    path('minha_plataforma_inicial/', views.minha_plataforma_inicial, name='minha_plataforma_inicial'), 
]