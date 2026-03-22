from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from middlewares.exception_handlers import catch_exception_middleware
from router.upload_pdfs import router as upload_router
from router.ask_question import router as ask_router

app = FastAPI(title = "AI Medical Chatbot Backend", description = "This is the backend for the AI Medical Chatbot project. It provides APIs for handling user interactions and processing medical data.", version = "1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers   
    allow_credentials=True, # Allow cookies and authentication headers
)

# middleware exceptions handlers
app.middleware("http")(catch_exception_middleware)
# routers
# 1. upload pdf documents
app.include_router(upload_router)
# 2. asking query
app.include_router(ask_router)