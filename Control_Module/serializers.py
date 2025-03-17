from rest_framework import serializers
from . import models




class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = '__all__'




class AppConfingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppConfing
        fields = '__all__'




class DailybonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dailybonus
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_staff:
            return super().create(validated_data)
        raise serializers.ValidationError("Only admins can create daily bonuses.")



class tasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.tasks
        read_only_fields = ('title','user','gift_coin','link',)
        fields = '__all__'



class adminalertserizlizer(serializers.ModelSerializer):
    class Meta:
        model = models.Adminalert
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        # Automatically assign the user from the request
        request = self.context.get('request')
        user = request.user
        return models.Adminalert.objects.create(user=user, **validated_data)

