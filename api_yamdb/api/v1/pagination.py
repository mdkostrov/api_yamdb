from rest_framework.pagination import LimitOffsetPagination


class PagePagination(LimitOffsetPagination):
    default_limit = 10
