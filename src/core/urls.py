"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordChangeDoneView, PasswordChangeView,  PasswordResetCompleteView,  \
    PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('accounts/', include('accounts.urls')),
    path('accounts/change/', PasswordChangeView.as_view(), name='password_change'),
    path('accounts/change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('accounts/reset/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('quiz/', include('quiz.urls')),
]
# path('accounts/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
