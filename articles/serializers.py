from rest_framework import serializers
from articles.models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    inventory_status = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y년 %m월 %d일 %p %I:%M")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y년 %m월 %d일 %p %I:%M")

    def get_inventory_status(self, obj):
        if obj.inventory_status == True:
            return f"남은 수량 : {obj.total_quantity}"
        else:
            return "Sold Out"

    def get_writer(self, obj):
        return obj.writer.username

    def get_price(self, obj):
        return obj.price

    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="writer.username")

    class Meta:
        model = Product
        fields = ("product", "content", "price",
                  "writer", "image", "total_quantity")

    def create(self, validated_data):
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y년 %m월 %d일 %p %I:%M")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y년 %m월 %d일 %p %I:%M")

    def get_writer(self, obj):
        return obj.writer.username

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "writer",
            "title",
            "content",
            "rating",
            "created_at",
            "updated_at",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["title", "content", "rating"]


class WishListSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="writer.username")

    class Meta:
        model = Product
        fields = (
            "product",
            "image",
            "writer",
            "updated_at",
            "price",
        )


class ReviewListSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source='writer.username')
    product = serializers.ReadOnlyField(source='product.product')

    class Meta:
        model = Review
        fields = ("product", "title", "writer", "content", "updated_at",)


class ProductListSerializer(serializers.ModelSerializer):
    writer = serializers.ReadOnlyField(source="writer.username")

    class Meta:
        model = Product
        fields = (
            "id",
            "product",
            "writer",
            "image",
            "updated_at",
            "price",
            "total_quantity",
        )
