from django.urls import path

from . import views

urlpatterns = [
    # generic list/create endpoint
    path("", views.FeatureView.as_view(), name="features"),

    # user-specific feature endpoint (user_id and feature name from URL)
    path("all/", views.FeaturesView.as_view(), name="features-list"),
    path("user/<str:feature>/", views.UserFeatureView.as_view()),
    path("<str:feature>/", views.FeatureView.as_view()),
]