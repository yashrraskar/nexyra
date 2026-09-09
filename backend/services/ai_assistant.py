import re
from typing import Dict, Any, List


def get_ai_assistant_response(query: str, citizen_name: str = "Rahul", citizen_id: str = "C001") -> Dict[str, Any]:
    """
    MahaMitra AI Government Assistant:
    Provides context-aware guidance for schemes, eligibility, required documents, and consent.
    Reliable rule-based intelligence ensuring zero-downtime offline presentation.
    """
    q = query.lower()

    if any(k in q for k in ["consent", "permission", "dpdp", "privacy", "why consent"]):
        return {
            "reply": (
                f"Hello {citizen_name}! In accordance with the Digital Personal Data Protection (DPDP) Act, "
                "MahaSync never shares your data without explicit authorization. When applying for the Agriculture Subsidy, "
                "MahaSync requests your consent to pull your verified 7/12 land record from the Revenue Department so you don't "
                "have to physically collect and upload paper certificates."
            ),
            "suggested_actions": ["Review Consent Policy", "View Application Status"],
            "relevant_scheme": "Agriculture Subsidy Scheme"
        }

    if any(k in q for k in ["land", "7/12", "revenue", "property", "record"]):
        return {
            "reply": (
                f"Under the MahaSync integration, your land records are verified directly from the State Revenue Registry. "
                f"For citizen {citizen_id}, your land record (Parcel MH-LAND-101, 2.5 Acres) is pre-verified in Revenue Department. "
                "Once you click 'Allow' in MahaSync, this is transmitted digitally to the Agriculture Department."
            ),
            "suggested_actions": ["Check Revenue Records", "Apply for Subsidy"],
            "relevant_scheme": "Land Record Verification"
        }

    if any(k in q for k in ["status", "track", "application", "where is", "progress"]):
        return {
            "reply": (
                f"You can track your active applications in the 'Applications' tab. Once consent is granted, "
                "the entire inter-departmental verification takes less than 3 seconds across Revenue and Agriculture systems."
            ),
            "suggested_actions": ["Go to Application Tracking", "View Audit Trail"],
            "relevant_scheme": "Agriculture Subsidy Scheme"
        }

    if any(k in q for k in ["scheme", "subsidy", "service", "available", "apply"]):
        return {
            "reply": (
                f"Welcome {citizen_name}! Available schemes under MahaSync include:\n"
                "1. **Agriculture Subsidy Scheme (DBT)** - Financial assistance for fertilizers and seeds.\n"
                "2. **PM-KISAN Samman Nidhi** - Direct income support of ₹6,000/year.\n"
                "3. **Land Mutation & Title Transfer** - Automated record updates across revenue sub-divisions."
            ),
            "suggested_actions": ["Apply for Agriculture Subsidy", "Explore All Schemes"],
            "relevant_scheme": "Agriculture Subsidy Scheme"
        }

    # Default fallback response
    return {
        "reply": (
            f"Namaskar {citizen_name}! I am MahaMitra, your AI Digital Governance Guide. "
            "I can assist you with scheme eligibility, document verification requirements, tracking applications, "
            "or explaining how your data is safely exchanged between government departments with your consent."
        ),
        "suggested_actions": ["What is Agriculture Subsidy?", "Why do you need my consent?", "Track my Application"],
        "relevant_scheme": "MahaSync Unified Portal"
    }
