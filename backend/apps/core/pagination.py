"""Custom pagination classes for standardized API responses."""

from collections import OrderedDict

from rest_framework.pagination import CursorPagination, PageNumberPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """
    Standard offset/limit pagination for lists <1000 items.
    Returns: {"data": [...], "meta": {"count": N, "next": "...", "previous": "..."}}
    """

    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("data", data),
                    (
                        "meta",
                        OrderedDict(
                            [
                                ("count", self.page.paginator.count),
                                ("next", self.get_next_link()),
                                ("previous", self.get_previous_link()),
                            ]
                        ),
                    ),
                ]
            )
        )

    def get_paginated_response_schema(self, schema):
        return {
            "type": "object",
            "required": ["data", "meta"],
            "properties": {
                "data": schema,
                "meta": {
                    "type": "object",
                    "properties": {
                        "count": {"type": "integer"},
                        "next": {"type": "string", "nullable": True, "format": "uri"},
                        "previous": {"type": "string", "nullable": True, "format": "uri"},
                    },
                },
            },
        }


class HistoricalCursorPagination(CursorPagination):
    """
    Cursor-based pagination for large historical datasets (10+ years of data).
    Used for: time entries, audit logs.
    """

    page_size = 50
    ordering = "-created_at"
    cursor_query_param = "cursor"
