"""
URL configuration for aplicativo_pos_hc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pos.urls')),  # Incluye las URLs de la aplicación 'pos'
]

# pos/views.py



def home(request):
    # Lógica para la vista de la página de inicio
    return render(request, 'pos/home.html')

def product_list(request):
    # Lógica para la vista de la lista de productos
    products = Product.objects.all()  # Obtén todos los productos desde la base de datos
    return render(request, 'pos/product_list.html', {'products': products})
