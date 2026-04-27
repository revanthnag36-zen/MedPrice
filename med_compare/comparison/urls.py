from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),

    path('search/', views.search_medicine, name='search_medicine'),
    path('search-problem/', views.search_by_problem, name='search_by_problem'),

    # AUTH
    path('login/', auth_views.LoginView.as_view(template_name='comparison/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    # REGISTER
    path('register/', views.register, name='register'),

    # HISTORY (THIS FIXES YOUR ERROR)
    path('history/', views.history, name='history'),
    #for deleting history
    path('delete-history/<int:id>/', views.delete_history, name='delete_history'),
]