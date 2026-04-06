from __future__ import annotations

from typing import Optional
from urllib.parse import unquote, urlsplit, urlunsplit


def normalize_proxy_url(proxy_url: Optional[str]) -> Optional[str]:
    """
    规范化代理 URL。
    1. 支持 host:port:user:pass 格式并转换为 http://user:pass@host:port
    2. 将 socks5:// 规范化为 socks5h://，避免本地 DNS 泄漏。
    """
    if proxy_url is None:
        return None

    value = str(proxy_url).strip()
    if not value:
        return None

    # 特殊处理 host:port:user:pass 格式
    if "://" not in value:
        parts = value.split(":")
        if len(parts) == 4:
            host, port, user, password = parts
            return f"http://{user}:{password}@{host}:{port}"
        elif len(parts) == 2:
            # host:port 格式
            return f"http://{value}"

    parts = urlsplit(value)
    scheme = (parts.scheme or "").lower()
    if scheme == "socks5":
        parts = parts._replace(scheme="socks5h")
        return urlunsplit(parts)
    elif not scheme and parts.netloc:
        # 补全缺失的 http://
        return f"http://{value}"
        
    return value



def build_requests_proxy_config(proxy_url: Optional[str]) -> Optional[dict[str, str]]:
    if not proxy_url:
        return None
    return {"http": proxy_url, "https": proxy_url}


def build_playwright_proxy_config(proxy_url: Optional[str]) -> Optional[dict[str, str]]:
    if not proxy_url:
        return None

    parts = urlsplit(proxy_url)
    if not parts.scheme or not parts.hostname or parts.port is None:
        return {"server": proxy_url}

    config = {"server": f"{parts.scheme}://{parts.hostname}:{parts.port}"}
    if parts.username:
        config["username"] = unquote(parts.username)
    if parts.password:
        config["password"] = unquote(parts.password)
    return config
