from math import ceil


def paginate(
    *,
    data,
    total: int,
    page: int,
    size: int,
):
    return {
        "items": data,
        "pagination": {
            "page": page,
            "size": size,
            "total": total,
            "total_pages": ceil(total / size) if size else 0,
            "has_next": page * size < total,
            "has_previous": page > 1,
        },
    }