"""djangogoat URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.views.generic import TemplateView
from django.views.static import serve
from django.urls import (
    include,
    path,
    re_path,
)

from authentication import views as auth_views
from notes import views as notes_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Notes pages
    path('dash/', notes_views.dash, name='dash'),
    path(
        'conversation/<friend_pk>',
        notes_views.conversation,
        name='conversation'
    ),
    path('note/<pk>', notes_views.note, name='note'),
    path('write-note/', notes_views.write_note, name='write-note'),

    # Unauthenticated pages
    path('vulnerabilities',
         TemplateView.as_view(template_name='vulnerabilities.html'),
         name='vulnerabilities'),
    path(
        '',
        TemplateView.as_view(template_name='landing.html'),
        name='landing'
    ),
    path(
        'instructions',
        TemplateView.as_view(template_name='instructions.html'),
        name='instructions'
    ),

    # Authentication and user management pages
    path('login/', auth_views.log_in, name='login'),
    path('logout/', logout_then_login, {'login_url': 'login'}, name='logout'),
    path('profile/<pk>', auth_views.profile, name='profile'),
    path('profile-update', auth_views.profile_update, name='profile-update'),
    path('sign-up/', auth_views.sign_up, name='sign-up'),
    path('', include('django.contrib.auth.urls')),

    # Media files
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT}
    ),
]
