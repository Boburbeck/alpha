def product_availability(product, stock):
    from main.models import ProductBalance
    product_balance = ProductBalance.objects.filter(product=product, stock=stock)
    if product_balance.exists():
        return product_balance.first().available
