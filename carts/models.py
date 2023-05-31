from django.db import models
from django.conf import settings
from articles.models import Product
from django.contrib.auth import get_user_model

User = get_user_model()  # 현재 프로젝트에서 사용되는 사용자 모델이 할당 됨


class Cart(models.Model):
    """
    장바구니 모델
    """
    user = models.OneToOneField(  # 장바구니를 소유한 사용자 1대1로
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart'
    )  # settings.AUTH_USER_MODEL를 참조해서 사용자 모델과 관계를 맺음
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s 장바구니"

    def total(self):  # 장바구니에 있는 모든 상품의 총 가격을 계산하여 반환하는 메서드
        return sum(item.subtotal() for item in self.cart_items.all())


class CartItem(models.Model):
    """
    장바구니 안에 들어갈 상품 모델
    """
    cart = models.ForeignKey(  # 해당 상품이 속한 장바구니
        Cart, on_delete=models.CASCADE, related_name='cart_items'
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=None)  # 장바구니에 담긴 상품을 나타냄
    quantity = models.PositiveIntegerField(default=1)  # 상품의 수량을 저장함, 기본값 1
    is_selected = models.BooleanField(
        default=False)  # 상품의 선택 여부를 나타내는 필드 기본값 False

    def __str__(self):
        return self.product.product

    def subtotal(self):  # 해당 상품의 소계 가격을 계산
        return self.product.price * self.quantity
