from .models import Profile

class EnsureProfileMiddleware:
    """
    This middleware ensures that every authenticated user has a corresponding Profile.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # get_or_create returns a tuple (profile, created)
            Profile.objects.get_or_create(user=request.user)
        response = self.get_response(request)
        return response