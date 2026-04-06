# HotmailAPI 邮箱集成说明

## 概述

HotmailAPI 是一个基于第三方 API 的 Hotmail/Outlook 邮箱服务集成，支持从本地文件导入邮箱账号池，并通过 API 获取验证码。

## 功能特性

- ✅ 支持从本地文件批量导入 Hotmail 账号
- ✅ 自动轮转使用邮箱池中的账号
- ✅ 支持通过 API 获取新邮件
- ✅ 智能验证码提取（支持自定义正则）
- ✅ 支持代理配置
- ✅ 线程安全的账号池管理

## 账号文件格式

邮箱账号文件使用 `.txt` 格式，每行一个账号，字段之间使用 `----` 分隔：

```
email----password----client_id----refresh_token
```

### 字段说明

1. **email**: Hotmail/Outlook 邮箱地址
2. **password**: 邮箱密码（可选，某些场景下可能不需要）
3. **client_id**: Microsoft OAuth 应用的 Client ID
4. **refresh_token**: Microsoft OAuth 的 Refresh Token

### 示例

```
CaesarPhryne2274@hotmail.com----eg699579----9e5f94bc-e8a4-4e73-b8be-63364c29d753----M.C508_BAY.0.U.-CtJ4G35AD2YZGqZKsoEb4qEi1cUS6Hcn36nhbJq8SSvWsTJFDdgnbuEyxPSjxeIk4bINeaBO7HufyI4!XWyRsoZdy1C3imxO54Depfdw8JcJDz7ZmoR3xftDzvlYiNB*QHruRpha0SZPxLirgdMZYUjoQXNlW6s2k44ng9JHZMVWtE*JepU*TiZ2rkM*jR2*PtgqTYyx0vMLKccm0DnfahzDAN6lerGzLL2d0TpT*OcnTwK7xQgh1z3GYbjhWO6zchKBXgnrAn54YGcMG7aHIsksR2Y7IYaFmwPd0mR7e!TT4zapKTMErk3q91fvVMRNXePNlnFEhoTqWDLWCXEpMeC2UKpBrxm9eNpgMnrSb04r*AlwzdbYSHm*vrWrViW3OQ$$
BeatrizQuill1241@hotmail.com----uw923904----9e5f94bc-e8a4-4e73-b8be-63364c29d753----M.C547_BAY.0.U.-CuWrl5Agd5zDDc0ZdGd0IsAFqGLz7eD3ailo8mCV*Ho3IwzeakJpL2C14Jxab7cxLosk!V68K7QlAJqGElugQ8r3WLv4eBMpANpItOSUtfDsjJkIq7bo!5HdKZKkNKQCyRFmAgPVJePMdrxFcBu0uSoKrtlBmMYCK0VAUiVcqpqkXv0yYvK7WEpO!0eRh0*fgHePOOZKJFn9BwuwSdaNbGXvVD3i7gm!CAtOTKg*k7cjcHxkXZ1BeV*XPVV95SldfEnvLOWpXS7gGPKvyoLIYjt9hdbwbR0gYd7UUKiMILDFEqckIeGm8mJdlgOxgvUFbv4RIqb83ToPDSNqNidufSEYaW3m*RnuvMIshKGEVrhX4bnlvDPKb3Ts*A6RCPI5!A$$
```

## API 接口说明

### 获取新邮件

**接口**: `POST /api/mail-new`

**请求头**:
```
Content-Type: application/json
```

**请求体**:
```json
{
  "refresh_token": "OAuth Refresh Token",
  "client_id": "OAuth Client ID",
  "email": "邮箱地址",
  "mailbox": "邮箱文件夹（默认 INBOX）",
  "response_type": "json"
}
```

**示例请求**:
```python
import requests

url = "https://yourdomain.com/api/mail-new"
headers = {"Content-Type": "application/json"}
data = {
    "refresh_token": "your_refresh_token",
    "client_id": "your_client_id",
    "email": "your_email@hotmail.com",
    "mailbox": "INBOX",
    "response_type": "json"
}

response = requests.post(url, headers=headers, json=data)
data = response.json()
```

## 配置方法

### 1. 准备邮箱账号文件

将你的 Hotmail 账号信息保存到 `mail/` 目录下的 `.txt` 文件中：

```bash
# 创建账号文件
cat > mail/hotmail_accounts.txt << 'EOF'
email1@hotmail.com----password1----client_id1----refresh_token1
email2@hotmail.com----password2----client_id2----refresh_token2
EOF
```

### 2. 配置邮箱服务

在你的配置中添加 HotmailAPI 邮箱服务：

