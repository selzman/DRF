from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from Moribit_Module.models import User
from .models import News, AppConfing, Dailybonus, tasks
from .serializers import NewsSerializer, AppConfingsSerializer, DailybonusSerializer, tasksSerializer , adminalertserizlizer
import asyncio


class NewsView(APIView):
    """
    get news from admin
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = NewsSerializer

    def get(self, request):
        if request.user.is_staff:
            news = News.objects.all().order_by('-DateTime')
            serializer = NewsSerializer(news, many=True)

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class AppConfingView(APIView):
    """
    main confing of the application
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAuthenticatedOrReadOnly]
    serializer_class = AppConfingsSerializer

    def get(self, request):
        if request.user.is_staff:
            appConfing = AppConfing.objects.last()
            serializer = AppConfingsSerializer(appConfing)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class DailybonusClaimView(APIView):
    """
    Claim daily bonus
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DailybonusSerializer


    def get(self, request):
        if Dailybonus.objects.filter(is_active=True, user=request.user.id):
            print(request.user.id)
            return Response(status=status.HTTP_200_OK)
        else:
            dailybonus = Dailybonus.objects.filter(is_active=True).all()
            serializer = DailybonusSerializer(dailybonus, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response(data={"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            active_bonuses = Dailybonus.objects.filter(is_active=True, id=request.data['id'])

            if active_bonuses.filter(user=user).exists():
                return Response(data={"detail": "You have already claimed the daily bonus."},
                                status=status.HTTP_400_BAD_REQUEST)

            total_gift_coin = 0
            for dailybonus in active_bonuses:
                dailybonus.user.add(user)
                dailybonus.save()
                total_gift_coin += dailybonus.gift_coin

            user_profile = User.objects.get(id=user.id)
            user_profile.coin += total_gift_coin
            user_profile.save()

            return Response(data={"detail": f"Daily bonus claimed successfully. You received {total_gift_coin} coins."},
                            status=status.HTTP_200_OK)

        except:
            return Response(data={"detail": "send id of dailybonus to get gift coins. "},
                            status=status.HTTP_400_BAD_REQUEST)


class tasksview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = tasksSerializer

    def get(self, request):
        if request.user.is_staff:
            get_tasks = tasks.objects.all()
            serializer = tasksSerializer(get_tasks, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user

        if not user.is_authenticated:
            return Response(data={"detail": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)


        tasks_get = tasks.objects.filter(id=request.data['id'])

        if tasks_get.exists():
            try:

                if tasks_get.filter(user=user).exists():
                    return Response(data={"detail": "You have already claimed the tasks gift."},
                                    status=status.HTTP_400_BAD_REQUEST)

                total_gift_coin = 0
                for task in tasks_get:
                    task.user.add(user)
                    task.save()
                    total_gift_coin += task.gift_coin

                user_profile = User.objects.get(id=user.id)
                user_profile.coin += total_gift_coin
                user_profile.save()

                return Response(
                    data={"detail": f"task claimed successfully. You received {total_gift_coin} coins."},
                    status=status.HTTP_200_OK)

            except:
                return Response(data={"detail": "send id of task to get gift coins. "},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(data={"detail": "send correct id of task to get gift coins. "},
                            status=status.HTTP_400_BAD_REQUEST)




class adminalertview(APIView):

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = adminalertserizlizer

    def post(self, request, *args, **kwargs):
        serializer = adminalertserizlizer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)













