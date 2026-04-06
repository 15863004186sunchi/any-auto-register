# HotmailAPI 快速开始指南

## 快速开始

### 1. 准备账号文件

创建 `mail/hotmail_accounts.txt` 文件，格式如下：

```
email----password----client_id----refresh_token
```

示例：
```
user1@hotmail.com----pass123----9e5f94bc-e8a4-4e73-b8be-63364c29d753----M.C508_BAY.0.U.-CtJ4G35AD2YZGqZKsoEb4qEi1cUS6Hcn...
user2@hotmail.com----pass456----9e5f94bc-e8a4-4e73-b8be-63364c29d753----M.C547_BAY.0.U.-CuWrl5Agd5zDDc0ZdGd0IsAFqGLz7eD...
```

### 2. 配置 API 服务

确保你的 API 服务已部署并可访问，API 接口格式：

```
GET /api/mail-new?refresh_token={token}&client_id={id}&email={email}&mailbox=INBOX&response_type=json
```

### 3. 在代码中使用

```python
from core.base_mailbox import create_mailbox

# 创建邮箱实例
mailbox = create_mailbox(
    provider="hotmailapi",
    extra={
        "hotmailapi_api_url": "https://yourdomain.com",
        "hotmailapi_pool_dir": "mail",
    }
)

# 获取邮箱
account = mailbox.get_email()
print(f"使用邮箱: {account.email}")

# 获取当前邮件 ID（用于过滤）
before_ids = mailbox.get_current_ids(account)

# 发送验证码...（你的业务逻辑）

# 等待验证码
code = mailbox.wait_for_code(
    account=account,
    timeout=120,
    before_ids=before_ids,
)
print(f"验证码: {code}")
```

### 4. 在平台配置中使用

如果你的项目支持配置文件，可以这样配置：

```json
{
  "mailbox": {
    "provider": "hotmailapi",
    "hotmailapi_api_url": "https://yourdomain.com",
    "hotmailapi_pool_dir": "mail",
    "hotmailapi_mailbox": "INBOX"
  }
}
```

## 测试

运行测试脚本验证配置：

```bash
python scripts/test_hotmailapi.py
```

## 常见问题

### Q: 如何获取 refresh_token 和 client_id？

A: 这些是 Microsoft OAuth 的凭证，需要：
1. 在 Azure Portal 注册应用
2. 配置 OAuth 权限（Mail.Read）
3. 通过 OAuth 流程获取 refresh_token

### Q: 账号池文件放在哪里？

A: 默认在 `mail/` 目录下，文件名任意（.txt 后缀）。也可以通过 `hotmailapi_pool_file` 指定完整路径。

### Q: 支持多个账号文件吗？

A: 目前每个实例只支持一个账号文件。如果需要使用多个文件，可以创建多个 mailbox 实例。

### Q: 验证码提取不准确怎么办？

A: 可以通过 `code_pattern` 参数指定自定义正则表达式：

```python
code = mailbox.wait_for_code(
    account=account,
    code_pattern=r"验证码[：:]\s*(\d{6})",  # 自定义正则
    timeout=120,
)
```

### Q: API 请求失败怎么办？

A: 检查以下几点：
1. API URL 是否正确
2. refresh_token 是否过期
3. 网络连接是否正常
4. 查看日志中的详细错误信息

## 下一步

- 查看完整文档：[HotmailAPI 集成说明](./hotmailapi_integration.md)
- 了解验证码提取算法
- 配置代理支持
- 集成到你的自动化流程中
