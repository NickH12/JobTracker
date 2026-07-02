#create fastapi
from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.api.v1.companies import router as company_router
from app.api.v1.applications import router as application_router

app = FastAPI(title="Job Application Tracker",
               description="A simple FastAPI application")

@app.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(company_router, prefix="/companies", tags=["companies"])
app.include_router(application_router, prefix="/applications", tags=["applications"])