"""
Comprehensive diagnostic tests for Issue #13: Error Code 11 with createPerson/updatePerson.

This test suite diagnoses the "No identifiers available" error (error code 11)
that occurs when creating or updating people despite providing valid data.

Test cases use real names from the provided test data.
"""

import os
import pytest
import time
from cloze_sdk import ClozeClient
from cloze_sdk.exceptions import ClozeAPIError


pytestmark = [pytest.mark.integration, pytest.mark.slow]


# Test data from the provided image
TEST_PEOPLE = [
    {
        "name": "Rhea Bhatia",
        "first": "Rhea",
        "last": "Bhatia",
        "email": "rheabhatia@rocketmail.com",
        "title": None,
    },
    {
        "name": "Stephanie Koogler, SHRM-SCP",
        "first": "Stephanie",
        "last": "Koogler",
        "email": "skoogler@deezee.com",
        "title": "Talent Acquisition Consultant",
    },
    {
        "name": "Kaushik Konlade",
        "first": "Kaushik",
        "last": "Konlade",
        "email": "kaushik.konlade@pattern.com",
        "title": "Director - Talent Acquisition - India",
    },
    {
        "name": "Nicole Kombrink, CPC, CDR",
        "first": "Nicole",
        "last": "Kombrink",
        "email": None,  # No email provided
        "title": "Manager, Talent Acquisition",
    },
    {
        "name": "Richard Kolikof",
        "first": "Richard",
        "last": "Kolikof",
        "email": "nkolikof@gmail.com",
        "title": "Sr. Talent Acquisition Consultant",
    },
    {
        "name": "Stephanie Knobbe",
        "first": "Stephanie",
        "last": "Knobbe",
        "email": "stephaniek@dowbuilt.com",
        "title": "Senior Talent Acquisition Lead",
    },
    {
        "name": "Ric Klinger (He, Him, His)",
        "first": "Ric",
        "last": "Klinger",
        "email": "ricklinger2@gmail.com",
        "title": "Global Talent Attraction, Assistant Director - US Global, Compliance Reporting, Corporate Tax Hub Lead",
    },
    {
        "name": "Elizabeth Klein",
        "first": "Elizabeth",
        "last": "Klein",
        "email": "focusvision2005@yahoo.com",
        "title": "Principal Talent Finder",
    },
]


@pytest.fixture
def api_key():
    """Get API key from file or environment variable."""
    # Try to read from file first
    key_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "tmp", "api_key.txt"
    )
    if os.path.exists(key_file):
        with open(key_file, "r") as f:
            key = f.read().strip()
            if key:
                return key
    
    # Fall back to environment variable
    key = os.getenv("CLOZE_API_KEY")
    if not key:
        pytest.skip("API key not found in tmp/api_key.txt or CLOZE_API_KEY environment variable")
    return key


@pytest.fixture
def client(api_key):
    """Create a real ClozeClient for diagnostic tests."""
    return ClozeClient(api_key=api_key)


@pytest.fixture
def unique_suffix():
    """Generate a unique suffix for test data to avoid conflicts."""
    return int(time.time() * 1000) % 1000000


