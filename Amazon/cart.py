import json
from decimal import Decimal
from django.conf import settings
from ecomm.redis_client import redis_client
from .models import Product

class Cart:
    def __init__(self, request):
        self.user_id = request.user.id if request.user.is_authenticated else request.session.session_key

        if not self.user_id:
            request.session.save()
            self.user_id = request.session.session_key
        self.key = f"cart:{self.user_id}"

    def add(self, product_id, product_data):
        existing = redis_client.hget(self.key, product_id)

        if existing:
            existing_data = json.loads(existing)
            existing_data['quantity'] += product_data.get('quantity', 1)
            redis_client.hset(self.key, product_id, json.dumps(existing_data))
        else:
            redis_client.hset(self.key, product_id, json.dumps(product_data))

    def save(self):
        pass

    def remove(self, product):
        product_id = str(product.id)
        redis_client.hdel(self.key, product_id)

    def get_items(self):
        cart_data = redis_client.hgetall(self.key)
        print(f">>> Raw Redis data for key {self.key}: {cart_data}")  # Diagnostic print

        items = []

        for item_data in cart_data.values():
            item = json.loads(item_data)
            print(f">>> Item loaded from Redis: {item}")  # Diagnostic print
            item['total_price'] = Decimal(item.get('price', 0)) * item.get('quantity', 0)
            items.append(item)

        return items

    def get_total_price(self):
        return sum(
            Decimal(item.get('price', 0)) * item.get('quantity', 1)
            for item in self.get_items()
        )

    def clear(self):
        redis_client.delete(self.key)
