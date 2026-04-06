# HotmailAPI 邮箱服务使用说明

## 简介

HotmailAPI 是一个集成到项目中的 Hotmail/Outlook 邮箱服务，支持：
- 📦 从本地文件批量导入邮箱账号
- 🔄 自动轮转使用账号池
- 📧 通过 API 获取新邮件
- 🔍 智能提取验证码

## 快速开始

### 第一步：准备邮箱账号文件

在 `mail/` 目录下创建一个 `.txt` 文件（例如 `hotmail_accounts.txt`），每行一个账号：

```
邮箱地址----密码----client_id----refresh_token
```

**示例**：
```
CaesarPhryne2274@hotmail.com----eg699579----9e5f94bc-e8a4-4e73-b8be-63364c29d753----M.C508_BAY.0.U.-CtJ4G35AD2YZGqZKsoEb4qEi1cUS6Hcn36nhbJq8SSvWsTJFDdgnbuEyxPSjxeIk4bINeaBO7HufyI4!XWyRsoZdy1C3imxO54Depfdw8JcJDz7ZmoR3xftDzvlYiNB*QHruRpha0SZPxLirgdMZYUjoQXNlW6s2k44ng9JHZMVWtE*JepU*TiZ2rkM*jR2*PtgqTYyx0vMLKccm0DnfahzDAN6lerGzLL2d0TpT*OcnTwK7xQgh1z3GYbjhWO6zchKBXgnrAn54YGcMG7aHIsksR2Y7IYaFmwPd0mR7e!TT4zapKTMErk3q91fvVMRNXePNlnFEhoTqWDLWCXEpMeC2UKpBrxm9eNpgMnrSb04r*AlwzdbYSHm*vrWrViW3OQ$$
```

**注意**：
- 使用 `----` 分隔各个字段（4个短横线）
- 每行必须包含完整的 4 个字段
- 可以添加多个账号，系统会自动轮转使用

### 第二步：配置 API 服务地址

你需要一个提供以下接口的 API 服务：

```
POST /api/mail-new
请求头：
  Content-Type: application/json
  
请求体：
  - refresh_token: OAuth refresh token
  - client_id: OAuth client ID
  - email: 邮箱地址
  - mailbox: 邮箱文件夹（默认 INBOX）
  - response_type: json
```

### 第三步：在代码中使用

```python
from core.base_mailbox import create_mailbox

# 1. 创建邮箱服务实例
mailbox = create_mailbox(
    provider="hotmailapi",
    extra={
        "hotmailapi_api_url": "https://yourdomain.com",  # 你的 API 地址
        "hotmailapi_pool_dir": "mail",                    # 账号文件所在目录
        "hotmailapi_mailbox": "INBOX",                    # 邮箱文件夹
    },
    proxy=None  # 如果需要代理，填写代理地址
)

# 2. 获取一个邮箱账号
account = mailbox.get_email()
print(f"分配的邮箱: {account.email}")

# 3. 记录当前邮件 ID（用于过滤旧邮件）
before_ids = mailbox.get_current_ids(account)

# 4. 发送验证码到该邮箱
# ... 你的业务逻辑 ...

# 5. 等待并获取验证码
code = mailbox.wait_for_code(
    account=account,
    keyword="",           # 可选：邮件关键词过滤
    timeout=120,          # 超时时间（秒）
    before_ids=before_ids,
    code_pattern=None,    # 可选：自定义验证码正则
)

print(f"收到验证码: {code}")
```

## 配置参数详解

| 参数名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `hotmailapi_api_url` | ✅ | - | API 服务地址 |
| `hotmailapi_pool_dir` | ❌ | `mail` | 账号文件所在目录 |
| `hotmailapi_pool_file` | ❌ | - | 指定账号文件完整路径（优先级高于 pool_dir） |
| `hotmailapi_mailbox` | ❌ | `INBOX` | 邮箱文件夹名称 |

## 高级用法

### 1. 指定特定的账号文件

```python
mailbox = create_mailbox(
    provider="hotmailapi",
    extra={
        "hotmailapi_api_url": "https://yourdomain.com",
        "hotmailapi_pool_file": "mail/my_hotmail_accounts.txt",  # 指定文件
    }
)
```

### 2. 使用代理

```python
mailbox = create_mailbox(
    provider="hotmailapi",
    extra={
        "hotmailapi_api_url": "https://yourdomain.com",
        "hotmailapi_pool_dir": "mail",
    },
    proxy="http://127.0.0.1:7890"  # 代理地址
)
```

