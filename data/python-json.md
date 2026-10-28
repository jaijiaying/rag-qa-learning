# Python JSON 数据处理

来源：Python 官方 json 文档
https://docs.python.org/3/library/json.html

JSON 是一种常见的数据交换格式，能够表示对象、数组、字符串、数字、布尔值和空值。Python 的 json 模块可以在 JSON 文本和 Python 对象之间转换。

json.loads 用于把 JSON 字符串解析为 Python 对象。json.dumps 用于把 Python 对象转换为 JSON 字符串。

读取 HTTP 请求中的 JSON 时，应先读取请求体，再调用 json.loads 解析。解析失败时，程序应该返回清晰的错误信息，而不是直接崩溃。

ensure_ascii=False 可以让 json.dumps 保留中文字符。实际保存或返回 JSON 时，还要注意字符编码，通常使用 UTF-8。

JSON 对象通常对应 Python 字典，JSON 数组通常对应 Python 列表，JSON 中的 true、false、null 分别对应 Python 的 True、False、None。

练习问题：
1. json.loads 的作用是什么？
2. json.dumps 的作用是什么？
3. JSON 数组对应 Python 的什么类型？
4. 如何让 json.dumps 保留中文字符？
