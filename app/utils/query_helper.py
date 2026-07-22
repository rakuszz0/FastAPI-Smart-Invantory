from sqlalchemy import asc
from sqlalchemy import desc


def apply_sort(
    query,
    model,
    sort_by: str = "id",
    order: str = "asc"
):

    if not hasattr(
        model,
        sort_by
    ):

        return query

    column = getattr(
        model,
        sort_by
    )

    if order.lower() == "desc":

        return query.order_by(
            desc(column)
        )

    return query.order_by(
        asc(column)
    )


def apply_pagination(
    query,
    page: int,
    size: int
):

    offset = (
        page - 1
    ) * size

    return (
        query
        .offset(offset)
        .limit(size)
    )


def apply_search(
    query,
    model,
    keyword: str,
    fields: list
):

    from sqlalchemy import or_

    filters = []

    for field in fields:

        filters.append(
            getattr(
                model,
                field
            ).ilike(
                f"%{keyword}%"
            )
        )

    return query.filter(
        or_(*filters)
    )