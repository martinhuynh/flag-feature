from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Features, FeatureFlag, Status
import json

# Create your views here.
class FeatureView(generics.GenericAPIView):
    def get(self, request, feature=None):
        if feature is not None:
            return JsonResponse({
                "status": FeatureFlag.is_feature_enabled(feature, request.user),
                "user_id": request.user.id,
                "feature": feature
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "Hello, World!", "user_id": request.user.id}, status=status.HTTP_200_OK)
    
    def put(self, request, feature=None):
        if feature is not None:
            description = request.data.get("description", "")
            newFeature = Features(feature=feature, description=description)
            if (Features.get_feature(feature_name=feature) is not None):
                return JsonResponse({
                    "message": f"Feature '{feature}' already exists",
                }, status=status.HTTP_200_OK)
            else:
                newFeature.save()
                return JsonResponse({
                    "message": f"Feature has been created!",
                }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"message": "Feature name is required in the URL."}, status=status.HTTP_400_BAD_REQUEST)

class FeaturesView(generics.GenericAPIView):
    # features/ - GET - Get the list of all features
    def get(self, request):
        features = Features.objects
        return JsonResponse({
            "features": list(features.values()),
        }, status=status.HTTP_200_OK)
    
class UserFeatureView(generics.GenericAPIView):
    # features/{userId}/{feature} - GET - Get the status of a feature for a user
    def get(self, request, feature):
        return JsonResponse({
            "status": FeatureFlag.is_feature_enabled(feature, request.user),
            "user_id": request.user.id,
            "feature": feature
        }, status=status.HTTP_200_OK)
    
    # features/user/{feature} - PUT - Enable a feature for a user providing the feature name in the request body
    def put(self, request, feature):
        try:
            feature_obj = Features.objects.get(feature=feature)
            status = Status(request.data.get("status", Status.Inactive))
            feature_flag, created = FeatureFlag.objects.update_or_create(feature=feature_obj, user_id=request.user.id, status=status)
            feature_flag.save()

            return JsonResponse({
                "message": f"Feature '{feature}' is now {feature_flag.status} for user {request.user.id}",
            }, status=status.HTTP_200_OK)
        except (Features.DoesNotExist, FeatureFlag.DoesNotExist):
            return JsonResponse({
                "message": f"Feature '{feature}' does not exist or is not enabled for user {request.user.id}",
            }, status=status.HTTP_404_NOT_FOUND)
    
# features/{userId} - GET - Get the list of features enabled for a user
# features/{userId} - POST - Enable a feature for a user providing the feature name in the request body
