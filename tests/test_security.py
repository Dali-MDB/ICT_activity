from datetime import datetime

import app.security as security


def test_create_and_verify_token_roundtrip(monkeypatch):
    monkeypatch.setattr(security, "SECRET_KEY", "test-secret", raising=False)
    monkeypatch.setattr(security, "ALGORITHM", "HS256", raising=False)

    token = security.create_token({"sub": "user@example.com"})
    payload = security.verify_token(token)

    assert payload is not None
    assert payload["sub"] == "user@example.com"
    assert "exp" in payload
    assert isinstance(payload["exp"], int) or isinstance(payload["exp"], datetime)
