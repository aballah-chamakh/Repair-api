from rest_framework import pagination

class OfferPagination(pagination.PageNumberPagination):
    page_size = 10
