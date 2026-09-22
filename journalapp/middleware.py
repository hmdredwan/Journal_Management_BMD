from django.shortcuts import get_object_or_404
from .models import HitCounter

class HitCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get or create the HitCounter object
        counter, created = HitCounter.objects.get_or_create(id=1)
        # Increment the total_hits
        counter.total_hits += 1
        counter.save()

        response = self.get_response(request)
        return response