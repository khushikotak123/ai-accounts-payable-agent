from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import threading
import time

from app.api.invoices import router as invoice_router
from app.agents.sla_agent import check_sla_breaches

# ✅ Create FastAPI App
app = FastAPI(
    title="AI Accounts Payable Employee (Offline RAG)",
    version="0.1.0"
)

# ======================================================
# ✅ Enable CORS (Frontend React Dashboard Support)
# React runs on localhost:5173
# Backend runs on localhost:8000
# ======================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (fine for demo)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# ✅ Include API Routers
# ======================================================
app.include_router(invoice_router)

# ======================================================
# ✅ Background SLA Monitor Thread
# Runs every 30 seconds to detect SLA breach risk
# ======================================================
def sla_monitor():
    while True:
        check_sla_breaches()
        time.sleep(30)


@app.on_event("startup")
def start_sla_thread():
    thread = threading.Thread(target=sla_monitor, daemon=True)
    thread.start()
    print("✅ SLA Proactive Monitor Started!")


# ======================================================
# ✅ Root Endpoint (Health Check)
# ======================================================
@app.get("/")
def home():
    return {
        "message": "AI Accounts Payable Employee is running ✅",
        "docs": "http://127.0.0.1:8000/docs"
    }
