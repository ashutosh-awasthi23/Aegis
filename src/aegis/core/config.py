from enum import Enum
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str,Enum):
    LOCAL = "local"
    STAGING = "staging"
    SHADOW = "shadow"       # For Shadow Deployment testing
    PRODUCTION = "production"

class AegisSettings(BaseSettings):
    """Centralized, validated configuration for Project Aegis."""
    app_name: str = "Aegis Banking AI"
    environment: Environment = Field(default=Environment.LOCAL)
    # Security & Tokenization Secrets (SecretStr prevents accidental logging!)
    tokenization_salt: SecretStr = Field(
        default=SecretStr("dev-only-salt-change-in-prod-32bytes"),
        description="Cryptographic salt for Format-Preserving Tokenization"
    )
    # Model Endpoints (Cloud vs Air-Gapped On-Prem)
    frontier_cloud_model: str = "gpt-4o-mini"
    airgapped_local_model_url: str = "http://localhost:11434/v1"  # e.g., Local Llama/Mistral via vLLM/Ollama

    enable_worm_audit_log: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = AegisSettings()




