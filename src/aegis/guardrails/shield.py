import re
import hmac
hashlib = __import__('hashlib')
from typing import Tuple
from aegis.core.config import settings
from aegis.core.schemas import AegisRequest


class EdgeShield:
    """
    Module 1: The Edge Shield.
    Performs Format-Preserving Tokenization and Prompt Injection screening
    before any request touches downstream LLM or agent modules.
    """
    
    # Regex pattern for a sample 10 to 12 digit bank account number
    ACCOUNT_PATTERN = re.compile(r'\b\d{10,12}\b')

    @classmethod
    def tokenize_pii(cls, text: str) -> Tuple[str, str]:
        """
        Swaps sensitive account numbers with deterministic cryptographic tokens
        using our secret tokenization salt so the LLM never sees raw PII.
        """
        salt = settings.tokenization_salt.get_secret_value().encode('utf-8')

        def replace_match(match: re.Match) -> str:
            raw_val = match.group(0)
            # Create a HMAC-SHA256 token keyed with our salt
            digest = hmac.new(salt, raw_val.encode('utf-8'), hashlib.sha256).hexdigest()
            # Return a realistic-looking 10-digit token prefix
            return f"TOK_ACC_{digest[:10].upper()}"

        sanitized_text = cls.ACCOUNT_PATTERN.sub(replace_match, text)
        token_map_id = "token_map_active"  # In enterprise code, store mapping in Redis/Vault
        return sanitized_text, token_map_id

    @classmethod
    def detect_prompt_injection(cls, query: str) -> bool:
        """
        Scans for common prompt injection and jailbreak signatures.
        Returns True if a malicious injection pattern is detected.
        """
        malicious_patterns = [
            "ignore previous instructions",
            "disregard previous rules",
            "you are now unrestricted",
            "system override",
            "show me everyone's salary"
        ]
        query_lower = query.lower()
        for pattern in malicious_patterns:
            if pattern in query_lower:
                return True
        return False

    @classmethod
    def process_incoming_request(cls, raw_query: str) -> AegisRequest:
        """
        Main entrypoint for Module 1. Screens for injections and tokenizes PII.
        """
        # 1. Check for prompt injection
        if cls.detect_prompt_injection(raw_query):
            raise ValueError("Security Violation: Potential Prompt Injection or Jailbreak detected!")

        # 2. Tokenize sensitive PII
        sanitized, map_id = cls.tokenize_pii(raw_query)

        # 3. Return the hardened request envelope
        return AegisRequest(
            raw_query=raw_query,
            sanitized_query=sanitized,
            token_map_id=map_id
        )