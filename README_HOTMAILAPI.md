# HotmailAPI 邮箱服务集成

## 📋 概述

本项目已成功集成 HotmailAPI 邮箱服务，支持从本地文件导入 Hotmail/Outlook 账号池，并通过第三方 API 获取验证码。

## ✨ 主要特性

- 📦 **本地账号池**：从文件批量导入邮箱账号
- 🔄 **自动轮转**：智能轮转使用账号池中的邮箱
- 📧 **API 集成**：通过 API 获取新邮件
- 🔍 **智能提取**：增强的验证码提取算法
- 🔒 **线程安全**：支持多线程并发使用
- 🌐 **代理支持**：支持配置 HTTP/HTTPS 代理

## 🚀 快速开始

### 1. 准备账号文件

在 `mail/` 目录创建账号文件（例如 `hotmail_accounts.txt`）：

```
email----password----client_id----refresh_token
```

示例已提供：`mail/hotmail_accounts_example.txt`

### 2. 使用代码

```python
from core.base_mailbox import create_mailbox

# 创建邮箱服务
mailbox = create_mailbox(
    provider="hotmailapi",
    extra={
        "hotmailapi_api_url": "https://yourdomain.com",
        "hotmailapi_pool_dir": "mail",
    }
)

# 获取邮箱并等待验证码
account = mailbox.get_email()
before_ids = mailbox.get_current_ids(account)
code = mailbox.wait_for_code(account, timeout=120, before_ids=before_ids)
print(f"验证码: {code}")
```

### 3. 测试

```bash
python scripts/test_hotmailapi.py
```

## 📚 文档

| 文档 | 说明 |
|------|------|
| [使用说明（中文）](docs/hotmailapi_使用说明.md) | 详细的中文使用教程 |
| [快速开始（英文）](docs/hotmailapi_quickstart.md) | 快速上手指南 |
| [集成文档（英文）](docs/hotmailapi_integration.md) | 完整的技术文档 |
| [集成总结](docs/hotmailapi_summary.md) | 集成工作总结 |

## 📁 文件结构

```
.
├── core/
│   └── base_mailbox.py              # 新增 HotmailAPIMailbox 类
├── mail/
│   └── hotmail_accounts_example.txt # 示例账号文件
├── docs/
│   ├── hotmailapi_integration.md    # 完整文档（英文）
│   ├── hotmailapi_quickstart.md     # 快速开始（英文）
│   ├── hotmailapi_使用说明.md        # 使用说明（中文）
│   └── hotmailapi_summary.md        # 集成总结
├── scripts/
│   └── test_hotmailapi.py           # 测试脚本
└── README_HOTMAILAPI.md             # 本文档
```

## ⚙️ 配置参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `hotmailapi_api_url` | ✅ | - | API 服务地址 |
| `hotmailapi_pool_dir` | ❌ | `mail` | 账号文件目录 |
| `hotmailapi_pool_file` | ❌ | - | 指定账号文件路径 |
| `hotmailapi_mailbox` | ❌ | `INBOX` | 邮箱文件夹 |

## 🔌 API 接口

你的 API 服务需要提供以下接口：

```
GET /api/mail-new
参数：
  - refresh_token: OAuth refresh token
  - client_id: OAuth client ID
  - email: 邮箱地址
  - mailbox: 邮箱文件夹（默认 INBOX）
  - response_type: json

返回：JSON 格式的邮件列表
```

## 💡 使用示例

### 基本用法

```python
from core.base_mailbox import create_mailbox

mailbox = create_mailbox(
    provider="hotmailapi",
    extra={
        "hotmailapi_api_url": "https://yourdomain.com",
        "hotmailapi_pool_dir": "mail",
    }
)

account = mailbox.get_email()
code = mailbox.wait_for_code(account, timeout=120)
```

### 使用代理

```python
mailbox = create_mailbox(
    provider="hotmailapi",
    extra={
        "hotmailapi_api_url": "https://yourdomain.com",
        "hotmailapi_pool_dir": "mail",
    },
    proxy="http://127.0.0.1:7890"
)
```

### 自定义验证码正则

```python
code = mailbox.wait_for_code(
    account=account,
    code_pattern=r"(\d{4})",  # 匹配4位数字
    timeout=120
)
```

## ❓ 常见问题

### Q: 如何获取 refresh_token 和 client_id？

A: 需要在 Azure Portal 注册应用并配置 OAuth 权限（Mail.Read），然后通过 OAuth 流程获取。

### Q: 账号文件格式错误怎么办？

A: 确保使用 `----`（4个短横线）分隔字段，每行必须包含完整的 4 个字段。

### Q: API 请求失败怎么办？

A: 检查 API URL、refresh_token 是否有效、网络连接是否正常。

### Q: 验证码提取不准确怎么办？

A: 使用 `code_pattern` 参数指定自定义正则表达式。

## 🔧 技术细节

### 验证码提取算法

- URL 过滤：避免误提取链接中的数字
- 边界检测：严格匹配验证码边界
- 关键词优先：优先匹配带关键词的验证码
- 多格式支持：支持 4-8 位数字或字母数字混合

### 线程安全

使用类级别的锁和缓存，支持多线程并发访问。

### 轮转机制

自动循环使用账号池中的邮箱，用完后回到第一个。

## ⚠️ 注意事项

1. **Token 管理**：refresh_token 可能会过期，需要定期更新
2. **API 限流**：注意请求频率限制
3. **账号安全**：不要将账号文件提交到版本控制
4. **并发限制**：同一账号不要在多个任务中同时使用

## 📝 更新日志

### v1.0.0 (2026-04-06)
- ✨ 初始版本
- ✅ 支持本地账号池导入
- ✅ 支持 API 获取新邮件
- ✅ 智能验证码提取
- ✅ 线程安全的账号管理
- ✅ 完整的文档和测试

## 📞 支持

如有问题，请查看：
1. [中文使用说明](docs/hotmailapi_使用说明.md)
2. [测试脚本](scripts/test_hotmailapi.py)
3. [示例账号文件](mail/hotmail_accounts_example.txt)

---

**集成完成时间**: 2026-04-06  
**集成状态**: ✅ 已完成并测试
