def mark_sold_cost_false(product):
    from main.models import SoldCost
    sold_cost = SoldCost.objects.filter(product=product, is_active=True)
    if sold_cost.exists():
        sold_cost.update(is_active=False)