### 3. 自定义验证码正则

```python
# 匹配 4 位数字验证码
code = mailbox.wait_for_code(
    account=account,
    code_pattern=r"(\d{4})",
    timeout=120,
)

# 匹配带中文提示的验证码
code = mailbox.wait_for_code(
    account=account,
    code_pattern=r"验证码[：:]\s*(\d{6})",
    timeout=120,
)
```

### 4. 关键词过滤

```python
# 只处理包含特定关键词的邮件
code = mailbox.wait_for_code(
    account=account,
    keyword="OpenAI",  # 只处理包含 "OpenAI" 的邮件
    timeout=120,
)
```

## 测试

运行测试脚本验证配置是否正确：

```bash
python scripts/test_hotmailapi.py
```

## 常见问题

### 1. 提示"邮箱池文件不存在"

**原因**：找不到账号文件

**解决**：
- 检查 `mail/` 目录是否存在
- 确认目录中有 `.txt` 文件
- 或者使用 `hotmailapi_pool_file` 指定完整路径

### 2. 提示"格式错误的行"

**原因**：账号文件格式不正确

**解决**：
- 确保使用 `----`（4个短横线）分隔字段
- 每行必须有 4 个字段
- 检查是否有多余的空格或换行

### 3. API 请求失败

**原因**：API 服务不可用或 token 过期

**解决**：
- 检查 API 地址是否正确
- 确认 refresh_token 是否有效
- 检查网络连接
- 查看详细错误日志

### 4. 等待验证码超时

**原因**：邮件未到达或验证码提取失败

**解决**：
- 增加 timeout 时间
- 检查邮件是否真的发送了
- 尝试使用 `code_pattern` 自定义正则
- 检查 `keyword` 是否过滤掉了邮件

### 5. 验证码提取不准确

**原因**：默认正则无法匹配特殊格式

**解决**：
- 查看邮件原文，确定验证码格式
- 使用 `code_pattern` 参数指定自定义正则
- 参考文档中的正则示例

## 账号池管理

### 轮转机制

系统会自动轮转使用账号池中的邮箱：
1. 第一次调用 `get_email()` 返回第 1 个账号
2. 第二次调用返回第 2 个账号
3. 依此类推，用完后回到第 1 个账号

### 线程安全

账号池使用线程锁保护，支持多线程并发使用。

### 缓存机制

账号文件在首次加载后会缓存在内存中，不会重复读取。

## 验证码提取算法

系统使用增强的验证码提取算法，具有以下特性：

1. **URL 过滤**：自动过滤邮件中的链接，避免误提取
2. **边界检测**：严格检查验证码前后的字符
3. **关键词优先**：优先匹配带有"验证码"等关键词的内容
4. **多格式支持**：支持 4-8 位数字或字母数字混合

## 注意事项

1. **Token 有效期**：refresh_token 可能会过期，需要定期更新
2. **API 限流**：注意 API 服务的请求频率限制
3. **账号安全**：妥善保管账号文件，不要提交到版本控制
4. **并发使用**：同一账号不要在多个任务中同时使用

## 完整示例

```python
from core.base_mailbox import create_mailbox

def register_with_hotmail():
    """使用 HotmailAPI 进行注册的完整示例"""
    
    # 创建邮箱服务
    mailbox = create_mailbox(
        provider="hotmailapi",
        extra={
            "hotmailapi_api_url": "https://yourdomain.com",
            "hotmailapi_pool_dir": "mail",
        }
    )
    
    # 获取邮箱
    account = mailbox.get_email()
    email = account.email
    print(f"使用邮箱: {email}")
    
    # 记录当前邮件 ID
    before_ids = mailbox.get_current_ids(account)
    
    # 发起注册请求（示例）
    # register_api.send_verification_code(email)
    
    # 等待验证码
    try:
        code = mailbox.wait_for_code(
            account=account,
            keyword="",
            timeout=120,
            before_ids=before_ids,
        )
        print(f"收到验证码: {code}")
        
        # 提交验证码完成注册
        # register_api.verify_code(email, code)
        
        return True
    except TimeoutError:
        print("等待验证码超时")
        return False

if __name__ == "__main__":
    register_with_hotmail()
```

## 更多信息

- 详细文档：[HotmailAPI 集成说明](./hotmailapi_integration.md)
- 快速开始：[HotmailAPI 快速开始](./hotmailapi_quickstart.md)
- 测试脚本：`scripts/test_hotmailapi.py`