class TestIssue13Diagnostic:
    """Diagnostic tests for Issue #13: Error Code 11."""
    
    def test_format_1_direct_fields(self, client, unique_suffix):
        """
        Test Format 1: Direct fields (as SDK currently sends).
        Format: {"email": "...", "first": "...", "last": "..."}
        """
        person_data = TEST_PEOPLE[0].copy()
        if person_data["email"]:
            # Add unique suffix to email to avoid conflicts
            email_parts = person_data["email"].split("@")
            person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        
        print(f"\n[TEST] Format 1 - Direct fields")
        print(f"[DATA] {person_data}")
        
        try:
            result = client.people.create(person_data)
            print(f"[RESULT] Success: {result}")
            assert result.get("errorcode") == 0, f"Expected errorcode 0, got {result.get('errorcode')}: {result}"
            
            # Check for direct ID
            direct_id = result.get("direct") or result.get("person", {}).get("direct")
            print(f"[DIRECT_ID] {direct_id}")
            
        except ClozeAPIError as e:
            print(f"[ERROR] {e}")
            print(f"[ERRORCODE] {e.errorcode if hasattr(e, 'errorcode') else 'unknown'}")
            print(f"[MESSAGE] {e}")
            raise
    
    def test_format_2_wrapped_in_person(self, client, unique_suffix):
        """
        Test Format 2: Wrapped in "person" key (as described in issue).
        Format: {"person": {"email": "...", "first": "...", "last": "..."}}
        
        NOTE: This format might not work with current SDK, but we test it
        to see if the API expects this format.
        """
        person_data = TEST_PEOPLE[1].copy()
        if person_data["email"]:
            email_parts = person_data["email"].split("@")
            person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        
        # Try wrapping in "person" key by making direct request
        print(f"\n[TEST] Format 2 - Wrapped in 'person' key")
        print(f"[DATA] {person_data}")
        
        try:
            # Make direct request with wrapped format
            response = client.session.post(
                f"{client.base_url}/v1/people/create",
                json={"person": person_data},
                headers=client.session.headers
            )
            result = response.json()
            print(f"[RESULT] Status: {response.status_code}, Body: {result}")
            
            errorcode = result.get("errorcode", 0)
            if errorcode != 0:
                print(f"[ERROR] Error code {errorcode}: {result.get('message', 'No message')}")
            else:
                print(f"[SUCCESS] Error code 0")
                direct_id = result.get("direct") or result.get("person", {}).get("direct")
                print(f"[DIRECT_ID] {direct_id}")
                
        except Exception as e:
            print(f"[EXCEPTION] {e}")
            pytest.fail(f"Format 2 test failed: {e}")
    
    def test_format_3_with_name_field(self, client, unique_suffix):
        """
        Test Format 3: Including "name" field in addition to first/last.
        Format: {"name": "...", "first": "...", "last": "...", "email": "..."}
        """
        person_data = TEST_PEOPLE[2].copy()
        if person_data["email"]:
            email_parts = person_data["email"].split("@")
            person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        
        print(f"\n[TEST] Format 3 - With 'name' field")
        print(f"[DATA] {person_data}")
        
        try:
            result = client.people.create(person_data)
            print(f"[RESULT] {result}")
            assert result.get("errorcode") == 0, f"Expected errorcode 0, got {result.get('errorcode')}: {result}"
            
        except ClozeAPIError as e:
            print(f"[ERROR] {e}")
            print(f"[ERRORCODE] {e.errorcode if hasattr(e, 'errorcode') else 'unknown'}")
            raise
    
    def test_format_4_with_segment_stage(self, client, unique_suffix):
        """
        Test Format 4: With segment and stage (as in issue description).
        Format: {"first": "...", "last": "...", "email": "...", "segment": "lead", "stage": "lead"}
        """
        person_data = TEST_PEOPLE[3].copy()
        # Skip if no email
        if not person_data["email"]:
            pytest.skip("No email provided for this person")
        
        email_parts = person_data["email"].split("@")
        person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        person_data["segment"] = "lead"
        person_data["stage"] = "lead"
        
        print(f"\n[TEST] Format 4 - With segment and stage")
        print(f"[DATA] {person_data}")
        
        try:
            result = client.people.create(person_data)
            print(f"[RESULT] {result}")
            assert result.get("errorcode") == 0, f"Expected errorcode 0, got {result.get('errorcode')}: {result}"
            
        except ClozeAPIError as e:
            print(f"[ERROR] {e}")
            print(f"[ERRORCODE] {e.errorcode if hasattr(e, 'errorcode') else 'unknown'}")
            if hasattr(e, 'errorcode') and e.errorcode == 11:
                print(f"[DIAGNOSIS] Got error code 11 - 'No identifiers available'")
                print(f"[DIAGNOSIS] Data sent: first={person_data.get('first')}, last={person_data.get('last')}, email={person_data.get('email')}")
            raise
    
    def test_format_5_with_phone(self, client, unique_suffix):
        """
        Test Format 5: With phone number in E.164 format.
        Format: {"first": "...", "last": "...", "email": "...", "phone": "+1234567890"}
        """
        person_data = TEST_PEOPLE[4].copy()
        if person_data["email"]:
            email_parts = person_data["email"].split("@")
            person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        person_data["phone"] = "+1234567890"
        
        print(f"\n[TEST] Format 5 - With phone number")
        print(f"[DATA] {person_data}")
        
        try:
            result = client.people.create(person_data)
            print(f"[RESULT] {result}")
            assert result.get("errorcode") == 0, f"Expected errorcode 0, got {result.get('errorcode')}: {result}"
            
        except ClozeAPIError as e:
            print(f"[ERROR] {e}")
            print(f"[ERRORCODE] {e.errorcode if hasattr(e, 'errorcode') else 'unknown'}")
            raise
    
    def test_format_6_email_only(self, client, unique_suffix):
        """
        Test Format 6: Email only (API docs say this should work).
        Format: {"email": "..."}
        """
        person_data = TEST_PEOPLE[5].copy()
        if not person_data["email"]:
            pytest.skip("No email provided for this person")
        
        email_parts = person_data["email"].split("@")
        person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        # Remove first and last to test email-only
        person_data.pop("first", None)
        person_data.pop("last", None)
        person_data.pop("name", None)
        person_data.pop("title", None)
        
        print(f"\n[TEST] Format 6 - Email only")
        print(f"[DATA] {person_data}")
        
        try:
            result = client.people.create(person_data)
            print(f"[RESULT] {result}")
            assert result.get("errorcode") == 0, f"Expected errorcode 0, got {result.get('errorcode')}: {result}"
            
        except ClozeAPIError as e:
            print(f"[ERROR] {e}")
            print(f"[ERRORCODE] {e.errorcode if hasattr(e, 'errorcode') else 'unknown'}")
            raise
    
    def test_format_7_first_last_only(self, client, unique_suffix):
        """
        Test Format 7: First and last name only (no email).
        Format: {"first": "...", "last": "..."}
        """
        person_data = TEST_PEOPLE[6].copy()
        # Remove email to test name-only
        person_data.pop("email", None)
        person_data.pop("name", None)
        person_data.pop("title", None)
        
        print(f"\n[TEST] Format 7 - First and last name only (no email)")
        print(f"[DATA] {person_data}")
        
        try:
            result = client.people.create(person_data)
            print(f"[RESULT] {result}")
            # This might fail, but we want to see the error
            if result.get("errorcode") != 0:
                print(f"[EXPECTED] Error code {result.get('errorcode')}: {result.get('message', 'No message')}")
            
        except ClozeAPIError as e:
            print(f"[ERROR] {e}")
            print(f"[ERRORCODE] {e.errorcode if hasattr(e, 'errorcode') else 'unknown'}")
            # Don't fail - this might be expected behavior
    
    def test_format_8_with_title(self, client, unique_suffix):
        """
        Test Format 8: With title/job title field.
        Format: {"first": "...", "last": "...", "email": "...", "title": "..."}
        """
        person_data = TEST_PEOPLE[7].copy()
        if person_data["email"]:
            email_parts = person_data["email"].split("@")
            person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        # Keep title if present
        
        print(f"\n[TEST] Format 8 - With title field")
        print(f"[DATA] {person_data}")
        
        try:
            result = client.people.create(person_data)
            print(f"[RESULT] {result}")
            assert result.get("errorcode") == 0, f"Expected errorcode 0, got {result.get('errorcode')}: {result}"
            
        except ClozeAPIError as e:
            print(f"[ERROR] {e}")
            print(f"[ERRORCODE] {e.errorcode if hasattr(e, 'errorcode') else 'unknown'}")
            raise
    
    def test_error_11_recovery_with_update(self, client, unique_suffix):
        """
        Test the recovery strategy: if createPerson fails with error 11, try updatePerson.
        This tests the exact scenario described in the issue.
        """
        person_data = TEST_PEOPLE[0].copy()
        if person_data["email"]:
            email_parts = person_data["email"].split("@")
            person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        person_data["segment"] = "lead"
        person_data["stage"] = "lead"
        
        print(f"\n[TEST] Error 11 Recovery - createPerson then updatePerson")
        print(f"[DATA] {person_data}")
        
        create_success = False
        update_success = False
        direct_id = None
        
        # Try createPerson first
        try:
            result = client.people.create(person_data)
            errorcode = result.get("errorcode", 0)
            print(f"[CREATE] Result: errorcode={errorcode}, {result}")
            
            if errorcode == 0:
                create_success = True
                direct_id = result.get("direct") or result.get("person", {}).get("direct")
                print(f"[CREATE] Success! Direct ID: {direct_id}")
            elif errorcode == 11:
                print(f"[CREATE] Got error 11, trying updatePerson...")
                # Try updatePerson as recovery
                try:
                    update_result = client.people.update(person_data)
                    update_errorcode = update_result.get("errorcode", 0)
                    print(f"[UPDATE] Result: errorcode={update_errorcode}, {update_result}")
                    
                    if update_errorcode == 0:
                        update_success = True
                        direct_id = update_result.get("direct") or update_result.get("person", {}).get("direct")
                        print(f"[UPDATE] Success! Direct ID: {direct_id}")
                        
                        # If no direct ID in response, try to get it
                        if not direct_id and person_data.get("email"):
                            print(f"[UPDATE] No direct ID in response, trying get()...")
                            get_result = client.people.get(person_data["email"])
                            if get_result.get("errorcode") == 0:
                                person = get_result.get("person", {})
                                direct_id = person.get("direct")
                                print(f"[GET] Retrieved direct ID: {direct_id}")
                    else:
                        print(f"[UPDATE] Failed with errorcode {update_errorcode}")
                except ClozeAPIError as update_e:
                    print(f"[UPDATE] Exception: {update_e}")
            else:
                print(f"[CREATE] Unexpected errorcode {errorcode}")
                
        except ClozeAPIError as e:
            errorcode = e.errorcode if hasattr(e, 'errorcode') else None
            print(f"[CREATE] Exception: {e}, errorcode={errorcode}")
            
            if errorcode == 11:
                # Try updatePerson as recovery
                try:
                    update_result = client.people.update(person_data)
                    update_errorcode = update_result.get("errorcode", 0)
                    print(f"[UPDATE] Result: errorcode={update_errorcode}, {update_result}")
                    
                    if update_errorcode == 0:
                        update_success = True
                        direct_id = update_result.get("direct") or update_result.get("person", {}).get("direct")
                        print(f"[UPDATE] Success! Direct ID: {direct_id}")
                except ClozeAPIError as update_e:
                    print(f"[UPDATE] Exception: {update_e}")
        
        # Assert that at least one succeeded
        assert create_success or update_success, "Both createPerson and updatePerson failed"
        print(f"[SUMMARY] create_success={create_success}, update_success={update_success}, direct_id={direct_id}")
    
    def test_all_people_from_image(self, client, unique_suffix):
        """
        Test creating all people from the provided image data.
        This comprehensive test will help identify patterns in failures.
        """
        results = []
        
        for idx, person_template in enumerate(TEST_PEOPLE):
            person_data = person_template.copy()
            
            # Skip if no email and no way to identify
            if not person_data.get("email") and not (person_data.get("first") and person_data.get("last")):
                print(f"\n[SKIP] Person {idx+1}: {person_data.get('name')} - No email or name")
                results.append({"index": idx, "name": person_data.get("name"), "status": "skipped", "reason": "no identifiers"})
                continue
            
            # Make email unique if present
            if person_data.get("email"):
                email_parts = person_data["email"].split("@")
                person_data["email"] = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
            
            print(f"\n[TEST] Person {idx+1}: {person_data.get('name')}")
            print(f"[DATA] {person_data}")
            
            try:
                result = client.people.create(person_data)
                errorcode = result.get("errorcode", 0)
                
                if errorcode == 0:
                    direct_id = result.get("direct") or result.get("person", {}).get("direct")
                    print(f"[SUCCESS] Errorcode 0, Direct ID: {direct_id}")
                    results.append({
                        "index": idx,
                        "name": person_data.get("name"),
                        "status": "success",
                        "errorcode": 0,
                        "direct_id": direct_id
                    })
                else:
                    message = result.get("message", "No message")
                    print(f"[FAILED] Errorcode {errorcode}: {message}")
                    results.append({
                        "index": idx,
                        "name": person_data.get("name"),
                        "status": "failed",
                        "errorcode": errorcode,
                        "message": message
                    })
                    
            except ClozeAPIError as e:
                errorcode = e.errorcode if hasattr(e, 'errorcode') else None
                print(f"[EXCEPTION] {e}, errorcode={errorcode}")
                results.append({
                    "index": idx,
                    "name": person_data.get("name"),
                    "status": "exception",
                    "errorcode": errorcode,
                    "message": str(e)
                })
        
        # Print summary
        print(f"\n[SUMMARY] Test Results:")
        print(f"  Total: {len(results)}")
        print(f"  Success: {sum(1 for r in results if r.get('status') == 'success')}")
        print(f"  Failed: {sum(1 for r in results if r.get('status') == 'failed')}")
        print(f"  Exceptions: {sum(1 for r in results if r.get('status') == 'exception')}")
        print(f"  Skipped: {sum(1 for r in results if r.get('status') == 'skipped')}")
        
        # Check for error code 11 specifically
        error_11_count = sum(1 for r in results if r.get('errorcode') == 11)
        if error_11_count > 0:
            print(f"\n[WARNING] {error_11_count} test(s) returned error code 11")
            for r in results:
                if r.get('errorcode') == 11:
                    print(f"  - {r.get('name')}: {r.get('message')}")
        
        # Store results for analysis
        self.test_results = results
    
    def test_update_with_email_only(self, client, unique_suffix):
        """
        Test if updatePerson can find a person by email alone (without direct ID).
        This addresses question 2 from the issue.
        """
        person_data = TEST_PEOPLE[1].copy()
        if not person_data["email"]:
            pytest.skip("No email provided for this person")
        
        email_parts = person_data["email"].split("@")
        unique_email = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        person_data["email"] = unique_email
        
        print(f"\n[TEST] Update with email only (no direct ID)")
        print(f"[DATA] {person_data}")
        
        # First, try to create the person
        try:
            create_result = client.people.create(person_data)
            if create_result.get("errorcode") == 0:
                print(f"[CREATE] Success: {create_result}")
                direct_id_from_create = create_result.get("direct") or create_result.get("person", {}).get("direct")
                print(f"[CREATE] Direct ID: {direct_id_from_create}")
        except ClozeAPIError as e:
            print(f"[CREATE] Failed: {e}")
            # Continue anyway - person might already exist
        
        # Now try to update using only email
        try:
            update_data = {
                "email": unique_email,
                "first": person_data["first"],
                "last": person_data["last"],
                "segment": "lead"
            }
            update_result = client.people.update(update_data)
            errorcode = update_result.get("errorcode", 0)
            print(f"[UPDATE] Result: errorcode={errorcode}, {update_result}")
            
            if errorcode == 0:
                direct_id = update_result.get("direct") or update_result.get("person", {}).get("direct")
                print(f"[UPDATE] Success! Direct ID: {direct_id}")
                
                # If no direct ID, try to get it
                if not direct_id:
                    print(f"[UPDATE] No direct ID in response, trying get()...")
                    get_result = client.people.get(unique_email)
                    if get_result.get("errorcode") == 0:
                        person = get_result.get("person", {})
                        direct_id = person.get("direct")
                        print(f"[GET] Retrieved direct ID: {direct_id}")
                        assert direct_id, "Could not retrieve direct ID after successful update"
            else:
                print(f"[UPDATE] Failed with errorcode {errorcode}: {update_result.get('message', 'No message')}")
                
        except ClozeAPIError as e:
            print(f"[UPDATE] Exception: {e}")
            raise
    
    def test_get_direct_id_after_update(self, client, unique_suffix):
        """
        Test retrieving direct ID when updatePerson succeeds but doesn't return it.
        This addresses question 3 from the issue.
        """
        person_data = TEST_PEOPLE[2].copy()
        if not person_data["email"]:
            pytest.skip("No email provided for this person")
        
        email_parts = person_data["email"].split("@")
        unique_email = f"{email_parts[0]}+test{unique_suffix}@{email_parts[1]}"
        person_data["email"] = unique_email
        
        print(f"\n[TEST] Get direct ID after updatePerson")
        print(f"[DATA] {person_data}")
        
        # Try to create first
        try:
            create_result = client.people.create(person_data)
            print(f"[CREATE] {create_result}")
        except ClozeAPIError as e:
            print(f"[CREATE] {e}")
        
        # Update the person
        try:
            update_result = client.people.update(person_data)
            errorcode = update_result.get("errorcode", 0)
            print(f"[UPDATE] errorcode={errorcode}, {update_result}")
            
            if errorcode == 0:
                direct_id = update_result.get("direct") or update_result.get("person", {}).get("direct")
                print(f"[UPDATE] Direct ID in response: {direct_id}")
                
                # If no direct ID, try to get it
                if not direct_id:
                    print(f"[GET] No direct ID in update response, trying get()...")
                    get_result = client.people.get(unique_email)
                    print(f"[GET] Result: {get_result}")
                    
                    if get_result.get("errorcode") == 0:
                        person = get_result.get("person", {})
                        direct_id = person.get("direct")
                        print(f"[GET] Retrieved direct ID: {direct_id}")
                        
                        if direct_id:
                            print(f"[SUCCESS] Successfully retrieved direct ID: {direct_id}")
                        else:
                            print(f"[WARNING] get() succeeded but no direct ID in person object")
                            print(f"[WARNING] Person object: {person}")
                    else:
                        print(f"[ERROR] get() failed with errorcode {get_result.get('errorcode')}")
                else:
                    print(f"[SUCCESS] Direct ID found in update response: {direct_id}")
                    
        except ClozeAPIError as e:
            print(f"[UPDATE] Exception: {e}")
            raise

