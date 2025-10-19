from django.contrib.auth.models import User
from rest_framework import serializers

class AdminUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

    def get_role(self, obj: User) -> str:
        return 'admin' if obj.is_staff or obj.is_superuser else 'user'

class AdminUserUpdateSerializer(serializers.ModelSerializer):
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'role']

    def update(self, instance: User, validated_data):
        role = validated_data.pop('role', None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if role is not None:
            instance.is_staff = True if role == 'admin' else False
        instance.save()
        return instance
