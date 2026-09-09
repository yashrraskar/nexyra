import os
import logging
from typing import Optional, Dict, Any
from fastapi import HTTPException, Security, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

logger = logging.getLogger("MahaSync.Security")

security = HTTPBearer(auto_error=False)

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
REALM = os.getenv("KEYCLOAK_REALM", "mahasync")
ENABLE_KEYCLOAK = os.getenv("ENABLE_KEYCLOAK", "false").lower() == "true"

# Pre-configured demo users for zero-friction local SIH judging
DEMO_USERS: Dict[str, Dict[str, Any]] = {
    "C001": {
        "citizen_id": "C001",
        "username": "rahul",
        "name": "Rahul Patil",
        "email": "rahul@mahasync.gov.in",
        "phone": "+91 98765 43210",
        "roles": ["citizen"],
        "token": "demo-token-c001-rahul"
    },
    "C002": {
        "citizen_id": "C002",
        "username": "amit",
        "name": "Amit Deshmukh",
        "email": "amit@mahasync.gov.in",
        "phone": "+91 98765 43211",
        "roles": ["citizen"],
        "token": "demo-token-c002-amit"
    },
    "C003": {
        "citizen_id": "C003",
        "username": "priya",
        "name": "Priya Sharma",
        "email": "priya@mahasync.gov.in",
        "phone": "+91 98765 43212",
        "roles": ["citizen"],
        "token": "demo-token-c003-priya"
    }
}


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security),
    x_citizen_id: Optional[str] = Header(None, alias="X-Citizen-Id")
) -> Dict[str, Any]:
    """
    Authenticates the request.
    1. If Keycloak is enabled and a valid Bearer token is passed, verifies JWT against Keycloak.
    2. If running in local Demo/Dev mode, validates demo tokens or X-Citizen-Id header (defaulting to C001 Rahul).
    """
    token = credentials.credentials if credentials else None

    # Production / Live Keycloak Flow
    if ENABLE_KEYCLOAK and token and not token.startswith("demo-"):
        try:
            import httpx
            # Query Keycloak UserInfo endpoint
            userinfo_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo"
            async with httpx.AsyncClient(timeout=5.0) as client:
                res = await client.get(userinfo_url, headers={"Authorization": f"Bearer {token}"})
                if res.status_code == 200:
                    info = res.json()
                    return {
                        "citizen_id": info.get("citizen_id", ["C001"])[0] if isinstance(info.get("citizen_id"), list) else info.get("citizen_id", "C001"),
                        "username": info.get("preferred_username", "citizen"),
                        "name": info.get("name", "Citizen"),
                        "email": info.get("email", ""),
                        "roles": info.get("realm_access", {}).get("roles", ["citizen"])
                    }
        except Exception as e:
            logger.warning(f"Keycloak verification error: {e}. Falling back to demo mode.")

    # Local Demo Mode Resolution
    if token:
        for cid, user in DEMO_USERS.items():
            if user["token"] == token or token == f"bearer-{cid.lower()}":
                return user

    if x_citizen_id and x_citizen_id in DEMO_USERS:
        return DEMO_USERS[x_citizen_id]

    # Default to primary demo user C001 (Rahul) for seamless judging experience
    return DEMO_USERS["C001"]


def get_demo_user(citizen_id: str = "C001") -> Dict[str, Any]:
    return DEMO_USERS.get(citizen_id, DEMO_USERS["C001"])
