"""
Order Management API
Handles order processing and tracking
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from models import Order, OrderCreate, OrderUpdate
from database import get_db

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("/")
async def list_orders(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db = Depends(get_db)
) -> List[Order]:
    """
    Retrieve a list of orders.
    
    - **status**: Filter by order status (pending, completed, cancelled)
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    return db.query_orders(status=status, skip=skip, limit=limit)


@router.post("/")
async def create_order(order: OrderCreate, db = Depends(get_db)) -> Order:
    """
    Create a new order.
    
    This endpoint creates a new order in the system.
    """
    return db.create_order(order)


@router.get("/{order_id}")
async def get_order(order_id: str, db = Depends(get_db)) -> Order:
    """Get details of a specific order."""
    order = db.get_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}")
async def update_order(
    order_id: str,
    order: OrderUpdate,
    db = Depends(get_db)
) -> Order:
    """Update an existing order."""
    updated = db.update_order(order_id, order)
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated


@router.delete("/{order_id}")
async def cancel_order(order_id: str, db = Depends(get_db)):
    """Cancel an order."""
    success = db.cancel_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order cancelled"}


@router.get("/{order_id}/status")
async def get_order_status(order_id: str, db = Depends(get_db)):
    """Get the current status of an order."""
    status = db.get_order_status(order_id)
    if not status:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order_id, "status": status}
