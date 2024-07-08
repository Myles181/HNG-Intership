from django.urls import path
from .views import (
    register_view,
    login_view,
    user_detail_view,
    organisation_list_create_view,
    organisation_detail_view,
    add_user_to_organisation_view
)

urlpatterns = [
    path('auth/register', register_view, name='register'),
    path('auth/login', login_view, name='login'),
    path('users/<str:id>', user_detail_view, name='user-detail'),
    path('organisations', organisation_list_create_view, name='organisation-list'),
    path('organisations/<str:orgId>', organisation_detail_view, name='organisation-detail'),
    path('organisations/<str:orgId>/users', add_user_to_organisation_view, name='add-user-to-organisation'),
]
