def format_currency(
    value: float
):

    return f"Rp {value:,.0f}".replace(
        ",",
        "."
    )


def percentage(
    value,
    total
):

    if total == 0:

        return 0

    return round(
        (value / total) * 100,
        2
    )


def discount_price(
    price,
    discount
):

    return price - (
        price * discount / 100
    )


def calculate_tax(
    amount,
    tax=11
):

    return amount * tax / 100