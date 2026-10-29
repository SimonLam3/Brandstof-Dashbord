def fuel_saving(
    nl_price,
    de_price,
    tank_size,
    distance_km,
    km_per_liter
):
    liters_used = distance_km / km_per_liter

    liters_to_fill = tank_size - liters_used

    return (
        nl_price - de_price
    ) * liters_to_fill