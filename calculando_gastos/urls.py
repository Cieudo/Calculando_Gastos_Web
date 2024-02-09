from django.contrib import admin
from django.urls import path
from app_calculando_gastos import views
from app_calculando_gastos.views import delete_gasto


app_name = 'calculadora'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_login, name='login'),
    path('login/', views.login, name='login'),
    path('registro/', views.registrar, name='registrar'),  # Corrigido para 'registrar'
    path('confirmacao/', views.confirmacao, name='confirmacao'),
    path('', views.home, name='home'),
    path('processar_gastos/', views.processar_gastos, name='processar_gastos'),
    path('delete_gasto/<int:gasto_id>/', delete_gasto, name='delete_gasto'),
    path('index/', views.index, name='index'),

]
