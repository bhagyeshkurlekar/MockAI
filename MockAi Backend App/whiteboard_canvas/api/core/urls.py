from .views import LoginViewset, RegisterViewset, ConversationViewset
from django.urls import path

urlpatterns = [
    path('register/', RegisterViewset.as_view(
        {
            'post': 'post_register'
        }
    ), name='register'),

    path('login/', LoginViewset.as_view(
        {
            'post': 'post_login'
        }
    ), name='login'),

    path('submit/', ConversationViewset.as_view(
        {
            'post': 'post_question'
        }
    ), name='submit'),

    path('', ConversationViewset.as_view(
        {
            'get': 'get_conversation'
        }
    ), name='conversation')
]