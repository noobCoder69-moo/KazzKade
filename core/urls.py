from django.urls import path
from . import views

urlpatterns = [
    # auth
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # posts
    path("posts/", views.post_view, name="posts"),  
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),  

    # comments
    path("posts/<int:post_id>/comments/", views.comment_view, name="comments"),  
    path("comments/<int:comment_id>/", views.comment_details, name="comment_detail"),  

    # likes
    path("<str:content_type>/<int:object_id>/like/", views.like_view, name="like"),  

    # follow toggle
    path("users/<int:user_id>/follow/", views.follow_toggle, name="follow_toggle"),

    # profile
    path("users/<int:user_id>/", views.profile_view, name="profile_view"),
    path("profile/", views.profile_detail, name="profile_detail"),  
]
