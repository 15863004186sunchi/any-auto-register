from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
from core.db import ProxyModel, get_session
from core.proxy_pool import proxy_pool

router = APIRouter(prefix="/proxies", tags=["proxies"])


class ProxyCreate(BaseModel):
    url: str
    region: str = ""


class ProxyBulkCreate(BaseModel):
    proxies: list[str]
    region: str = ""


class ProxyBulkDelete(BaseModel):
    ids: Optional[list[int]] = None


class ProxySyncRequest(BaseModel):
    url: Optional[str] = None
    region: str = ""


@router.get("")
def list_proxies(session: Session = Depends(get_session)):
    items = session.exec(select(ProxyModel)).all()
    return items


@router.post("")
def add_proxy(body: ProxyCreate, session: Session = Depends(get_session)):
    existing = session.exec(select(ProxyModel).where(ProxyModel.url == body.url)).first()
    if existing:
        raise HTTPException(400, "代理已存在")
    p = ProxyModel(url=body.url, region=body.region)
    session.add(p)
    session.commit()
    session.refresh(p)
    return p


@router.post("/bulk")
def bulk_add_proxies(body: ProxyBulkCreate, session: Session = Depends(get_session)):
    added = 0
    for url in body.proxies:
        url = url.strip()
        if not url:
            continue
        existing = session.exec(select(ProxyModel).where(ProxyModel.url == url)).first()
        if not existing:
            session.add(ProxyModel(url=url, region=body.region))
            added += 1
    session.commit()
    return {"added": added}


@router.delete("/{proxy_id}")
def delete_proxy(proxy_id: int, session: Session = Depends(get_session)):
    p = session.get(ProxyModel, proxy_id)
    if not p:
        raise HTTPException(404, "代理不存在")
    session.delete(p)
    session.commit()
    return {"ok": True}


@router.delete("/bulk/clear")
def bulk_delete_proxies(body: ProxyBulkDelete = ProxyBulkDelete(), session: Session = Depends(get_session)):
    from sqlmodel import delete
    ids = body.ids
    if not ids:
        statement = delete(ProxyModel)
    else:
        statement = delete(ProxyModel).where(ProxyModel.id.in_(ids))
    session.exec(statement)
    session.commit()
    return {"ok": True}


@router.patch("/{proxy_id}/toggle")
def toggle_proxy(proxy_id: int, session: Session = Depends(get_session)):
    p = session.get(ProxyModel, proxy_id)
    if not p:
        raise HTTPException(404, "代理不存在")
    p.is_active = not p.is_active
    session.add(p)
    session.commit()
    return {"is_active": p.is_active}


@router.post("/check")
def check_proxies(background_tasks: BackgroundTasks):
    background_tasks.add_task(proxy_pool.check_all)
    return {"message": "检测任务已启动"}


@router.post("/sync")
def sync_proxies(body: ProxySyncRequest, session: Session = Depends(get_session)):
    import requests
    from core.config_store import config_store
    
    url = (body.url or config_store.get("proxy_sync_url", "")).strip()
    if not url:
        raise HTTPException(400, "未配置同步 URL，请在设置中保存或直接请求时提供")
    
    if not url.startswith("http"):
        raise HTTPException(400, "无效的同步 URL")

    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        content = r.text
    except Exception as e:
        raise HTTPException(500, f"无法从 URL 获取列表: {e}")
    
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    added = 0
    for line in lines:
        if line.startswith("#"): continue
        
        # 尝试格式解析: host:port:user:pass 或 host:port 或 user:pass@host:port
        proxy_url = line
        if "://" not in line:
            parts = line.split(":")
            if len(parts) == 4:
                # Webshare 常见格式 host:port:user:pass
                h, p, u, pw = parts
                proxy_url = f"http://{u}:{pw}@{h}:{p}"
            elif len(parts) == 2:
                # host:port
                h, p = parts
                proxy_url = f"http://{h}:{p}"
            # 如果已经是 user:pass@host:port 但没有 http://
            elif "@" in line:
                proxy_url = f"http://{line}"
        
        existing = session.exec(select(ProxyModel).where(ProxyModel.url == proxy_url)).first()
        if not existing:
            session.add(ProxyModel(url=proxy_url, region=body.region))
            added += 1
            
    session.commit()
    return {"added": added, "total": len(lines)}
