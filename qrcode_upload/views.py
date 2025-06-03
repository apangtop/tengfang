from django.http import JsonResponse, FileResponse
from django.core.files.storage import default_storage
import os
from django.conf import settings

# Create your views here.

def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            # 确保上传目录存在
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            
            # 生成唯一的文件名
            file_extension = os.path.splitext(image.name)[1]
            unique_filename = f"{os.urandom(8).hex()}{file_extension}"
            
            # 保存图片到固定路径
            file_name = default_storage.save(f'uploads/{unique_filename}', image)
            # 构建完整的URL
            file_url = f"{request.scheme}://{request.get_host()}/media/uploads/{unique_filename}"
            
            return JsonResponse({
                'status': 'success',
                'url': file_url,
                'filename': unique_filename
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_file(request, filename):
    """获取文件"""
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    return JsonResponse({'error': 'File not found'}, status=404)
