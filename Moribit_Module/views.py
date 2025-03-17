from rest_framework import permissions
from rest_framework import permissions
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.shortcuts import get_object_or_404

from Control_Module import models
from .models import User, GiftCode, Moriaigiftcoin ,webappusercode,userdaily,chatbot
from .serializers import CodeCheckSerializer, webappgiftcodeserializercheck, usercodeCheckSerializer, UserSerializer, LoginSerializer, DataUSerializer, UserDetailUpdateSerializer, VideSentForCheckSerializer, ChangePasswordSerializer, webappgiftcodeserializer, dailyuserserializer, chatbotserializer

from django.shortcuts import render
import  requests

from django.utils.deprecation import MiddlewareMixin
from asgiref.sync import sync_to_async



class RedirectBrowserRequestsMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Define paths that should not be redirected
        excluded_paths = ['/admin', '/admin/','/schema','/schema/','schema/swagger-ui/','schema/redoc/']

        # Check if the request path is excluded
        if any(request.path.startswith(path) for path in excluded_paths):
            return None

        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()

        # Simple check to determine if the request comes from a browser
        if 'mozilla' in user_agent or 'chrome' in user_agent or 'safari' in user_agent or 'edge' in user_agent:
            return render(request, '404.html', status=404)

        return None

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


class CreateUserView(APIView):
    """
    Create new user
    """
    serializer_class = UserSerializer

    def post(self, request):
        # Parse request data
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the serializer
            serializer.save()
            return Response({'status': 'success', 'message': 'User successfully created.'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    login user
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.save(), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    """
    get user detail
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DataUSerializer

    def get(self, request, *args, **kwargs):
        serializer = DataUSerializer(request.user)
        return Response(serializer.data)


class UserDetailUpdate(APIView):
    """
   first get user data then update it
   for example user has 200 coin you must get 200 coin from database then plus to your
   coin request finally send update request
   user coin in database = 100
   user update coin you want send 200
   100+200
   then send 300 request to update it

    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserDetailUpdateSerializer

    def put(self, request, *args, **kwargs):
        user = request.user  # Fetch the user object
        serializer = self.serializer_class(user, data=request.data, partial=True)  # Use partial=True
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLinks(APIView):
    """
    get links task for check of if they do the social video or not
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = VideSentForCheckSerializer

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id

        serializer = VideSentForCheckSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response({'status': 'success', 'message': 'links successfully saved.'},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):

    '''
    get username or email if its correct the new password will update.

    password and email/username must send togather.
    '''
    serializer_class = ChangePasswordSerializer
    model = User

    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        email = self.request.data.get('email')
        username = self.request.data.get('username')

        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                return None
        elif username:
            try:
                return User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        else:
            return None

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.object.set_password(serializer.validated_data.get("new_password"))
            self.object.save()

            response = {
                'status': 'success',
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class Codeview(APIView):

    '''
    check the entered code if it is ok give them coin
    '''


    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = usercodeCheckSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            code = serializer.validated_data.get('code')
            gift = GiftCode.objects.filter(code=code).first()

            if gift:
                user_exist = gift.user.exists()
                if user_exist:
                    return Response({'status': 'error', 'message': 'You already received your gift!'},status=status.HTTP_200_OK)
                else:
                    gift.user.add(user)
                    user.coin += gift.gift
                    user.save()
                    return Response({'status': 'success', 'message': f'You received {gift.gift} coins.'},
                                    status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': 'Code does not exist!'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


















def check_code_with_external_service(referral_code):
    url = 'https://test.org/data'
    token = '4dced4e2b5414448a9445fe1deb1c11ac7d954a5'  # Use the appropriate token
    headers = {
        'Authorization': f'Token {token}'
    }
    params = {
        'code': referral_code
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json(), response.status_code
    except requests.HTTPError as e:
        return str(e), response.status_code
    except requests.RequestException as e:
        return str(e), status.HTTP_500_INTERNAL_SERVER_ERROR

class Giftcheckview(APIView):

    '''
    get user Token with code if it is ok give them 100000 coin .
    '''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CodeCheckSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            user = request.user

            # Check if the user has already redeemed this code
            if Moriaigiftcoin.objects.filter(user=user, code=code).exists():
                return Response({
                    'status': 'error',
                    'message': 'You have already redeemed this code.'
                }, status=status.HTTP_400_BAD_REQUEST)

            result, status_code = check_code_with_external_service(code)

            if status_code == status.HTTP_200_OK:
                if isinstance(result, list) and len(result) > 0:
                    code_details = next((item for item in result if item.get('code') == code), None)

                    if code_details:
                        external_email = code_details.get('email')
                        if user.email == external_email:
                            user.coin += 100000
                            user.save()
                            Moriaigiftcoin.objects.create(user=user, code=code)
                            response_data = {
                                'status': 'success',
                                'message': 'You have received 100000 coins!'
                            }
                        else:
                            response_data = {
                                'status': 'error',
                                'message': 'Your email does not match with the one in test.org'
                            }
                    else:
                        response_data = {
                            'status': 'error',
                            'message': 'Code does not exist or is invalid'
                        }
                else:
                    response_data = {
                        'status': 'error',
                        'message': 'Invalid response from external service'
                    }
            else:
                response_data = {
                    'status': 'error',
                    'message': result
                }

            return Response(response_data, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WebAppGiftCodeCheck(APIView):
    """
    Get user webapp gift code if it is ok give them coin.
    """

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = webappgiftcodeserializercheck

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            code = serializer.validated_data.get('code')

            giftwebapp=get_object_or_404(webappusercode,code=code)

            if giftwebapp.is_used ==True:
                return Response({'status': 'error', 'message': 'you already get gift with this code.'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                giftwebapp.is_used = True
                giftwebapp.save()
                user.coin += giftwebapp.gift
                user.save()
                return Response({'status': 'success', 'message': f'You received {giftwebapp.gift} coins.'},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'status': 'error', 'message': 'An error occurred while processing your request.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







class webappgiftcodview(APIView):
    '''
        save gift code user to check
    '''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = webappgiftcodeserializer


    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class userdailyview(APIView):
    '''
    Update user daily turbo, energy, jackpot. If the record does not exist, create it and decrement the values if specified in the request.
    '''

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = dailyuserserializer

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data

        # Get or create the userdaily record
        user_daily, created = userdaily.objects.get_or_create(user=user)

        # Update the userdaily record using the serializer's update method
        serializer = self.serializer_class(user_daily, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









class chatbotview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = chatbotserializer

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_staff:
                chats = chatbot.objects.all()
                # Using a serializer to return the data in a proper format
                serializer = self.serializer_class(chats, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            print(e)
            return Response({'status': 'error', 'message': 'An error occurred while processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







