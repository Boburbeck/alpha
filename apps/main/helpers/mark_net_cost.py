def mark_net_cost_false(product):
    from main.models import NetCost
    net_cost = NetCost.objects.filter(product=product, is_active=True)
    if net_cost.exists():
        net_cost.update(is_active=False)
