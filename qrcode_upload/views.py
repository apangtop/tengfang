from django.http import JsonResponse, FileResponse
from django.core.files.storage import default_storage
import os
from django.conf import settings
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

# Create your views here.

@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request):
    try:
        logger.info("Received upload request")
        logger.info(f"Request FILES: {request.FILES}")
        logger.info(f"Request POST: {request.POST}")
        
        image = request.FILES.get('image')
        if not image:
            logger.error("No image file provided")
            return JsonResponse({'error': 'No image file provided'}, status=400)

        # 确保上传目录存在
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir, mode=0o755)
            logger.info(f"Created upload directory: {upload_dir}")
        
        # 生成唯一的文件名
        file_extension = os.path.splitext(image.name)[1]
        unique_filename = f"{os.urandom(8).hex()}{file_extension}"
        
        # 保存图片到固定路径
        file_path = os.path.join(upload_dir, unique_filename)
        with open(file_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        
        logger.info(f"File saved: {file_path}")
        
        # 构建完整的URL
        file_url = f"{request.scheme}://{request.get_host()}/media/uploads/{unique_filename}"
        logger.info(f"File URL: {file_url}")
        
        return JsonResponse({
            'status': 'success',
            'url': file_url,
            'filename': unique_filename
        })
    except Exception as e:
        logger.error(f"Upload error: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_file(request, filename):
    """获取文件"""
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'))
        logger.error(f"File not found: {file_path}")
        return JsonResponse({'error': 'File not found'}, status=404)
    except Exception as e:
        logger.error(f"File retrieval error: {str(e)}", exc_info=True)
        return JsonResponse({'error': str(e)}, status=500)
