# MahaSync Citizen Frontend (Member 1)

## Overview
The MahaSync Citizen Portal is a modern, responsive web application built with **Next.js 14, React 18, and Tailwind CSS**. It provides citizens with a unified interface to discover government schemes, review explicit data-sharing consent under the DPDP Act 2023, and track cross-departmental verification in real-time.

## Key Routes
- `/login`: Citizen authentication with Keycloak SSO and pre-configured demo user Rahul Patil (`C001`).
- `/dashboard`: Welcome metrics, active applications, quick consent reviews.
- `/services`: Discoverable catalog of government schemes.
- `/services/agriculture-subsidy`: Detailed DBT subsidy scheme specifications.
- `/apply`: One-click application submission with pre-filled citizen identity.
- `/consent`: Transparent consent authorization modal/page with explicit Allow/Deny actions.
- `/applications`: Unified listing of submitted applications.
- `/applications/[id]`: Interactive 5-stage verification stepper with full immutable audit trail.

## Dual Execution Modes

### 1. Embedded Zero-Dependency Mode (Recommended for SIH Judging)
The citizen portal is pre-compiled and served directly by the MahaSync backend at:
`http://localhost:8082` (or port 3000 via `run_demo.py`).
This allows the entire system to run without requiring Node.js or `npm install` on the presenter's laptop.

### 2. Standalone Next.js Development Mode
To run the frontend in standard Next.js development mode:
```bash
cd frontend
npm install
npm run dev
```
The development server will launch at `http://localhost:3000`.
