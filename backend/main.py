import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import httpx
from pathlib import Path

from .config import REVENUE_API_URL, AGRICULTURE_API_URL, BACKEND_HOST, BACKEND_PORT
from .database import engine, Base, SessionLocal, get_db
from .models import Citizen, Service, Application, ConsentRecord, AuditEvent
from .api.v1.services_router import router as services_router
from .api.v1.applications_router import router as applications_router
from .api.v1.assistant_router import router as assistant_router

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("MahaSync.Core")


def seed_database():
    """Initializes tables and populates default demo data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Seed Citizens
        if not db.query(Citizen).filter(Citizen.id == "C001").first():
            c1 = Citizen(id="C001", name="Rahul Patil", email="rahul@mahasync.gov.in", phone="+91 98765 43210")
            c2 = Citizen(id="C002", name="Amit Deshmukh", email="amit@mahasync.gov.in", phone="+91 98765 43211")
            c3 = Citizen(id="C003", name="Priya Sharma", email="priya@mahasync.gov.in", phone="+91 98765 43212")
            db.add_all([c1, c2, c3])
            db.commit()

        # Seed Services
        if not db.query(Service).filter(Service.id == "SRV-AGRI-001").first():
            s1 = Service(
                id="SRV-AGRI-001",
                title="Agriculture Subsidy Scheme (DBT)",
                department="Department of Agriculture",
                category="Farmer Welfare",
                description="Financial subsidy providing assistance for high-yield seeds, eco-fertilizers, and modern drip irrigation equipment.",
                benefit_amount="₹15,000 / Season",
                eligibility="Registered landowners with minimum 1.0 acre of cultivable land holding documented in Revenue Registry.",
                required_data_source="Revenue Department (7/12 Land Record)",
                is_active=True
            )
            s2 = Service(
                id="SRV-KISAN-002",
                title="PM-KISAN Samman Nidhi",
                department="Department of Agriculture",
                category="Direct Income",
                description="Central government income support scheme providing ₹6,000 annually in three equal installments to farmer families.",
                benefit_amount="₹6,000 / Year",
                eligibility="Small and marginal farmer landholders across Maharashtra state.",
                required_data_source="Revenue Department Land Records",
                is_active=True
            )
            s3 = Service(
                id="SRV-MUT-003",
                title="Automated Land Mutation & Title Registry",
                department="Revenue & Land Administration",
                category="Land Services",
                description="Seamless cross-departmental notification and automated record update following land parcel transfer or succession.",
                benefit_amount="Instant Title Verification",
                eligibility="Property owners with valid Survey Parcel ID.",
                required_data_source="Revenue Department Cadastral Index",
                is_active=True
            )
            db.add_all([s1, s2, s3])
            db.commit()

        # Seed Initial Demo Application for Rahul C001
        if not db.query(Application).filter(Application.id == "APP-2026-001").first():
            demo_app = Application(
                id="APP-2026-001",
                citizen_id="C001",
                service_id="SRV-AGRI-001",
                status="CONSENT_PENDING",
                department_application_id="A001"
            )
            db.add(demo_app)
            db.commit()

            consent = ConsentRecord(
                id="CNS-APP-2026-001",
                application_id="APP-2026-001",
                citizen_id="C001",
                purpose="Revenue Department land information is required to verify your Agriculture Subsidy application.",
                data_source="Revenue Department",
                data_recipient="Department of Agriculture",
                status="PENDING"
            )
            db.add(consent)

            init_event = AuditEvent(
                application_id="APP-2026-001",
                event_type="APPLICATION_SUBMITTED",
                source="CitizenPortal",
                description="Citizen Rahul Patil submitted Agriculture Subsidy application. Land verification pending consent."
            )
            db.add(init_event)
            db.commit()

        logger.info("Database schema and seed records initialized successfully.")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed_database()
    yield


# Ensure database tables and seed data exist immediately
seed_database()


app = FastAPI(

    title="MahaSync Core API - The Digital Bridge",
    description="Cross-departmental interoperability platform connecting independent government systems (SIH 2026).",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for Next.js frontend and all local tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers (v1 and root aliases)
app.include_router(services_router, prefix="/api/v1")
app.include_router(applications_router, prefix="/api/v1")
app.include_router(assistant_router, prefix="/api/v1")

# Direct aliases as requested in backend specifications
app.include_router(services_router)
app.include_router(applications_router)


@app.get("/health")
def health_check():
    return {"status": "UP", "service": "MahaSync Core Gateway"}


@app.get("/api/v1/system-status")
async def system_status():
    """Checks real-time connectivity status across independent government systems."""
    rev_online = False
    agri_online = False

    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            r = await client.get(f"{REVENUE_API_URL}/health", follow_redirects=True)
            rev_online = r.status_code in [200, 404]
        except Exception:
            try:
                # check land endpoint
                r = await client.get(f"{REVENUE_API_URL}/revenue/land/C001")
                rev_online = r.status_code == 200
            except Exception:
                rev_online = False

        try:
            a = await client.get(f"{AGRICULTURE_API_URL}/health", follow_redirects=True)
            agri_online = a.status_code in [200, 404]
        except Exception:
            try:
                a = await client.get(f"{AGRICULTURE_API_URL}/agriculture/applications")
                agri_online = a.status_code == 200
            except Exception:
                agri_online = False

    return {
        "mahasync_core": {"status": "ONLINE", "port": BACKEND_PORT},
        "revenue_department": {"status": "ONLINE" if rev_online else "OFFLINE", "url": REVENUE_API_URL, "port": 8000},
        "agriculture_department": {"status": "ONLINE" if agri_online else "OFFLINE", "url": AGRICULTURE_API_URL, "port": 8001},
        "event_bus": {"status": "ONLINE", "type": "RabbitMQ (with async fallback)"}
    }


@app.post("/api/v1/reset-demo")
async def reset_demo_state(db: Session = Depends(get_db)):
    """Resets entire demo state across MahaSync, Revenue, and Agriculture for repeat testing."""
    # Reset local applications
    db.query(AuditEvent).delete()
    db.query(ConsentRecord).delete()
    db.query(Application).delete()
    db.commit()

    # Re-seed application APP-2026-001
    demo_app = Application(
        id="APP-2026-001",
        citizen_id="C001",
        service_id="SRV-AGRI-001",
        status="CONSENT_PENDING",
        department_application_id="A001"
    )
    db.add(demo_app)
    db.commit()

    consent = ConsentRecord(
        id="CNS-APP-2026-001",
        application_id="APP-2026-001",
        citizen_id="C001",
        purpose="Revenue Department land information is required to verify your Agriculture Subsidy application.",
        data_source="Revenue Department",
        data_recipient="Department of Agriculture",
        status="PENDING"
    )
    db.add(consent)

    init_event = AuditEvent(
        application_id="APP-2026-001",
        event_type="APPLICATION_SUBMITTED",
        source="CitizenPortal",
        description="Citizen Rahul Patil submitted Agriculture Subsidy application. Land verification pending consent."
    )
    db.add(init_event)
    db.commit()

    # Trigger resets on Revenue and Agriculture APIs
    async with httpx.AsyncClient(timeout=3.0) as client:
        try:
            await client.post(f"{REVENUE_API_URL}/revenue/reset")
        except Exception:
            pass
        try:
            await client.post(f"{AGRICULTURE_API_URL}/agriculture/reset")
        except Exception:
            pass

    return {"status": "success", "message": "Demo state reset to original PENDING state across all departments"}


# Mount embedded citizen frontend portal
try:
    from .portal_ui import get_portal_html
    @app.get("/", response_class=HTMLResponse)
    @app.get("/portal", response_class=HTMLResponse)
    def render_citizen_portal():
        return get_portal_html()
except Exception as e:
    logger.warning(f"Embedded portal UI not mounted yet: {e}")
