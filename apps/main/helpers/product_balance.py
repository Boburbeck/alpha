def product_availability(product, stock):
    from main.models import ProductBalance
    product_balance = ProductBalance.objects.products(product=product, stock=stock)
    if product_balance.exists():
        available = dict()
        for balance in product_balance:
            available["available"] = balance['available']
        return available
    return 0


def init_create_product_balance(stock, product, amount=None):
    from main.models import ProductBalance
    ProductBalance.objects.create(
        stock=stock,
        product=product,
        sold=amount
    )
