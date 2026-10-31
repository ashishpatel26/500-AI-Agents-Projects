"""Comprehensive unit and security tests for PII Sanitization Agent."""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure agent directory is in path whether run from repo root or agent dir
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from agent import (
    ENDPOINT,
    _is_luhn_valid,
    _run_self_checks,
    _sanitize_with_counts,
    sanitize,
    sanitize_locally,
    sanitize_text,
)


class TestLocalPIIDetectionAndSanitization(unittest.TestCase):
    """Test local detection and masking for all supported PII categories."""

    def test_email_detection_and_masking(self):
        """Test single and multiple email detection and replacement."""
        text = "Contact alice@example.com or bob.smith+tag@work.co.uk for details."
        sanitized = sanitize_text(text)
        self.assertNotIn("alice@example.com", sanitized)
        self.assertNotIn("bob.smith+tag@work.co.uk", sanitized)
        self.assertEqual(sanitized, "Contact [EMAIL] or [EMAIL] for details.")

    def test_phone_number_detection_and_masking(self):
        """Test phone numbers in various formats including unhyphenated 10-digit format."""
        # Unhyphenated 10-digit number from Issue #185 prompt
        prompt_example = "My email is akif@example.com and my phone number is 9876543210."
        sanitized = sanitize_text(prompt_example)
        self.assertEqual(sanitized, "My email is [EMAIL] and my phone number is [PHONE].")

        # International, parenthesized, and dashed formats
        intl_text = "Call +1 (555) 123-4567 or +44 20 7946 0958 or 555-123-4567."
        sanitized_intl = sanitize_text(intl_text)
        self.assertNotIn("+1 (555) 123-4567", sanitized_intl)
        self.assertNotIn("+44 20 7946 0958", sanitized_intl)
        self.assertNotIn("555-123-4567", sanitized_intl)
        self.assertIn("[PHONE]", sanitized_intl)

    def test_ip_address_detection_and_validation(self):
        """Test valid IPv4 and IPv6 detection and replacement."""
        text = "Server IPv4 is 192.0.2.42 and IPv6 is 2001:db8::1."
        sanitized = sanitize_text(text)
        self.assertEqual(sanitized, "Server IPv4 is [IP_ADDRESS] and IPv6 is [IP_ADDRESS].")

        # Invalid IP addresses should not be masked
        invalid_ip_text = "Versions are 1.2.3 and 999.999.999.999."
        self.assertEqual(sanitize_text(invalid_ip_text), invalid_ip_text)

    def test_credit_card_detection_and_luhn_validation(self):
        """Test credit card masking and verify Luhn checksum validation."""
        valid_card = "Card number 4111-1111-1111-1111 used for payment."
        sanitized = sanitize_text(valid_card)
        self.assertNotIn("4111-1111-1111-1111", sanitized)
        self.assertEqual(sanitized, "Card number [CREDIT_CARD] used for payment.")

        # Test Luhn helper directly
        self.assertTrue(_is_luhn_valid("4111111111111111"))
        self.assertFalse(_is_luhn_valid("4111111111111112"))

    def test_ssn_detection_and_masking(self):
        """Test US Social Security Number detection."""
        text = "Social Security number is 123-45-6789."
        sanitized = sanitize_text(text)
        self.assertNotIn("123-45-6789", sanitized)
        self.assertEqual(sanitized, "Social Security number is [SSN].")

    def test_government_and_tax_ids(self):
        """Test detection of national/tax IDs such as Mexican CURP and RFC."""
        text = "RFC is PEMJ880126MNEZSN01."
        sanitized = sanitize_text(text)
        self.assertNotIn("PEMJ880126MNEZSN01", sanitized)
        self.assertEqual(sanitized, "RFC is [GOV_ID].")

    def test_api_keys_and_secrets(self):
        """Test detection of API keys like OpenAI and GitHub tokens."""
        text = "Secret is sk-abc123fakekeynotreal0000000000."
        sanitized = sanitize_text(text)
        self.assertNotIn("sk-abc123fakekeynotreal0000000000", sanitized)
        self.assertEqual(sanitized, "Secret is [API_KEY].")

    def test_bank_account_masking(self):
        """Test bank account numbers and IBAN redaction."""
        text = "Transfer to Account 0123456789."
        sanitized = sanitize_text(text)
        self.assertNotIn("0123456789", sanitized)
        self.assertEqual(sanitized, "Transfer to Account [BANK_ACCOUNT].")

    def test_multiple_pii_values_in_one_input(self):
        """Test sanitizing multiple distinct PII types in a single passage."""
        text = (
            "User: Juan Perez. Email: juan.perez@example.com. Phone: +1-555-123-4567. "
            "Card: 4111-1111-1111-1111. SSN: 123-45-6789. IP: 192.0.2.42."
        )
        result = sanitize(text)
        sanitized = result["data"]["sanitized_content"]
        self.assertNotIn("juan.perez@example.com", sanitized)
        self.assertNotIn("+1-555-123-4567", sanitized)
        self.assertNotIn("4111-1111-1111-1111", sanitized)
        self.assertNotIn("123-45-6789", sanitized)
        self.assertNotIn("192.0.2.42", sanitized)
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["data"]["risk_category"], "PRIVATE")

        # Verify entity counts
        types = {e["type"] for e in result["data"]["entities"]}
        self.assertTrue({"email", "phone", "credit_card", "ssn", "ip_address"}.issubset(types))

    def test_text_containing_no_pii(self):
        """Ensure ordinary text is not modified."""
        text = "The quick brown fox jumps over the lazy dog in 2026."
        result = sanitize(text)
        self.assertEqual(result["data"]["sanitized_content"], text)
        self.assertEqual(result["data"]["risk_category"], "UNKNOWN")
        self.assertEqual(result["data"]["entities"], [])

    def test_empty_and_whitespace_inputs(self):
        """Test handling of empty string and whitespace."""
        empty_res = sanitize("")
        self.assertEqual(empty_res["data"]["sanitized_content"], "")
        self.assertEqual(empty_res["data"]["entities"], [])

        ws_res = sanitize("   \n\t   ")
        self.assertEqual(ws_res["data"]["sanitized_content"], "   \n\t   ")
        self.assertEqual(ws_res["data"]["entities"], [])

    def test_invalid_data_types(self):
        """Test that non-string inputs raise TypeError safely without data leakage."""
        for invalid_val in [None, 12345, ["email@test.com"], {"text": "hello"}]:
            with self.subTest(val=invalid_val):
                with self.assertRaises(TypeError):
                    sanitize(invalid_val)

    def test_already_sanitized_placeholders(self):
        """Ensure literal placeholders are not mistakenly counted as detected PII."""
        text = "The literal [EMAIL] and [PHONE] are not PII."
        result = sanitize(text)
        self.assertEqual(result["data"]["sanitized_content"], text)
        self.assertEqual(result["data"]["entities"], [])
        self.assertEqual(result["data"]["risk_category"], "UNKNOWN")


