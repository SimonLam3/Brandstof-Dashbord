from functions.germany.trip_cost import trip_cost
from functions.germany.fuel_saving import fuel_saving

def is_worth_it(
    nl_price,
    de_price,
    distance_km,
    tank_size=30,
    km_per_liter=15
):
    savings = fuel_saving(
        nl_price,
        de_price,
        tank_size,
        distance_km,
        km_per_liter
    )

    travel_cost = trip_cost(
        distance_km,
        km_per_liter,
        nl_price
    )

    profit = savings - travel_cost

    return {
        "savings": round(savings, 2),
        "travel_cost": round(travel_cost, 2),
        "profit": round(profit, 2),
        "worth_it": profit > 0
    }