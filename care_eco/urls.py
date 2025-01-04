"""care_eco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

# from vote.views import admin_stats, generate_otp, get_candidates, submit_vote, verify_otp
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from vote import views
# from django.http import HttpResponse

# # Add a simple view for the base URL
# def home_view(request):
#     return HttpResponse("Welcome to the Online Voting System!")

urlpatterns = [
    # path('', views.index, name='index'),  # Home page for rendering the HTML template
    path('', views.home, name='home'),  # Login page as the homepage
    path('login/', auth_views.LoginView.as_view(template_name='voting/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('generate_otp/', views.generate_otp, name='generate_otp'),  # Endpoint for OTP generation
    path('verify_otp/', views.verify_otp, name='verify_otp'),  # Endpoint for OTP verification
    path('get_candidates/', views.get_candidates, name='get_candidates'),  # Fetch candidates based on constituency
    path('submit_vote/', views.submit_vote, name='submit_vote'),  # Endpoint for submitting votes
    path('admin_stats/', views.admin_stats, name='admin_stats'),  # Admin statistics for a constituency
    # path('login/', auth_views.LoginView.as_view(template_name='voting_app/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('login/', auth_views.LoginView.as_view(template_name='voting_app/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('dashboard/', views.dashboard, name='dashboard'),
]

# # URLs (Add these to your urls.py)
# urlpatterns = 
#     path('admin/', admin.site.urls),
#     path('vote/', include('vote.urls')),
#     # path('generate-otp/', generate_otp),
#     # path('verify-otp/', verify_otp),
#     # path('get-candidates/', get_candidates),
#     # path('submit-vote/', submit_vote),
#     # path('admin-stats/', admin_stats),
# 
# urlpatterns = [
#     # path('generate-otp/', views.generate_otp),
#     # path('verify-otp/', views.verify_otp),
#     # path('get-candidates/', views.get_candidates),
#     # path('submit-vote/', views.submit_vote),
#     # path('admin-stats/', views.admin_stats),
#     path('', views.home_view),
# ]
