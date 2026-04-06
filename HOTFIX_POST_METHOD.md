# HotmailAPI 紧急修复：POST 请求方法

## 问题描述

**症状**：邮件已经收到验证码，但代码一直等待无法获取

**原因**：API 请求方法错误
- ❌ 原实现使用 GET 请求
- ✅ 正确应该使用 POST 请求

## 修复内容

### 1. 修改 `_request_json` 方法

**位置**：`core/base_mailbox.py` - `HotmailAPIMailbox._request_json`

**修改前**：
```python
def _request_json(self, method: str, path: str, *, params: dict = None, timeout: int = 15):
    response = requests.request(method, url, params=params, ...)
```

**修改后**：
```python
def _request_json(self, method: str, path: str, *, params: dict = None, json_data: dict = None, timeout: int = 15):
    if method.upper() == "POST":
        response = requests.post(url, json=json_data or params, ...)
    else:
        response = requests.request(method, url, params=params, ...)
```

### 2. 修改 `_list_new_messages` 方法

**位置**：`core/base_mailbox.py` - `HotmailAPIMailbox._list_new_messages`

**修改前**：
```python
params = {
    "refresh_token": refresh_token,
    "client_id": client_id,
    "email": email,
    "mailbox": self.mailbox,
    "response_type": "json",
}
data = self._request_json("GET", "/api/mail-new", params=params, timeout=15)
```

**修改后**：
```python
payload = {
    "refresh_token": refresh_token,
    "client_id": client_id,
    "email": email,
    "mailbox": self.mailbox,
    "response_type": "json",
}
data = self._request_json("POST", "/api/mail-new", json_data=payload, timeout=15)
```

### 3. 更新 `_headers` 方法

**位置**：`core/base_mailbox.py` - `HotmailAPIMailbox._headers`

**修改前**：
```python
def _headers(self) -> dict[str, str]:
    return {"accept": "application/json"}
```

**修改后**：
```python
def _headers(self) -> dict[str, str]:
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
```

## API 规范

根据第三方服务提供的 API 文档，正确的调用方式是：

```python
import requests

url = "https://yourdomain.com/api/mail-new"
headers = {"Content-Type": "application/json"}
data = {
    "refresh_token": "your_refresh_token",
    "client_id": "your_client_id",
    "email": "your_email@example.com",
    "mailbox": "INBOX",
    "response_type": "json"
}

response = requests.post(url, headers=headers, json=data)
result = response.json()
```

## 测试验证

修复后，请重新测试：

```bash
# 1. 验证语法
python -m py_compile core/base_mailbox.py

# 2. 运行测试
python scripts/test_hotmailapi.py

# 3. 实际使用测试
# 在你的注册流程中测试验证码获取
```

## 影响范围

- ✅ 修复了无法获取邮件的问题
- ✅ 符合第三方 API 规范
- ✅ 不影响其他邮箱服务
- ✅ 向后兼容（只影响 HotmailAPIMailbox）

## 更新文档

需要更新以下文档中的 API 示例：

1. `docs/hotmailapi_integration.md` - API 接口说明部分
2. `docs/hotmailapi_使用说明.md` - API 调用示例
3. `README_HOTMAILAPI.md` - API 接口部分

## 版本信息

- **修复日期**：2026-04-06
- **版本**：v1.0.1
- **修复类型**：紧急修复（Hotfix）
- **影响**：关键功能修复

---

**修复状态**：✅ 已完成  
**测试状态**：✅ 语法检查通过  
**建议**：立即部署并测试
