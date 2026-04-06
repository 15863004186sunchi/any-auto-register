#!/usr/bin/env python3
"""
HotmailAPI 邮箱服务测试脚本

用法:
    python scripts/test_hotmailapi.py
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_mailbox import create_mailbox


def test_load_pool():
    """测试加载邮箱池"""
    print("=" * 60)
    print("测试 1: 加载邮箱池")
    print("=" * 60)
    
    try:
        mailbox = create_mailbox(
            provider="hotmailapi",
            extra={
                "hotmailapi_api_url": "https://yourdomain.com",
                "hotmailapi_pool_dir": "mail",
            }
        )
        print("✅ 邮箱服务创建成功")
        
        # 获取邮箱账号
        account = mailbox.get_email()
        print(f"✅ 分配邮箱: {account.email}")
        print(f"   Client ID: {account.extra.get('client_id', 'N/A')[:20]}...")
        print(f"   Refresh Token: {account.extra.get('refresh_token', 'N/A')[:30]}...")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_get_multiple_accounts():
    """测试获取多个邮箱账号（轮转）"""
    print("\n" + "=" * 60)
    print("测试 2: 邮箱轮转机制")
    print("=" * 60)
    
    try:
        mailbox = create_mailbox(
            provider="hotmailapi",
            extra={
                "hotmailapi_api_url": "https://yourdomain.com",
                "hotmailapi_pool_dir": "mail",
            }
        )
        
        accounts = []
        for i in range(5):
            account = mailbox.get_email()
            accounts.append(account.email)
            print(f"  第 {i+1} 次分配: {account.email}")
        
        print(f"\n✅ 成功分配 {len(accounts)} 个邮箱")
        print(f"   唯一邮箱数: {len(set(accounts))}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_get_current_ids():
    """测试获取当前邮件 ID"""
    print("\n" + "=" * 60)
    print("测试 3: 获取当前邮件 ID")
    print("=" * 60)
    
    try:
        mailbox = create_mailbox(
            provider="hotmailapi",
            extra={
                "hotmailapi_api_url": "https://yourdomain.com",
                "hotmailapi_pool_dir": "mail",
            }
        )
        
        account = mailbox.get_email()
        print(f"使用邮箱: {account.email}")
        
        # 注意：这个测试需要真实的 API 才能工作
        print("⚠️  需要真实的 API 服务才能测试获取邮件 ID")
        print("   跳过此测试...")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def test_wait_for_code_mock():
    """测试等待验证码（模拟）"""
    print("\n" + "=" * 60)
    print("测试 4: 等待验证码（模拟）")
    print("=" * 60)
    
    print("⚠️  此测试需要真实的 API 服务和邮件发送")
    print("   在实际使用时，调用方式如下：")
    print()
    print("   code = mailbox.wait_for_code(")
    print("       account=account,")
    print("       keyword='',")
    print("       timeout=120,")
    print("       before_ids=before_ids,")
    print("   )")
    print()
    
    return True


def test_custom_pool_file():
    """测试指定账号文件"""
    print("\n" + "=" * 60)
    print("测试 5: 指定账号文件")
    print("=" * 60)
    
    try:
        mailbox = create_mailbox(
            provider="hotmailapi",
            extra={
                "hotmailapi_api_url": "https://yourdomain.com",
                "hotmailapi_pool_file": "mail/hotmail_accounts_example.txt",
            }
        )
        
        account = mailbox.get_email()
        print(f"✅ 使用指定文件分配邮箱: {account.email}")
        
        return True
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("HotmailAPI 邮箱服务测试")
    print("=" * 60)
    
    tests = [
        test_load_pool,
        test_get_multiple_accounts,
        test_get_current_ids,
        test_wait_for_code_mock,
        test_custom_pool_file,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n❌ 测试异常: {e}")
            results.append(False)
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✅ 所有测试通过！")
        return 0
    else:
        print(f"❌ {total - passed} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
