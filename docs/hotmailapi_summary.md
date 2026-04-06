# HotmailAPI 集成总结

## 已完成的工作

### 1. 核心代码实现

✅ **新增 `HotmailAPIMailbox` 类** (`core/base_mailbox.py`)
- 支持从本地文件导入邮箱账号池
- 自动轮转使用账号（线程安全）
- 通过 API 获取新邮件
- 智能验证码提取
- 支持代理配置

✅ **在工厂方法中注册** (`create_mailbox` 函数)
- 添加 `hotmailapi` provider 支持
- 配置参数映射

### 2. 文档

✅ **完整集成文档** (`docs/hotmailapi_integration.md`)
- 功能特性说明
- 账号文件格式详解
- API 接口说明
- 配置方法
- 故障排查指南

✅ **快速开始指南** (`docs/hotmailapi_quickstart.md`)
- 英文版快速上手指南
- 常见问题解答

✅ **中文使用说明** (`docs/hotmailapi_使用说明.md`)
- 详细的中文使用教程
- 高级用法示例
- 完整代码示例

### 3. 示例和测试

✅ **示例账号文件** (`mail/hotmail_accounts_example.txt`)
- 包含你提供的 10 个示例账号
- 格式正确，可直接使用

✅ **测试脚本** (`scripts/test_hotmailapi.py`)
- 测试账号池加载
- 测试轮转机制
- 测试配置选项

## 使用方法

### 基本用法

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
```

### 配置参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `hotmailapi_api_url` | API 服务地址 | `https://yourdomain.com` |
| `hotmailapi_pool_dir` | 账号文件目录 | `mail` |
| `hotmailapi_pool_file` | 指定账号文件 | `mail/accounts.txt` |
| `hotmailapi_mailbox` | 邮箱文件夹 | `INBOX` |

## 账号文件格式

```
email----password----client_id----refresh_token
```

示例：
```
user@hotmail.com----pass123----9e5f94bc-xxxx----M.C508_BAY.0.U.-CtJ4G35AD2YZ...
```

## API 接口要求

你的 API 服务需要提供以下接口：

```
GET /api/mail-new
参数：
  - refresh_token: string (必填)
  - client_id: string (必填)
  - email: string (必填)
  - mailbox: string (默认 INBOX)
  - response_type: string (默认 json)

返回：JSON 格式的邮件列表
```

## 核心特性

### 1. 账号池管理
- 从本地文件加载账号
- 自动轮转使用
- 线程安全
- 内存缓存

### 2. 智能验证码提取
- URL 过滤（避免误提取链接中的数字）
- 边界检测（严格匹配）
- 关键词优先（"验证码"、"verification code" 等）
- 支持自定义正则

### 3. 灵活配置
- 支持指定账号文件或目录
- 支持代理
- 支持自定义邮箱文件夹
- 支持关键词过滤

## 测试

运行测试脚本：

```bash
python scripts/test_hotmailapi.py
```

## 文件清单

```
core/
  └── base_mailbox.py          # 新增 HotmailAPIMailbox 类

mail/
  └── hotmail_accounts_example.txt  # 示例账号文件

docs/
  ├── hotmailapi_integration.md     # 完整集成文档（英文）
  ├── hotmailapi_quickstart.md      # 快速开始（英文）
  ├── hotmailapi_使用说明.md         # 使用说明（中文）
  └── hotmailapi_summary.md         # 本文档

scripts/
  └── test_hotmailapi.py       # 测试脚本
```

## 下一步

1. **部署 API 服务**
   - 确保 API 服务可访问
   - 测试 `/api/mail-new` 接口

2. **准备账号文件**
   - 将你的账号信息保存到 `mail/` 目录
   - 确保格式正确

3. **测试集成**
   - 运行测试脚本验证
   - 在实际场景中测试

4. **集成到业务流程**
   - 在注册流程中使用
   - 配置日志和监控

## 注意事项

1. **Token 管理**
   - refresh_token 可能会过期
   - 需要定期更新账号文件

2. **API 限流**
   - 注意请求频率
   - 避免触发限流

3. **账号安全**
   - 不要将账号文件提交到版本控制
   - 妥善保管敏感信息

4. **错误处理**
   - 捕获并处理 API 错误
   - 记录详细日志便于排查

## 技术细节

### 验证码提取算法

使用 `_yyds_safe_extract` 方法，特点：
1. 先过滤 URL 链接
2. 检查字符边界
3. 优先匹配关键词附近的验证码
4. 支持 4-8 位数字或字母数字混合

### 线程安全

使用类级别的锁和缓存：
```python
_pool_lock = threading.Lock()
_pool_cache: dict[str, list[dict]] = {}
_pool_index: dict[str, int] = {}
```

### 轮转机制

```python
index = HotmailAPIMailbox._pool_index[pool_path]
record = pool[index]
HotmailAPIMailbox._pool_index[pool_path] = (index + 1) % len(pool)
```

## 支持

如有问题，请查看：
1. 文档：`docs/hotmailapi_*.md`
2. 测试脚本：`scripts/test_hotmailapi.py`
3. 示例文件：`mail/hotmail_accounts_example.txt`
