# 🚀 HotmailAPI 快速修复参考

## 问题
验证码已收到，但代码一直等待无法获取 ❌

## 原因
API 请求方法错误：使用了 GET 而不是 POST

## 解决方案

### 已修复的内容 ✅

1. **请求方法**：GET → POST
2. **请求头**：添加 `Content-Type: application/json`
3. **参数传递**：URL params → JSON body

### 修改的文件

```
core/base_mailbox.py
├── _request_json()      # 支持 POST 请求
├── _list_new_messages() # 改用 POST
└── _headers()           # 添加 Content-Type
```

### 正确的 API 调用

```python
import requests

url = "https://yourdomain.com/api/mail-new"
headers = {"Content-Type": "application/json"}
data = {
    "refresh_token": "your_token",
    "client_id": "your_client_id",
    "email": "your_email@hotmail.com",
    "mailbox": "INBOX",
    "response_type": "json"
}

response = requests.post(url, headers=headers, json=data)
```

## 验证修复

```bash
# 1. 语法检查
python -m py_compile core/base_mailbox.py

# 2. 运行测试
python scripts/test_hotmailapi_post.py

# 3. 实际测试
# 在你的注册流程中测试
```

## 对比

| 项目 | 修复前 ❌ | 修复后 ✅ |
|------|----------|----------|
| 请求方法 | GET | POST |
| 参数位置 | URL params | JSON body |
| Content-Type | 无 | application/json |
| 能否获取邮件 | ❌ | ✅ |

## 相关文档

- 详细说明：`HOTFIX_POST_METHOD.md`
- 完整总结：`HOTFIX_SUMMARY.md`
- 测试脚本：`scripts/test_hotmailapi_post.py`

## 状态

✅ 修复完成  
✅ 语法检查通过  
⏳ 需要真实 API 测试

---

**修复时间**：2026-04-06  
**版本**：v1.0.1
