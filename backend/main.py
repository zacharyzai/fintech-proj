from fastapi import FastAPI
from app.core.database import supabase

app = FastAPI()

@app.get("/test-db")
def test_db():
    result = supabase.table("accounts").select("*").execute()
    return {"status": "connected", "data": result.data}