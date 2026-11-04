from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "user", "book", "created_at", "end_at", "plated_end_at"]
        extra_kwargs = {
            "user": {"required": True},
            "book": {"required": True},
        }

    def create(self, validated_data):
        if not validated_data.get("plated_end_at"):
            validated_data["plated_end_at"] = timezone.now() + timedelta(days=14)

        return super().create(validated_data)


class UserOrderSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        read_only_fields = ["user"]
