from dataclasses import field
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from users.models import User
from articles.serializers import ProductSerializer, WishListSerializer, ReviewListSerializer, ProductListSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # patch를 사용 하기 위에 값이 들어 오지 않으면 원래 상태, 아니면 수정된 데이터 저장
        user = super().update(instance, validated_data)
        password = user.password
        user.set_password(password)  # 비밀번호 암호화
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['is_admin'] = user.is_admin

        return token


class UserProfileSerializer(serializers.ModelSerializer):
    review_set = ReviewListSerializer(many=True)  # 내가 쓴 리뷰 불러오기
    wishes = WishListSerializer(many=True)  # 찜한 상품 불러오기

    class Meta:
        model = User
        fields = ("id", "email", "product_set", "wishes", "review_set")


class UserProfileProductSerializer(serializers.ModelSerializer):
    product_set = ProductListSerializer(many=True)  # 작성한 물품 불러오기

    class Meta:
        model = User
        fields = ("id", "email", "product_set",)


class UserProfileReviewSerializer(serializers.ModelSerializer):
    review_set = ReviewListSerializer(many=True)  # 내가 쓴 리뷰 불러오기

    class Meta:
        model = User
        fields = ("id", "email", "review_set")


class UserProfileWishSerializer(serializers.ModelSerializer):
    wishes = WishListSerializer(many=True)  # 찜한 상품 불러오기

    class Meta:
        model = User
        fields = ("id", "email", "wishes",)
