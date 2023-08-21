from multiprocessing import cpu_count

# Socket Path
#bind = 'unix:/home/lorenzo/botai/hypercorn_hbot.sock'
bind = '0.0.0.0:5005'

# Worker Options
workers = cpu_count() + 1
# worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/lorenzo/botai/log/access_log'
errorlog =  '/home/lorenzo/botai/log/error_log'