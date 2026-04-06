#!/usr/bin/env python3
"""
HotmailAPI 调试脚本 - 用于排查验证码获取问题
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.base_mailbox import create_mailbox


def debug_api_response():
    """调试 API 返回的数据"""
    print("=" * 60)
    print("HotmailAPI 调试 - API 响应测试")
    print("=" * 60)
    
    # 创建邮箱实例
    mailbox = create_mailbox(
        provider="hotmailapi",
        extra={
            "hotmailapi_api_url": "你的API地址",  # 替换为你的 API 地址
            "hotmailapi_pool_dir": "mail",
        }
    )
    
    # 获取邮箱
    account = mailbox.get_email()
    print(f"\n使用邮箱: {account.email}")
    print(f"Client ID: {account.extra.get('client_id', 'N/A')[:20]}...")
    print(f"Refresh Token: {account.extra.get('refresh_token', 'N/A')[:30]}...")
    
    # 直接调用 API 查看返回数据
    print("\n" + "=" * 60)
    print("调用 API 获取邮件...")
    print("=" * 60)
    
    try:
        messages = mailbox._list_new_messages(
            account.extra['refresh_token'],
            account.extra['client_id'],
            account.email
        )
        
        print(f"\n✅ API 调用成功")
        print(f"返回邮件数: {len(messages)}")
        
        if messages:
            print("\n" + "=" * 60)
            print("邮件详情:")
            print("=" * 60)
            
            for i, msg in enumerate(messages, 1):
                print(f"\n--- 邮件 {i} ---")
                print(f"原始数据: {json.dumps(msg, ensure_ascii=False, indent=2)}")
                
                # 提取邮件 ID
                msg_id = mailbox._extract_message_id(msg, i-1)
                print(f"\n提取的邮件 ID: {msg_id}")
                
                # 构建搜索文本
                search_text = mailbox._build_search_text(msg)
                print(f"\n搜索文本: {search_text[:200]}...")
                
                # 尝试提取验证码
                code = mailbox._extract_code_from_message(msg)
                print(f"\n提取的验证码: {code if code else '❌ 未提取到'}")
                
                if not code:
                    print("\n⚠️ 验证码提取失败，尝试手动提取...")
                    # 尝试使用不同的方法
                    for key in msg.keys():
                        value = str(msg.get(key, ''))
                        if '002002' in value or 'code' in key.lower():
                            print(f"  发现可能包含验证码的字段: {key} = {value[:100]}")
        else:
            print("\n❌ 没有返回任何邮件")
            print("可能的原因:")
            print("1. API 返回的数据格式不正确")
            print("2. 邮箱中确实没有新邮件")
            print("3. API 参数配置错误")
            
    except Exception as e:
        print(f"\n❌ API 调用失败: {e}")
        import traceback
        traceback.print_exc()


def debug_code_extraction():
    """调试验证码提取逻辑"""
    print("\n" + "=" * 60)
    print("验证码提取测试")
    print("=" * 60)
    
    from core.base_mailbox import BaseMailbox
    
    # 创建一个临时实例用于测试
    class TempMailbox(BaseMailbox):
        def get_email(self):
            pass
        def wait_for_code(self, *args, **kwargs):
            pass
        def get_current_ids(self, *args):
            return set()
    
    mb = TempMailbox()
    
    # 测试不同的文本格式
    test_cases = [
        "Your ChatGPT code is 002002",
        "验证码: 002002",
        "code: 002002",
        "002002",
        "Your code is: 002002",
        "主题: Your ChatGPT code is 002002\n内容: Please use this code",
    ]
    
    print("\n测试用例:")
    for i, text in enumerate(test_cases, 1):
        code = mb._yyds_safe_extract(text)
        status = "✅" if code == "002002" else "❌"
        print(f"{status} 测试 {i}: {text[:50]}")
        print(f"   提取结果: {code}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("HotmailAPI 问题诊断工具")
    print("=" * 60)
    
    print("\n请选择调试模式:")
    print("1. 调试 API 响应（查看 API 返回的数据）")
    print("2. 调试验证码提取（测试提取算法）")
    print("3. 全部运行")
    
    choice = input("\n请输入选项 (1/2/3): ").strip()
    
    if choice == "1":
        debug_api_response()
    elif choice == "2":
        debug_code_extraction()
    elif choice == "3":
        debug_code_extraction()
        debug_api_response()
    else:
        print("无效选项")
