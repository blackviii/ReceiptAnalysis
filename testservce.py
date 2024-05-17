#把当前时间打印出来精确到秒
import time
print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