class TestSecureThirdPartyAPIIntegration(unittest.TestCase):
    """Test third-party API integration security, payload construction, and fail-closed handling."""

    @patch("agent.requests.post")
    def test_raw_pii_never_reaches_external_api(self, mock_post):
        """CRITICAL SECURITY TEST: Ensure raw sensitive data is NEVER sent in the HTTP payload."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "data": {"sanitized_content": "Verified [EMAIL] and [PHONE]"},
        }
        mock_post.return_value = mock_response

        raw_email = "victim.confidential@secretcorp.com"
        raw_phone = "9876543210"
        raw_card = "4111-1111-1111-1111"
        raw_ssn = "123-45-6789"
        raw_input = (
            f"My private email is {raw_email}, phone is {raw_phone}, "
            f"card is {raw_card}, and SSN is {raw_ssn}."
        )

        # Trigger sanitization with external API dispatch enabled
        result = sanitize(raw_input, call_api=True)

        # Verify requests.post was called
        mock_post.assert_called_once()
        call_kwargs = mock_post.call_args.kwargs
        sent_payload = call_kwargs["json"]

        # Inspect the exact outgoing payload content
        payload_text = sent_payload["text"]

        # ASSERTION 1: Raw sensitive data must NOT appear anywhere in the outgoing payload
        self.assertNotIn(raw_email, payload_text)
        self.assertNotIn(raw_phone, payload_text)
        self.assertNotIn(raw_card, payload_text)
        self.assertNotIn(raw_ssn, payload_text)

        # ASSERTION 2: Only sanitized placeholders should be present
        self.assertIn("[EMAIL]", payload_text)
        self.assertIn("[PHONE]", payload_text)
        self.assertIn("[CREDIT_CARD]", payload_text)
        self.assertIn("[SSN]", payload_text)

        # Check request headers and endpoint
        self.assertEqual(mock_post.call_args[0][0], ENDPOINT)
        self.assertEqual(sent_payload["tx_hash"], "TRIAL")

    @patch("agent.requests.post")
    def test_api_timeout_fail_closed_handling(self, mock_post):
        """Test that API timeouts fall back safely to local sanitization without crashing or leaking data."""
        import requests
        mock_post.side_effect = requests.Timeout("Connection timed out after 30s")

        raw_input = "Contact sensitive@example.com or 9876543210."
        result = sanitize(raw_input, call_api=True)

        # Must retain local sanitization
        self.assertEqual(result["status"], "error")
        sanitized = result["data"]["sanitized_content"]
        self.assertNotIn("sensitive@example.com", sanitized)
        self.assertNotIn("9876543210", sanitized)
        self.assertIn("[EMAIL]", sanitized)
        self.assertIn("[PHONE]", sanitized)
        self.assertIn("error", result)

    @patch("agent.requests.post")
    def test_api_connection_error_handling(self, mock_post):
        """Test transport connection error handling."""
        import requests
        mock_post.side_effect = requests.ConnectionError("Failed to establish a new connection")

        raw_input = "Email sensitive@example.com."
        result = sanitize(raw_input, call_api=True)

        self.assertEqual(result["status"], "error")
        self.assertNotIn("sensitive@example.com", result["data"]["sanitized_content"])
        self.assertIn("[EMAIL]", result["data"]["sanitized_content"])

    @patch("agent.requests.post")
    def test_api_402_payment_required_handling(self, mock_post):
        """Test safe handling when API returns 402 Payment Required."""
        mock_response = MagicMock()
        mock_response.status_code = 402
        mock_response.json.return_value = {"error": "Payment required"}
        mock_post.return_value = mock_response

        raw_input = "My email is user@example.com."
        result = sanitize(raw_input, call_api=True)

        self.assertEqual(result["status"], "payment_required")
        # Ensure local sanitization was not wiped out
        self.assertEqual(result["data"]["sanitized_content"], "My email is [EMAIL].")
        self.assertEqual(result["sanitized_content"], "My email is [EMAIL].")

    @patch("agent.requests.post")
    def test_api_500_server_error_handling(self, mock_post):
        """Test safe handling when API returns HTTP 500 error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        raw_input = "My email is user@example.com."
        result = sanitize(raw_input, call_api=True)

        self.assertEqual(result["status"], "error")
        self.assertEqual(result["http_status"], 500)
        self.assertEqual(result["data"]["sanitized_content"], "My email is [EMAIL].")


class TestRegressionAndCompatibility(unittest.TestCase):
    """Ensure backward compatibility with legacy calls and self-checks."""

    def test_self_checks_pass(self):
        """Verify the built-in self checks pass without error."""
        _run_self_checks()

    def test_legacy_dictionary_shape(self):
        """Ensure both data.sanitized_content and top-level sanitized_content exist."""
        result = sanitize("Call 555-123-4567 or email a@b.com", context="medical", tx_hash="TRIAL")
        self.assertIn("data", result)
        self.assertIn("sanitized_content", result["data"])
        self.assertIn("sanitized_content", result)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "success")

    def test_local_only_function(self):
        """Test sanitize_locally standalone function."""
        res = sanitize_locally("Email a@b.com.")
        self.assertEqual(res["data"]["sanitized_content"], "Email [EMAIL].")
        self.assertEqual(res["status"], "success")


if __name__ == "__main__":
    unittest.main()
