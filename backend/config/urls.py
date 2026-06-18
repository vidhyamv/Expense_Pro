from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({
        'message': 'Expense Tracker API',
        'endpoints': {
            'admin': '/admin/',
            'categories': '/api/categories/',
            'expenses': '/api/expenses/',
            'expense_stats': '/api/expenses/stats/',
        }
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include('expenses.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)