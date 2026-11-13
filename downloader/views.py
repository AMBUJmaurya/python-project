from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import yt_dlp
import os
import tempfile
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'downloader/index.html')

@csrf_exempt
def download(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        revolutions = 0
        if not url:
            return JsonResponse({'success': False, 'error': 'No URL provided.', 'revolutions': revolutions})
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                ydl_opts = {
                    'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                    'quiet': True,
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    revolutions += 1
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                if not os.path.exists(filename):
                    return JsonResponse({'success': False, 'error': 'Download failed. File not found.', 'revolutions': revolutions})
                with open(filename, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/octet-stream')
                    response['Content-Disposition'] = f'attachment; filename=\"{os.path.basename(filename)}\"'
                    response['X-Revolutions'] = str(revolutions)
                    return response
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e), 'revolutions': revolutions})
    return JsonResponse({'success': False, 'error': 'Invalid request', 'revolutions': 0})
