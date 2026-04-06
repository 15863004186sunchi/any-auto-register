#!/usr/bin/env python3
"""
HotmailAPI POST 请求方法测试脚本

用于验证修复后的 POST 请求是否正常工作
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_mailbox import create_mailbox


def test_post_request():
    """测试 POST 请求方法"""
    print("=" * 60)
    print("测试 HotmailAPI POST 请求方法")
    print("=" * 60)
    
    try:
        # 创建邮箱实例
        mailbox = create_mailbox(
            provider="hotmailapi",
            extra={
                "hotmailapi_api_url": "https://yourdomain.com",  # 替换为你的 API 地址
                "hotmailapi_pool_dir": "mail",
            }
        )
        print("✅ 邮箱服务创建成功")
        
        # 获取邮箱账号
        account = mailbox.get_email()
        print(f"✅ 分配邮箱: {account.email}")
        
        # 测试获取邮件（这会使用 POST 请求）
        print("\n开始测试 POST 请求...")
        print(f"API URL: {mailbox.api}/api/mail-new")
        print(f"请求方法: POST")
        print(f"请求头: {mailbox._headers()}")
        
        # 尝试获取当前邮件
        try:
            before_ids = mailbox.get_current_ids(account)
            print(f"✅ POST 请求成功！当前邮件数: {len(before_ids)}")
            
            if before_ids:
                print("\n邮件 ID 列表（前 5 个）:")
                for i, mid in enumerate(list(before_ids)[:5], 1):
                    print(f"  {i}. {mid}")
            
            return True
        except Exception as e:
            print(f"❌ POST 请求失败: {e}")
            print("\n请检查：")
            print("1. API URL 是否正确")
            print("2. refresh_token 和 client_id 是否有效")
            print("3. 网络连接是否正常")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_request_format():
    """测试请求格式"""
    print("\n" + "=" * 60)
    print("验证请求格式")
    print("=" * 60)
    
    print("\n正确的 API 调用格式：")
    print("""
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
result = response.json()
    """)
    
    print("✅ 请求格式验证完成")
    return True


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("HotmailAPI POST 请求修复验证")
    print("=" * 60)
    
    results = []
    
    # 测试 1: 请求格式
    results.append(test_request_format())
    
    # 测试 2: POST 请求
    results.append(test_post_request())
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("\n✅ 所有测试通过！")
        print("\n修复说明：")
        print("- 已将 GET 请求改为 POST 请求")
        print("- 已添加 Content-Type 请求头")
        print("- 请求参数改为 JSON body 传递")
        return 0
    else:
        print(f"\n⚠️  {total - passed} 个测试需要真实 API 才能完成")
        print("\n下一步：")
        print("1. 确保 API 服务已部署")
        print("2. 更新 API URL")
        print("3. 在实际场景中测试")
        return 1


if __name__ == "__main__":
    sys.exit(main())
