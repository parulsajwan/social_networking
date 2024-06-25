from django.urls import path
from .views import (
    SignupView,
    LoginView, 
    SearchView, 
    RequestListSentView, 
    RequestAcceptRejectView,
    ReceivedRequestListView
    )

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', SearchView.as_view(), name='search'),
    path('sent-request/', RequestListSentView.as_view(), name='sent-request'),
    path('action-request/<int:user_id>/', RequestAcceptRejectView.as_view(), name='action-request'),
    path('accepted-requests/', RequestListSentView.as_view(), name='accepted-requests'),
    path('action-on-request/', RequestAcceptRejectView.as_view(), name='action-on-request'),
    path('all-request/', ReceivedRequestListView.as_view(), name='all-request'), 
    path('reject-request/<int:pk>/', RequestAcceptRejectView.as_view(), name='reject-request'),
]
