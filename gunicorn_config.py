# Gunicorn配置
bind = "127.0.0.1:8000"
workers = 3  # 建议设置为(2 x CPU核心数 + 1)
user = "www-data"
group = "www-data"
timeout = 120
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
