import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import create_document, get_documents, db
from schemas import ProjectBrief

app = FastAPI(title="Builder Studio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Builder Studio backend is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Models for API
class BriefCreate(BaseModel):
    title: str
    type: str
    description: str
    target_audience: Optional[str] = None
    key_features: Optional[List[str]] = None
    style: Optional[str] = None
    budget: Optional[str] = None
    deadline: Optional[str] = None
    contact_email: Optional[str] = None

class BriefResponse(ProjectBrief):
    id: str

# Helper to get collection name from model
COLLECTION_BRIEF = ProjectBrief.__name__.lower()

@app.post("/api/briefs", response_model=dict)
def create_brief(payload: BriefCreate):
    try:
        brief = ProjectBrief(
            title=payload.title,
            type=payload.type,
            description=payload.description,
            target_audience=payload.target_audience,
            key_features=payload.key_features or [],
            style=payload.style,
            budget=payload.budget,
            deadline=payload.deadline,
            contact_email=payload.contact_email,
        )
        inserted_id = create_document(COLLECTION_BRIEF, brief)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/briefs", response_model=List[dict])
def list_briefs(limit: int = 20):
    try:
        docs = get_documents(COLLECTION_BRIEF, limit=limit)
        # Convert ObjectId to string if present
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
