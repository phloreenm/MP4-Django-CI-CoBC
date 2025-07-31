from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
import os
import mimetypes

# Create your views here.
def index(request):
    """ A view to return the index page """

    return render(request, 'home/index.html')

def serve_media(request, path):
    """Serve media files in production when DEBUG=False"""
    if not settings.DEBUG:
        # Build the full path to the file
        file_path = os.path.join(settings.MEDIA_ROOT, path)
        
        # Check if file exists
        if os.path.exists(file_path):
            # Determine the content type
            content_type, _ = mimetypes.guess_type(file_path)
            
            # Read and return the file
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type=content_type)
                return response
        else:
            raise Http404("Media file not found")
    else:
        raise Http404("This view is only for production")