```python
mailbox_config = {
    "provider": "hotmailapi",
    "extra": {
        "hotmailapi_api_url": "https://yourdomain.com",  # API 服务地址
        "hotmailapi_pool_dir": "mail",                    # 账号池目录
        "hotmailapi_pool_file": "",                       # 指定账号文件（可选）
        "hotmailapi_mailbox": "INBOX",                    # 邮箱文件夹
    },
    "proxy": "http://proxy:port"  # 代理配置（可选）
}
```

### 3. 使用示例

```python
from core.base_mailbox import create_mailbox

# 创建邮箱实例
mailbox = create_mailbox(
    provider="hotmailapi",
    extra={
        "hotmailapi_api_url": "https://yourdomain.com",
        "hotmailapi_pool_dir": "mail",
        "hotmailapi_mailbox": "INBOX",
    },
    proxy=None
)

# 获取一个邮箱账号
account = mailbox.get_email()
print(f"分配的邮箱: {account.email}")

# 获取当前邮件 ID（用于过滤旧邮件）
before_ids = mailbox.get_current_ids(account)

# 等待验证码
code = mailbox.wait_for_code(
    account=account,
    keyword="",           # 关键词过滤（可选）
    timeout=120,          # 超时时间（秒）
    before_ids=before_ids,
    code_pattern=None,    # 自定义验证码正则（可选）
)
print(f"收到验证码: {code}")
```

## 配置参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `hotmailapi_api_url` | string | 是 | - | API 服务地址 |
| `hotmailapi_pool_dir` | string | 否 | `mail` | 账号池文件所在目录 |
| `hotmailapi_pool_file` | string | 否 | - | 指定账号文件路径（优先级高于 pool_dir） |
| `hotmailapi_mailbox` | string | 否 | `INBOX` | 邮箱文件夹名称 |

## 账号池管理

### 轮转机制

系统会自动从账号池中轮转使用邮箱：
1. 首次使用时加载账号文件
2. 每次调用 `get_email()` 时按顺序分配下一个账号
3. 用完后自动回到第一个账号（循环使用）

### 线程安全

账号池使用线程锁保护，支持多线程并发访问。

### 缓存机制

账号池在首次加载后会缓存在内存中，避免重复读取文件。

## 验证码提取

### 智能提取

系统使用增强的验证码提取算法（`_yyds_safe_extract`），具有以下特性：

1. **URL 过滤**: 自动过滤邮件中的 URL 链接，避免误提取追踪链接中的数字
2. **边界检测**: 严格检查验证码前后的字符边界
3. **关键词匹配**: 优先匹配带有 "verification code"、"验证码" 等关键词的内容
4. **多模式匹配**: 支持多种验证码格式（6位数字、字母数字混合等）

### 自定义正则

可以通过 `code_pattern` 参数指定自定义的验证码正则表达式：

```python
code = mailbox.wait_for_code(
    account=account,
    code_pattern=r"(\d{4})",  # 匹配4位数字验证码
    timeout=120
)
```

## 故障排查

### 1. 账号文件格式错误

**错误信息**: `跳过格式错误的行`

**解决方法**:
- 确保每行使用 `----` 分隔字段
- 确保至少包含 4 个字段
- 检查是否有多余的空格或特殊字符

### 2. API 请求失败

**错误信息**: `HotmailAPI /api/mail-new 失败`

**解决方法**:
- 检查 API URL 是否正确
- 确认 refresh_token 和 client_id 是否有效
- 检查网络连接和代理配置
- 查看 API 服务日志

### 3. 验证码提取失败

**错误信息**: `等待验证码超时`

**解决方法**:
- 增加 timeout 时间
- 检查邮件是否真的到达
- 尝试使用自定义 code_pattern
- 检查 keyword 过滤是否过于严格

## 与其他邮箱服务的对比

| 特性 | HotmailAPI | AppleMail | LuckMail |
|------|-----------|-----------|----------|
| 账号来源 | 本地导入 | 本地导入 | API 分配 |
| 轮转机制 | ✅ | ✅ | ❌ |
| 代理支持 | ✅ | ✅ | ✅ |
| 自定义正则 | ✅ | ✅ | ✅ |
| 多文件夹 | ✅ | ✅ | ❌ |

## 注意事项

1. **Token 有效期**: Refresh Token 可能会过期，需要定期更新账号文件
2. **API 限流**: 注意 API 服务的请求频率限制
3. **账号安全**: 妥善保管账号文件，避免泄露
4. **并发限制**: 同一账号不应同时在多个任务中使用

## 更新日志

### v1.0.0 (2026-04-06)
- ✨ 初始版本
- ✅ 支持本地账号池导入
- ✅ 支持 API 获取新邮件
- ✅ 智能验证码提取
- ✅ 线程安全的账号管理
