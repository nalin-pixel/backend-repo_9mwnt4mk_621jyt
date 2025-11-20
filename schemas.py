"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (replace with your own):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# App-specific schema for project briefs
class ProjectBrief(BaseModel):
    """
    Project briefs submitted by users who want to create websites or apps
    Collection name: "projectbrief"
    """
    title: str = Field(..., description="Project title")
    type: str = Field(..., description="Type of project: website or app")
    description: str = Field(..., description="What do you want to build?")
    target_audience: Optional[str] = Field(None, description="Who is this for?")
    key_features: List[str] = Field(default_factory=list, description="List of desired features")
    style: Optional[str] = Field(None, description="Visual style or inspiration")
    budget: Optional[str] = Field(None, description="Budget range")
    deadline: Optional[str] = Field(None, description="Desired timeline/deadline")
    contact_email: Optional[str] = Field(None, description="Your contact email")
