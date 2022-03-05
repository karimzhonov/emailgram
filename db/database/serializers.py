from rest_framework import serializers
from .models import User, Mail

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class MailSerializers(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = "__all__"
