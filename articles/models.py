from django.db import models
from django.core.exceptions import ValidationError
from users.models import User


class Product(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.CharField("상품명", max_length=30)
    content = models.TextField("내용")
    price = models.PositiveIntegerField("가격", default=0)
    image = models.ImageField("사진", blank=True, null=True)
    total_quantity = models.PositiveIntegerField("총수량", default=0)
    inventory_status = models.BooleanField("재고유무", default=True)  # 품절이면 False
    created_at = models.DateTimeField("생성 시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시간", auto_now=True)
    wishes = models.ManyToManyField(
        User, related_name='wishes', blank=True)

    def __str__(self):
        return str(self.product)

    def save(self, **kwargs):
        if self.total_quantity is None:
            self.total_quantity = 0  # 기본값으로 0 설정 또는 다른 유효한 값으로 대체

        if self.total_quantity < 0:
            raise ValidationError("총수량이 0보다 작을 수 없습니다.")

        if self.total_quantity <= 0:
            self.inventory_status = False

        super().save(**kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("제목", max_length=50)
    content = models.TextField("내용")
    rating = models.IntegerField("별점", default=0)
    created_at = models.DateTimeField("생성 시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시간", auto_now=True)

    def __str__(self):
        return self.title
