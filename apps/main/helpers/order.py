from decimal import Decimal

from main.models import Order


def init_order_product(order_product, order: Order):
    from main.models import OrderProduct
    from main.helpers import order_product_price
    product = order_product['product']
    amount = order_product['amount']
    price = order_product_price(product, amount)
    OrderProduct.objects.create(
        order=order,
        product=product,
        amount=amount,
        price=price,
        internal_price=price
    )


def init_order(order: Order):
    order_products = order.products.select_related('product').all()
    order.total_price = sum(p.price for p in order_products)
    if order.deliver:
        order.internal_delivery_price = order.delivery_price
        order.total_price += order.delivery_price or Decimal(0)

    order.internal_total_price = order.total_price


def is_int(num: str):
    try:
        int(num)
        return True
    except ValueError:
        return False
