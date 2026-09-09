# Keycloak Identity & Access Management (IAM) - Member 5

## Purpose & Scope
MahaSync uses Keycloak for centralized Citizen Identity, Authentication, and Consent Authorization.

Instead of each department requiring separate logins and credentials, citizens authenticate once through MahaSync. Data access between departments is strictly gated by authenticated citizen consent, aligning with the principles of India's **Digital Personal Data Protection (DPDP) Act 2023**.

## Architecture & Flows
```text
[Citizen Browser]
       │
       ▼ (1. Login / OAuth2 Authorization Code Flow)
[Keycloak Identity Provider] (:8080)
       │
       ▼ (2. Issues Signed JWT Access & ID Tokens)
[MahaSync Frontend / Backend]
       │
       ▼ (3. Explicit Consent Challenge for Inter-Department Access)
[Consent Management Engine] (Records Signed Consent Artifact)
       │
       ▼ (4. Authorized Inter-Department Query)
[Revenue Dept / Agriculture Dept]
```

## Configured Realm & Clients
- **Realm Name**: `mahasync`
- **Clients**:
  - `mahasync-frontend`: Public client for Single Page Applications (Next.js/React).
  - `mahasync-backend`: Bearer-only client for REST API endpoints.
- **Roles**:
  - `citizen`: Can view services, submit applications, manage consents.
  - `officer`: Departmental verification and auditing privileges.
- **Pre-configured Demo Users**:
  - **Username**: `rahul` (Password: `rahul123`) -> Citizen ID: `C001`
  - **Username**: `amit` (Password: `amit123`) -> Citizen ID: `C002`
  - **Username**: `officer` (Password: `officer123`) -> Revenue Officer

## Running Keycloak Locally with Docker
```bash
cd keycloak
docker compose up -d
```
Keycloak Administration Console: `http://localhost:8080/admin` (User: `admin`, Password: `admin_password`).

## Local Demo Mode Fallback
For local laptop judging where Docker or Keycloak might not be running, `auth_middleware.py` automatically provides a mock authentication session pre-configured for Rahul (`C001`), ensuring that the SIH demonstration can run smoothly without dependencies.
