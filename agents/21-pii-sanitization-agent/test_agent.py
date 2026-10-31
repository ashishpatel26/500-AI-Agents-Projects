"""Comprehensive unit and security tests for PII Sanitization Agent.

Includes thorough test coverage resolving all 11 Sourcery review findings:
1. API key detection (OpenAI sk-proj-, sk-svcacct-, GitHub github_pat_, etc.)
2. Metadata PII leakage prevention (context, tx_hash, wallet_address)
3. Case-insensitive government IDs and IBANs
4. Malformed API response handling (invalid JSON, unexpected types, missing fields)
5. Environment-based API configuration and CLI flag precedence
6. Self-check quota consumption (ensuring zero network calls)
7. Grouped bank account detection (hyphenated, spaced, labeled)
8. Formatted IBAN detection (spaces, hyphens, MOD-97 checksum, case-insensitivity)
9. Invalid timeout handling (zero, negative, non-numeric values)
10. Idempotency and retry safety (no invented headers or unsafe duplicate billing)
11. Empty CLI input handling (--text "" vs omitted vs non-empty vs file)
"""

import io
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Ensure agent directory is in path whether run from repo root or agent dir
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from agent import (
    ENDPOINT,
    _is_iban_valid,
    _is_luhn_valid,
    _run_self_checks,
    _sanitize_with_counts,
    _validate_and_sanitize_metadata,
    main,
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
        prompt_example = "My email is akif@example.com and my phone number is 9876543210."
        sanitized = sanitize_text(prompt_example)
        self.assertEqual(sanitized, "My email is [EMAIL] and my phone number is [PHONE].")

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

        invalid_ip_text = "Versions are 1.2.3 and 999.999.999.999."
        self.assertEqual(sanitize_text(invalid_ip_text), invalid_ip_text)

    def test_credit_card_detection_and_luhn_validation(self):
        """Test credit card masking and verify Luhn checksum validation."""
        valid_card = "Card number 4111-1111-1111-1111 used for payment."
        sanitized = sanitize_text(valid_card)
        self.assertNotIn("4111-1111-1111-1111", sanitized)
        self.assertEqual(sanitized, "Card number [CREDIT_CARD] used for payment.")

        self.assertTrue(_is_luhn_valid("4111111111111111"))
        self.assertFalse(_is_luhn_valid("4111111111111112"))

    def test_ssn_detection_and_masking(self):
        """Test US Social Security Number detection."""
        text = "Social Security number is 123-45-6789."
        sanitized = sanitize_text(text)
        self.assertNotIn("123-45-6789", sanitized)
        self.assertEqual(sanitized, "Social Security number is [SSN].")

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


class TestSourceryFinding1ApiKeyDetection(unittest.TestCase):
    """Finding 1: Extended API key detection (OpenAI sk-proj-, sk-svcacct-, GitHub github_pat_, etc.)."""

    def test_openai_sk_proj_keys(self):
        """Test OpenAI project-scoped API key detection."""
        key = "sk-proj-abc123DEF456ghi789JKL012_mnop345-QRST678"
        text = f"My OpenAI key is {key}."
        sanitized = sanitize_text(text)
        self.assertNotIn(key, sanitized)
        self.assertEqual(sanitized, "My OpenAI key is [API_KEY].")

    def test_openai_sk_svcacct_keys(self):
        """Test OpenAI service account API key detection."""
        key = "sk-svcacct-serviceaccount1234567890abcdef_GH"
        text = f"Auth using {key} for agent."
        sanitized = sanitize_text(text)
        self.assertNotIn(key, sanitized)
        self.assertEqual(sanitized, "Auth using [API_KEY] for agent.")

    def test_github_pat_fine_grained_tokens(self):
        """Test GitHub fine-grained personal access token detection."""
        token = "github_pat_11ABCD1234_abcdefghijklmnopqrstuvwxyz1234567890"
        text = f"Token: {token}."
        sanitized = sanitize_text(text)
        self.assertNotIn(token, sanitized)
        self.assertEqual(sanitized, "Token: [API_KEY].")

    def test_standard_openai_github_aws_keys(self):
        """Test existing key formats (OpenAI sk-, GitHub ghp_, AWS AKIA)."""
        openai_key = "sk-abc123fakekeynotreal0000000000"
        github_token = "ghp_0123456789abcdefghijklmnopqrstuvwxyz12"
        aws_key = "AKIAIOSFODNN7EXAMPLE"
        text = f"Keys: {openai_key}, {github_token}, and {aws_key}."
        sanitized = sanitize_text(text)
        self.assertNotIn(openai_key, sanitized)
        self.assertNotIn(github_token, sanitized)
        self.assertNotIn(aws_key, sanitized)
        self.assertEqual(sanitized, "Keys: [API_KEY], [API_KEY], and [API_KEY].")


class TestSourceryFinding2MetadataPIILeakage(unittest.TestCase):
    """Finding 2: Prevent metadata PII leakage in context, tx_hash, and wallet_address."""

    @patch("agent.requests.post")
    def test_pii_in_context_is_blocked(self, mock_post):
        """Ensure sensitive user PII in context field is blocked from network transmission."""
        raw_text = "Hello world."
        pii_context = "juan.perez@example.com"
        result = sanitize(raw_text, context=pii_context, call_api=True)
        # External transmission must be blocked, falling back safely to local sanitization
        mock_post.assert_not_called()
        self.assertEqual(result["status"], "error")
        self.assertIn("Metadata 'context' contains", result["error"])
        self.assertEqual(result["data"]["sanitized_content"], "Hello world.")

    @patch("agent.requests.post")
    def test_pii_in_tx_hash_is_blocked(self, mock_post):
        """Ensure sensitive user PII in tx_hash field is blocked from network transmission."""
        raw_text = "Clean message"
        pii_tx = "9876543210"  # phone number passed as tx_hash
        result = sanitize(raw_text, tx_hash=pii_tx, call_api=True)
        mock_post.assert_not_called()
        self.assertEqual(result["status"], "error")
        self.assertIn("Metadata 'tx_hash' contains", result["error"])

    @patch.dict(os.environ, {"TRUSTBOOST_WALLET": "user@example.com"})
    @patch("agent.requests.post")
    def test_pii_in_wallet_env_is_blocked(self, mock_post):
        """Ensure sensitive PII in TRUSTBOOST_WALLET env var is blocked from network transmission."""
        result = sanitize("Some text", call_api=True)
        mock_post.assert_not_called()
        self.assertEqual(result["status"], "error")
        self.assertIn("Metadata 'wallet_address' contains", result["error"])

    @patch("agent.requests.post")
    def test_entire_outgoing_json_payload_inspected(self, mock_post):
        """Test that legitimate metadata succeeds and full outgoing JSON contains zero PII."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "status": "success",
            "data": {"sanitized_content": "[EMAIL] called [PHONE]"},
        }
        mock_post.return_value = mock_resp

        raw_input = "Contact victim@example.com or 9876543210."
        sanitize(raw_input, context="financial", tx_hash="solana_tx_valid_123", call_api=True)

        mock_post.assert_called_once()
        payload = mock_post.call_args.kwargs["json"]
        payload_json = json.dumps(payload)

        # Full serialized inspection
        self.assertNotIn("victim@example.com", payload_json)
        self.assertNotIn("9876543210", payload_json)
        self.assertEqual(payload["context"], "financial")
        self.assertEqual(payload["tx_hash"], "solana_tx_valid_123")


class TestSourceryFinding3CaseInsensitiveGovIDsAndIBANs(unittest.TestCase):
    """Finding 3: Case-insensitive government IDs (RFC/CURP) and IBANs."""

    def test_government_id_case_variations(self):
        """Test uppercase, lowercase, and mixed-case government IDs."""
        upper = "RFC: PEMJ880126MNEZSN01."
        lower = "RFC: pemj880126mnezsn01."
        mixed = "RFC: Pemj880126Mnezsn01."

        self.assertEqual(sanitize_text(upper), "RFC: [GOV_ID].")
        self.assertEqual(sanitize_text(lower), "RFC: [GOV_ID].")
        self.assertEqual(sanitize_text(mixed), "RFC: [GOV_ID].")

    def test_iban_case_variations(self):
        """Test uppercase, lowercase, and mixed-case IBANs."""
        upper = "IBAN: GB82WEST12345698765432"
        lower = "IBAN: gb82west12345698765432"
        mixed = "IBAN: Gb82West12345698765432"

        self.assertEqual(sanitize_text(upper), "IBAN: [BANK_ACCOUNT]")
        self.assertEqual(sanitize_text(lower), "IBAN: [BANK_ACCOUNT]")
        self.assertEqual(sanitize_text(mixed), "IBAN: [BANK_ACCOUNT]")


class TestSourceryFinding4MalformedAPIResponseHandling(unittest.TestCase):
    """Finding 4: Handle invalid JSON, unexpected types, and missing fields from remote API."""

    @patch("agent.requests.post")
    def test_http_200_invalid_json(self, mock_post):
        """When API returns 200 with invalid JSON, report error status and preserve local content."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.side_effect = ValueError("Invalid JSON in response")
        mock_post.return_value = mock_resp

        result = sanitize("Email user@example.com", call_api=True)
        self.assertEqual(result["status"], "error")
        self.assertIn("invalid JSON", result["error"])
        self.assertEqual(result["data"]["sanitized_content"], "Email [EMAIL]")

    @patch("agent.requests.post")
    def test_http_200_unexpected_json_type(self, mock_post):
        """When API returns 200 with a list or int instead of dict, report error status."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = ["unexpected", "array"]
        mock_post.return_value = mock_resp

        result = sanitize("Phone 9876543210", call_api=True)
        self.assertEqual(result["status"], "error")
        self.assertIn("unexpected JSON type", result["error"])
        self.assertEqual(result["data"]["sanitized_content"], "Phone [PHONE]")

    @patch("agent.requests.post")
    def test_http_200_missing_response_fields(self, mock_post):
        """When API returns empty dict or dict missing sanitized_content/status, report error."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"unrelated": "data"}
        mock_post.return_value = mock_resp

        result = sanitize("Card 4111-1111-1111-1111", call_api=True)
        self.assertEqual(result["status"], "error")
        self.assertIn("missing required fields", result["error"])
        self.assertEqual(result["data"]["sanitized_content"], "Card [CREDIT_CARD]")


class TestSourceryFinding5EnvironmentBasedAPIConfiguration(unittest.TestCase):
    """Finding 5: Respect TRUSTBOOST_CALL_API when unspecified, and preserve explicit CLI flags."""

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("agent.sanitize")
    def test_cli_api_flag_enables_remote(self, mock_sanitize, mock_stdout):
        """Passing --api explicitly enables remote API verification."""
        mock_sanitize.return_value = {"status": "success", "sanitized_content": "Test"}
        with patch.object(sys, "argv", ["agent.py", "--text", "Test", "--api"]):
            main()
            mock_sanitize.assert_called_once_with("Test", context="general", tx_hash="TRIAL", call_api=True)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("agent.sanitize")
    def test_cli_local_flag_overrides_environment(self, mock_sanitize, mock_stdout):
        """Passing --local explicitly forces local-only mode even when env is true."""
        mock_sanitize.return_value = {"status": "success", "sanitized_content": "Test"}
        with patch.dict(os.environ, {"TRUSTBOOST_CALL_API": "true"}):
            with patch.object(sys, "argv", ["agent.py", "--text", "Test", "--local"]):
                main()
                mock_sanitize.assert_called_once_with("Test", context="general", tx_hash="TRIAL", call_api=False)

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("agent.sanitize")
    def test_cli_unspecified_respects_env_true(self, mock_sanitize, mock_stdout):
        """When CLI flag is omitted, call_api is None so sanitize() respects env setting."""
        mock_sanitize.return_value = {"status": "success", "sanitized_content": "Test"}
        with patch.object(sys, "argv", ["agent.py", "--text", "Test"]):
            main()
            mock_sanitize.assert_called_once_with("Test", context="general", tx_hash="TRIAL", call_api=None)

    @patch("agent.requests.post")
    def test_sanitize_reads_env_when_call_api_is_none(self, mock_post):
        """Verify sanitize() reads TRUSTBOOST_CALL_API=true when call_api is None."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "success", "sanitized_content": "Clean"}
        mock_post.return_value = mock_resp

        with patch.dict(os.environ, {"TRUSTBOOST_CALL_API": "true"}):
            sanitize("Hello", call_api=None)
            mock_post.assert_called_once()


class TestSourceryFinding6SelfCheckQuotaConsumption(unittest.TestCase):
    """Finding 6: Ensure _run_self_checks() always runs in local-only mode."""

    @patch("agent.requests.post")
    def test_self_checks_never_call_api_even_when_env_enabled(self, mock_post):
        """Self-checks must never perform network calls even if TRUSTBOOST_CALL_API is enabled."""
        with patch.dict(os.environ, {"TRUSTBOOST_CALL_API": "true"}):
            _run_self_checks()
            mock_post.assert_not_called()


class TestSourceryFinding7GroupedBankAccountDetection(unittest.TestCase):
    """Finding 7: Improve BANK_ACCOUNT_RE to support hyphenated and spaced account numbers."""

    def test_labeled_account_with_hyphens(self):
        """Test Account: 1234-5678-90 format."""
        text = "Account: 1234-5678-90."
        sanitized = sanitize_text(text)
        self.assertNotIn("1234-5678-90", sanitized)
        self.assertEqual(sanitized, "Account: [BANK_ACCOUNT].")

    def test_labeled_account_number_with_spaces(self):
        """Test Account Number: 1234 5678 90 format."""
        text = "Account Number: 1234 5678 90"
        sanitized = sanitize_text(text)
        self.assertNotIn("1234 5678 90", sanitized)
        self.assertEqual(sanitized, "Account Number: [BANK_ACCOUNT]")

    def test_labeled_acc_no_unspaced(self):
        """Test Acc No: 123456789012 format."""
        text = "Acc No: 123456789012"
        sanitized = sanitize_text(text)
        self.assertNotIn("123456789012", sanitized)
        self.assertEqual(sanitized, "Acc No: [BANK_ACCOUNT]")

    def test_labeled_cuenta_bancaria(self):
        """Test Spanish label Cuenta: 1234-5678-90-12."""
        text = "Cuenta: 1234-5678-90-12"
        sanitized = sanitize_text(text)
        self.assertNotIn("1234-5678-90-12", sanitized)
        self.assertEqual(sanitized, "Cuenta: [BANK_ACCOUNT]")


class TestSourceryFinding8FormattedIBANDetection(unittest.TestCase):
    """Finding 8: Formatted IBAN detection with spaces, hyphens, MOD-97 check and case variations."""

    def test_spaced_iban_from_prompt_example(self):
        """Test exact prompt example: GB29 WEST 1234 5698 7654 32."""
        text = "Send transfer to GB29 WEST 1234 5698 7654 32."
        sanitized = sanitize_text(text)
        self.assertNotIn("GB29 WEST 1234 5698 7654 32", sanitized)
        self.assertEqual(sanitized, "Send transfer to [BANK_ACCOUNT].")

    def test_german_spaced_iban(self):
        """Test German IBAN with standard 4-block spacing."""
        text = "IBAN: DE89 3704 0044 0532 0130 00"
        sanitized = sanitize_text(text)
        self.assertNotIn("DE89 3704 0044 0532 0130 00", sanitized)
        self.assertEqual(sanitized, "IBAN: [BANK_ACCOUNT]")

    def test_hyphenated_iban(self):
        """Test IBAN with hyphen separators."""
        text = "Wire to GB82-WEST-1234-5698-7654-32."
        sanitized = sanitize_text(text)
        self.assertNotIn("GB82-WEST-1234-5698-7654-32", sanitized)
        self.assertEqual(sanitized, "Wire to [BANK_ACCOUNT].")

    def test_mod97_checksum_helper(self):
        """Verify _is_iban_valid detects genuine and invalid IBANs."""
        self.assertTrue(_is_iban_valid("GB82WEST12345698765432"))
        self.assertFalse(_is_iban_valid("GB00WEST12345698765432"))  # invalid checksum


class TestSourceryFinding9InvalidTimeoutHandling(unittest.TestCase):
    """Finding 9: Validate timeout parameter and safely fall back without raising ValueError."""

    def test_zero_timeout(self):
        """Zero timeout should be rejected safely, preserving local sanitization."""
        result = sanitize("Contact 9876543210", call_api=True, timeout=0)
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid timeout value", result["error"])
        self.assertEqual(result["data"]["sanitized_content"], "Contact [PHONE]")

    def test_negative_timeout(self):
        """Negative timeout should be rejected safely."""
        result = sanitize("Contact 9876543210", call_api=True, timeout=-10)
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid timeout value", result["error"])
        self.assertEqual(result["data"]["sanitized_content"], "Contact [PHONE]")

    def test_non_numeric_timeout(self):
        """Non-numeric timeout should be caught safely without unhandled exception."""
        result = sanitize("Contact 9876543210", call_api=True, timeout="not-a-number")
        self.assertEqual(result["status"], "error")
        self.assertIn("Invalid timeout value", result["error"])

    @patch("agent.requests.post")
    def test_valid_float_timeout(self, mock_post):
        """Valid positive timeout is accepted and passed to requests.post."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "success", "sanitized_content": "Clean"}
        mock_post.return_value = mock_resp

        sanitize("Contact info", call_api=True, timeout=12.5)
        self.assertEqual(mock_post.call_args.kwargs["timeout"], 12.5)


class TestSourceryFinding10IdempotencyAndRetrySafety(unittest.TestCase):
    """Finding 10: Verify no undocumented idempotency headers or unsafe duplicate retries."""

    @patch("agent.requests.post")
    def test_no_invented_idempotency_headers(self, mock_post):
        """Ensure agent does not inject unsupported headers like Idempotency-Key."""
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"status": "success", "sanitized_content": "Clean"}
        mock_post.return_value = mock_resp

        sanitize("Sample text", call_api=True)
        headers = mock_post.call_args.kwargs["headers"]
        self.assertNotIn("Idempotency-Key", headers)
        self.assertNotIn("X-Idempotency-Key", headers)

    @patch("agent.requests.post")
    def test_no_automatic_billable_retries_on_failure(self, mock_post):
        """Failures must not trigger blind auto-retries that could double-bill the wallet."""
        mock_resp = MagicMock()
        mock_resp.status_code = 402
        mock_post.return_value = mock_resp

        sanitize("Sample text", call_api=True)
        # requests.post must be called exactly once
        self.assertEqual(mock_post.call_count, 1)


