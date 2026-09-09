import sys
from pathlib import Path

# Add project root to sys.path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from tests.test_e2e_integration import (
    setup_module,
    test_revenue_api,
    test_agriculture_api_initial_state,
    test_adapters_bidirectional_mapping,
    test_agriculture_api_direct_verification,
    test_backend_services_endpoint,
    test_backend_consent_denial,
    test_primary_e2e_demo_flow,
    test_ai_assistant
)

def run_all():
    print("=" * 70)
    print("      RUNNING MAHASync END-TO-END INTEGRATION TEST SUITE      ")
    print("=" * 70)

    setup_module()
    tests = [
        ("1. Revenue Department API", test_revenue_api),
        ("2. Agriculture Department Initial State", test_agriculture_api_initial_state),
        ("3. Adapters Bidirectional Mapping", test_adapters_bidirectional_mapping),
        ("4. Agriculture API Direct Verification", test_agriculture_api_direct_verification),
        ("5. MahaSync Backend Services Catalog", test_backend_services_endpoint),
        ("6. MahaSync Consent Denial Safety", test_backend_consent_denial),
        ("7. PRIMARY DEMO E2E FLOW (Rahul C001 -> Verified)", test_primary_e2e_demo_flow),
        ("8. MahaMitra AI Government Assistant", test_ai_assistant),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("=" * 70)
    print(f"Test Summary: {passed} PASSED, {failed} FAILED out of {len(tests)} tests.")
    print("=" * 70)
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(run_all())
