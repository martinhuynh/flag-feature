from django.db import models
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status

# List of features that we want to enable/disable for users.
class Features(models.Model):
    class Feature(models.TextChoices):
        FeatureA = "FA", _("FeatureA")
        FeatureB = "FB", _("FeatureB")

    feature = models.CharField(choices=Feature.choices)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)

    @staticmethod
    def get_feature(feature_name):
        try:
            return Features.objects.get(feature=feature_name)
        except Features.DoesNotExist:
            return None

# This will be used to enable/disable a feature for a specific user.
class FeatureFlag(models.Model):
    class Status(models.TextChoices):
        Active = "AC", _("Active")
        Inactive = "IN", _("Inactive")
        
    user_id = models.IntegerField(null=False, blank=False, default=-1)
    feature = models.ForeignKey(Features, on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, default=Status.Inactive)
    created_date = models.DateField(auto_now_add=True)

    @staticmethod
    def is_feature_enabled(feature_name, user):
        try:
            if Features.objects.filter(feature=feature_name).exists() is False:
                None
            
            feature = Features.objects.get(feature=feature_name)
            feature_flag = FeatureFlag.objects.get(feature=feature, user=user)
            return feature_flag.status == FeatureFlag.Status.Active
        except (Features.DoesNotExist, FeatureFlag.DoesNotExist):
            return None

# This will be used to enable/disable a feature globally for all users.
# If a feature is disabled globally, it will be disabled for all users 
# regardless of their individual feature flags.
class GlobalFeatureFlag(models.Model):
    class Status(models.TextChoices):
        Active = "AC", _("Active")
        Inactive = "IN", _("Inactive")
        
    feature = models.ForeignKey(Features, on_delete=models.CASCADE)
    status = models.CharField(choices=Status.choices, default=Status.Inactive)
    created_date = models.DateField(auto_now_add=True)