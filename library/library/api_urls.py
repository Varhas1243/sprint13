from django.urls import path

from authentication.api_views import UserAPIView
from author.api_views import AuthorAPIView
from book.api_views import BookAPIView
from order.api_views import OrderAPIView, UserOrderAPIView

urlpatterns = [
    path("user/", UserAPIView.as_view()),
    path("user/<int:pk>/", UserAPIView.as_view()),
    path("user/<int:user_id>/order/", UserOrderAPIView.as_view()),
    path("user/<int:user_id>/order/<int:pk>/", UserOrderAPIView.as_view()),
    path("order/", OrderAPIView.as_view()),
    path("order/<int:pk>/", OrderAPIView.as_view()),
    path("book/", BookAPIView.as_view()),
    path("book/<int:pk>/", BookAPIView.as_view()),
    path("author/", AuthorAPIView.as_view()),
    path("author/<int:pk>/", AuthorAPIView.as_view()),
]
