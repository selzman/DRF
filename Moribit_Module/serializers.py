from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from .models import User, ReferralGift, VideoSentForCheck ,webappusercode ,userdaily ,chatbot



class CodeCheckSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)




class usercodeCheckSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=100)











class UserSerializer(serializers.ModelSerializer):
    referralCode = serializers.IntegerField(write_only=True, required=False, default=0)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = (
            'last_login',
            'is_superuser',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'date_joined',
            'referral_code',
            'level',
            'level_xp',
            'blue_tick',
            'coin'
        )

    def create(self, validated_data):
        referral_code_input = validated_data.pop('referralCode', None)

        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        if referral_code_input:
            referred_by = User.objects.filter(referral_code=referral_code_input).first()

            if referred_by:
                try:
                    referral_settings = ReferralGift.objects.get()
                    user.referred_by = referred_by
                    referred_by.coin += referral_settings.referral_coin_amount
                    referred_by.save()
                    user.coin +=30000
                    user.save()
                except ReferralGift.DoesNotExist:
                    pass
                except Exception as e:
                    pass
            else:
                pass

        return user











class LoginSerializer(serializers.Serializer):
    User = get_user_model()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    read_only_fields = (
        'last_login',
        'is_superuser',
        'first_name',
        'last_name',
        'is_active',
        'is_staff',
        'date_joined',
        'email_active_code',
        'referral_code',
        'total_balance',
        'level',
        'level_xp',
        'max_energy',
        'tap',
        'blue_tick',
        'coin'
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                # Fetch user by email
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError("Unable to login with provided credentials.")

            # Check the password
            if not check_password(password, user.password):
                raise serializers.ValidationError("Unable to login with provided credentials.")

            # Check if the user is active
            if not user.is_active:
                raise serializers.ValidationError("User account is deactivated.")

            data['user'] = user  # Add the user to the validated data
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        return data

    def create(self, validated_data):
        user = validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return {
            'token': token.key,
        }










class InvitedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'level')

class DataUSerializer(serializers.ModelSerializer):
    total_invites = serializers.SerializerMethodField()
    invited_users = InvitedUserSerializer(source='referrals', many=True, read_only=True)

    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', 'first_name', 'last_name', 'password', 'last_login', 'date_joined']
        read_only_fields = (
            'username',
            'is_superuser',
            'email',
            'is_active',
            'is_staff',
            'referral_code',
            'level',
            'level_xp',
            'blue_tick',
            'coin'
        )

    def get_total_invites(self, obj):
        return obj.referrals.count()


class UserDetailUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'level',
            'level_xp',
            'blue_tick',
            'coin',
            'wallet',
            'ads',
            'is_active',
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            # Check if the field is 'level' and set it directly
            if attr == 'level':
                setattr(instance, attr, value)
            # For other integer fields, add the value
            elif isinstance(getattr(instance, attr, None), int) and isinstance(value, int):
                setattr(instance, attr, getattr(instance, attr) + value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class VideSentForCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoSentForCheck
        fields = '__all__'





class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=300, required=False)
    username = serializers.CharField(max_length=100, required=False)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if not email and not username:
            raise serializers.ValidationError("Email or Username is required to change the password.")

        return data






class webappgiftcodeserializer(serializers.ModelSerializer):
    class Meta:
        model=webappusercode
        fields = '__all__'








class webappgiftcodeserializercheck(serializers.Serializer):
    code = serializers.CharField(max_length=100)





class dailyuserserializer(serializers.ModelSerializer):
    class Meta:
        model = userdaily
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():

            if isinstance(getattr(instance, attr, None), int) and isinstance(value, int):

                new_value = getattr(instance, attr) - value
                setattr(instance, attr, max(new_value, 0))
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance




class chatbotserializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_blue_tick = serializers.BooleanField(source='user.blue_tick', read_only=True)  # Include blue_tick

    class Meta:
        model = chatbot
        fields = ['id', 'message', 'time', 'date', 'is_pin', 'user_email', 'user_blue_tick']  # Add user_blue_tick
        read_only_fields = ['user']

    def create(self, validated_data):
        # Automatically assign the user from the request
        request = self.context.get('request')
        user = request.user
        return chatbot.objects.create(user=user, **validated_data)
