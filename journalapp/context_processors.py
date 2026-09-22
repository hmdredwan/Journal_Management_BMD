from .models import HitCounter

def hit_counter(request):
    counter = HitCounter.objects.first()  # Get the first HitCounter object
    return {'total_hits': counter.total_hits if counter else 0}