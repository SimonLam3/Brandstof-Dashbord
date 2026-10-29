def trip_cost(distance_km, km_per_liter, fuel_price):
    liters_needed = (distance_km * 2) / km_per_liter
    return liters_needed * fuel_price