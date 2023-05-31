from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from users.serializers import CustomTokenObtainPairSerializer, UserSerializer, UserProfileSerializer,UserProfileProductSerializer, UserProfileReviewSerializer, UserProfileWishSerializer
from rest_framework.generics import get_object_or_404
from users.models import User

# 카카오 로그인용
# from allauth.socialaccount.models import SocialAccount
# from users.models import User as UserModel


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"가입완료 ^^"}, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        """ 회원 정보를 수정합니다. """
        user = User.objects.get(email=request.user)
        serializer = UserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': '수정완료 ^ㅇ^'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """ 회원 탈퇴 기능입니다. """
        user= request.user
        user.is_active = False
        user.save()
        return Response({'message': '삭제완료'})

class CustomTokenObtainPairView(TokenObtainPairView):   #이게 로그인 기능이라서, 로그인 코드를 쓸 필요가 없었다는 것.
    serializer_class = CustomTokenObtainPairSerializer


# 마이페이지
class ProfileView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserProfileSerializer(user)

        return Response(serializer.data)

class ProfileProductView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserProfileProductSerializer(user)

        return Response(serializer.data)

class ProfileWishView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserProfileWishSerializer(user)

        return Response(serializer.data)

class ProfileReviewView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = UserProfileReviewSerializer(user)

        return Response(serializer.data)

# 카카오로그인
# class KakaoLoginView(APIView):

#     def post(self, request):
#         email = request.data.get("email")
#         nickname = request.data.get("nickname")

#         try:
#             # 기존에 가입된 유저와 쿼리해서 존재하면서, socialaccount에도 존재하면 로그인
#             user = UserModel.objects.get(email=email)
#             social_user = SocialAccount.objects.filter(user=user).first()
#             #로그인
#             if social_user:
#                 refresh = RefreshToken.for_user(user)
                
#                 return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "로그인 성공"}, status=status.HTTP_200_OK)
            
#             # 동일한 이메일의 유저가 있지만, social계정이 아닐때 
#             if social_user is None:
#                 return Response({"error": "email exists but not social user"}, status=status.HTTP_400_BAD_REQUEST)
            
#             # 소셜계정이 카카오가 아닌 다른 소셜계정으로 가입했을때
#             if social_user.provider != "kakao":
#                 return Response({"error": "no matching social type"}, status=status.HTTP_400_BAD_REQUEST)
    
#         except UserModel.DoesNotExist:
#             # 기존에 가입된 유저가 없으면 새로 가입
#             new_user = UserModel.objects.create(
#                 nickname=nickname,
#                 email=email,
#             )
#             #소셜account에도 생성
#             SocialAccount.objects.create(
#                 user_id=new_user.id,
#             )

#             refresh = RefreshToken.for_user(new_user)
                
#             return Response({'refresh': str(refresh), 'access': str(refresh.access_token), "msg" : "회원가입 성공"}, status=status.HTTP_201_CREATED)