class TestSourceryFinding11EmptyCLIInput(unittest.TestCase):
    """Finding 11: Correctly process explicitly empty --text \"\" vs omitted vs non-empty vs file."""

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_explicitly_empty_text(self, mock_stdout):
        """When --text \"\" is passed, process empty string and do not run DEMO_TEXT."""
        with patch.object(sys, "argv", ["agent.py", "--text", ""]):
            main()
            output = mock_stdout.getvalue()
            # Must NOT print the demo greeting
            self.assertNotIn("Running demo with local pre-sanitization", output)
            result = json.loads(output)
            self.assertEqual(result["data"]["sanitized_content"], "")
            self.assertEqual(result["data"]["entities"], [])

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_omitted_text_runs_demo(self, mock_stdout):
        """When neither --text nor --file is supplied, runs DEMO_TEXT."""
        with patch.object(sys, "argv", ["agent.py"]):
            main()
            output = mock_stdout.getvalue()
            self.assertIn("Running demo with local pre-sanitization", output)
            result = json.loads(output.split("\n\n")[1])
            self.assertIn("[EMAIL]", result["data"]["sanitized_content"])

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_non_empty_text_cli(self, mock_stdout):
        """When non-empty --text is provided, processes it directly."""
        with patch.object(sys, "argv", ["agent.py", "--text", "Email a@b.com"]):
            main()
            output = mock_stdout.getvalue()
            result = json.loads(output)
            self.assertEqual(result["data"]["sanitized_content"], "Email [EMAIL]")

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_file_based_input(self, mock_stdout):
        """When --file is provided, reads and sanitizes the file contents."""
        with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
            tmp.write("Call 9876543210")
            tmp_path = tmp.name

        try:
            with patch.object(sys, "argv", ["agent.py", "--file", tmp_path]):
                main()
                output = mock_stdout.getvalue()
                result = json.loads(output)
                self.assertEqual(result["data"]["sanitized_content"], "Call [PHONE]")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()
