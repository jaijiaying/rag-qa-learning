# Python HTTP 服务基础

来源：Python 官方 http.server 文档
https://docs.python.org/3/library/http.server.html

Python 标准库中的 http.server 提供了一个简单的 HTTP 服务实现，适合本地开发、测试静态文件和学习 HTTP 请求处理。

HTTPServer 负责监听地址和端口，并把收到的请求交给请求处理器。请求处理器可以继承 BaseHTTPRequestHandler，并实现 do_GET 或 do_POST 方法。

do_GET 通常用于处理浏览器的 GET 请求。处理器需要发送响应状态码、响应头和响应内容。发送 Content-Type 响应头时，应同时说明内容的字符编码。

do_POST 用于接收客户端提交的数据。服务端通常先读取 Content-Length，再解析请求体中的 JSON 或表单数据。

http.server 主要用于本地测试，不建议直接暴露在不可信的公网环境中。生产环境通常需要经过验证的 Web 框架、身份认证、日志、超时和安全配置。

练习问题：
1. HTTPServer 的作用是什么？
2. do_GET 和 do_POST 分别处理什么请求？
3. 为什么响应头需要设置 Content-Type？
4. http.server 适合直接用于生产环境吗？
