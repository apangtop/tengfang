from django.http import JsonResponse, FileResponse
from django.core.files.storage import default_storage
import os
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def upload_image(request):
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')
            if not image:
                return JsonResponse({'error': 'No image file provided'}, status=400)

            # 确保上传目录存在
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
                logger.info(f"Created upload directory: {upload_dir}")
            
            # 生成唯一的文件名
            file_extension = os.path.splitext(image.name)[1]
            unique_filename = f"{os.urandom(8).hex()}{file_extension}"
            
            # 保存图片到固定路径
            file_name = default_storage.save(f'uploads/{unique_filename}', image)
            logger.info(f"File saved: {file_name}")
            
            # 构建完整的URL
            file_url = f"{request.scheme}://{request.get_host()}/media/uploads/{unique_filename}"
            logger.info(f"File URL: {file_url}")
            
            return JsonResponse({
                'status': 'success',
                'url': file_url,
                'filename': unique_filename
            })
        except Exception as e:
            logger.error(f"Upload error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def get_file(request, filename):
    """获取文件"""
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
        if os.path.exists(file_path):
            return FileResponse(open(file_path, 'rb'))
        return JsonResponse({'error': 'File not found'}, status=404)
    except Exception as e:
        logger.error(f"File retrieval error: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)
