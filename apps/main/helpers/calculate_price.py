def order_product_price(product, amount):
    from main.models import SoldCost
    sold_cost = SoldCost.objects.filter(product=product, is_active=True).first()
    price = sold_cost.price * amount
    return price
