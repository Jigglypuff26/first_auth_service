from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api.endpoints import auth, users

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Auth Service API", "version": settings.VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}