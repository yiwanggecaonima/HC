# slave_hc

scrapy爬取慧聪网，这里并没有使用scrapy_redis  这个库，只是用来redis作为队列来进行调度
数据存储用的还是mongodb,redis出mongo入
中间件写了一个随机ua，proxy,和一些异常报错等等，对于proxy,思路是重试５次，如果达到４次仍旧得不到正确的状态码，几使用代理ip，最大程度防止有漏网之鱼
慧聪这个网站相应速度并不是特别快，下面是测试之后得到的参数
request =8,
timeout = 10,
DOWNLOAD_DELAY = 2,
RETRY_ENABLED = True,
RETRY_TIMES = 5


如果服务器性能够好可以增加request并发，但是注意不要把它搞死．

管道存储写了一个json文件，和一个mongodb  这个自然不用说

spider文件也是很平常　最好能加上动态域，不让他出现域名限制

setting文件更改redis和mongo配置，复制几份，可以玩玩分布式，这是一个简单的scrapy+redis分布式实现



最后欢迎技术交流：　wutong8773@163.com
