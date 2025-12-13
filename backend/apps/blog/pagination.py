from typing import Any, Dict, List, Tuple

def parse_pagination_params(query_params, default_page=1, default_page_size=10, max_page_size=50) -> Tuple[int, int]:
    def to_int(v, default):
        try:
            return int(v)
        except (TypeError, ValueError):
            return default

    page = to_int(query_params.get("page"), default_page)
    page_size = to_int(query_params.get("page_size"), default_page_size)

    if page < 1:
        page = default_page
    if page_size < 1:
        page_size = default_page_size
    if page_size > max_page_size:
        page_size = max_page_size

    return page, page_size

def paginate(items: List[Dict[str, Any]], page: int, page_size: int) -> Tuple[List[Dict[str, Any]], int]:
    total = len(items)
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end], total