"""
MongoDB + FastAPI Example
Production-ready REST API with async MongoDB integration.
"""

from fastapi import FastAPI, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import os

# Pydantic models
class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserCreate(BaseModel):
    """User creation request"""
    email: EmailStr
    name: str
    age: Optional[int] = None


class UserResponse(BaseModel):
    """User response model"""
    id: str = Field(alias="_id")
    email: str
    name: str
    age: Optional[int] = None
    createdAt: datetime
    updatedAt: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


class OrderCreate(BaseModel):
    """Order creation request"""
    userId: str
    items: List[dict]
    totalAmount: float


class OrderResponse(BaseModel):
    """Order response model"""
    id: str = Field(alias="_id")
    userId: str
    orderNumber: str
    items: List[dict]
    totalAmount: float
    status: str
    createdAt: datetime

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}


# FastAPI application
app = FastAPI(title="MongoDB FastAPI Example")

# MongoDB client (initialized on startup)
mongodb_client: Optional[AsyncIOMotorClient] = None
db = None


@app.on_event("startup")
async def startup_db_client():
    """Initialize MongoDB connection on startup"""
    global mongodb_client, db

    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
    mongodb_client = AsyncIOMotorClient(
        mongodb_uri,
        maxPoolSize=50,
        minPoolSize=10,
        serverSelectionTimeoutMS=5000
    )
    db = mongodb_client.myapp

    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.orders.create_index([("userId", 1), ("createdAt", -1)])

    print("✓ Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_db_client():
    """Close MongoDB connection on shutdown"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("✓ Disconnected from MongoDB")


# User endpoints
@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Create a new user"""
    user_dict = user.dict()
    user_dict["createdAt"] = datetime.utcnow()
    user_dict["updatedAt"] = datetime.utcnow()

    try:
        result = await db.users.insert_one(user_dict)
        created_user = await db.users.find_one({"_id": result.inserted_id})
        return created_user
    except Exception as e:
        if "duplicate key error" in str(e):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users/{email}", response_model=UserResponse)
async def get_user(email: str):
    """Get user by email"""
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 20):
    """List all users with pagination"""
    users = await db.users.find().skip(skip).limit(limit).to_list(length=limit)
    return users


@app.put("/users/{email}", response_model=UserResponse)
async def update_user(email: str, user_update: dict):
    """Update user by email"""
    user_update["updatedAt"] = datetime.utcnow()

    result = await db.users.update_one(
        {"email": email},
        {"$set": user_update}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = await db.users.find_one({"email": email})
    return updated_user


@app.delete("/users/{email}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(email: str):
    """Soft delete user (mark as deleted)"""
    result = await db.users.update_one(
        {"email": email},
        {"$set": {"deleted": True, "deletedAt": datetime.utcnow()}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")


# Order endpoints
@app.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    """Create a new order"""
    # Verify user exists
    user = await db.users.find_one({"_id": ObjectId(order.userId)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Generate order number
    order_count = await db.orders.count_documents({})
    order_number = f"ORD-{datetime.utcnow().year}-{order_count + 1:06d}"

    order_dict = order.dict()
    order_dict["userId"] = ObjectId(order_dict["userId"])
    order_dict["orderNumber"] = order_number
    order_dict["status"] = "pending"
    order_dict["createdAt"] = datetime.utcnow()

    result = await db.orders.insert_one(order_dict)
    created_order = await db.orders.find_one({"_id": result.inserted_id})
    created_order["userId"] = str(created_order["userId"])
    return created_order


@app.get("/orders/{order_number}", response_model=OrderResponse)
async def get_order(order_number: str):
    """Get order by order number"""
    order = await db.orders.find_one({"orderNumber": order_number})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["userId"] = str(order["userId"])
    return order


@app.get("/users/{user_id}/orders", response_model=List[OrderResponse])
async def list_user_orders(user_id: str):
    """List all orders for a user"""
    orders = await db.orders.find(
        {"userId": ObjectId(user_id)}
    ).sort("createdAt", -1).to_list(length=100)

    for order in orders:
        order["userId"] = str(order["userId"])

    return orders


# Analytics endpoint (aggregation example)
@app.get("/analytics/revenue-by-user")
async def revenue_by_user():
    """Get total revenue by user (aggregation pipeline)"""
    pipeline = [
        # Group by userId
        {
            "$group": {
                "_id": "$userId",
                "totalRevenue": {"$sum": "$totalAmount"},
                "orderCount": {"$sum": 1},
                "avgOrderValue": {"$avg": "$totalAmount"}
            }
        },
        # Lookup user details
        {
            "$lookup": {
                "from": "users",
                "localField": "_id",
                "foreignField": "_id",
                "as": "user"
            }
        },
        # Unwind user array
        {"$unwind": "$user"},
        # Project final structure
        {
            "$project": {
                "_id": 0,
                "userId": {"$toString": "$_id"},
                "userName": "$user.name",
                "userEmail": "$user.email",
                "totalRevenue": {"$round": ["$totalRevenue", 2]},
                "orderCount": 1,
                "avgOrderValue": {"$round": ["$avgOrderValue", 2]}
            }
        },
        # Sort by revenue
        {"$sort": {"totalRevenue": -1}}
    ]

    results = await db.orders.aggregate(pipeline).to_list(length=100)
    return results


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Ping MongoDB
        await mongodb_client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
