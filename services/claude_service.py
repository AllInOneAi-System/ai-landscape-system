"""
Service Layer — Anthropic API Integration
Handles all Claude API calls with proper error handling
"""

import anthropic
from typing import Generator


def get_client(api_key: str) -> anthropic.Anthropic:
    """Initialize Anthropic client with given API key."""
    return anthropic.Anthropic(api_key=api_key)


def stream_response(
    api_key: str,
    system_prompt: str,
    messages: list[dict],
    model: str = "claude-sonnet-4-5",
    max_tokens: int = 1500,
) -> Generator[str, None, None]:
    """
    Stream response from Claude API.
    Yields text chunks as they arrive.
    """
    client = get_client(api_key)

    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


def get_response(
    api_key: str,
    system_prompt: str,
    messages: list[dict],
    model: str = "claude-sonnet-4-5",
    max_tokens: int = 1500,
) -> str:
    """
    Get complete response from Claude API (non-streaming).
    Returns full response text.
    """
    client = get_client(api_key)

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=messages,
    )

    return response.content[0].text


def validate_api_key(api_key: str) -> tuple[bool, str]:
    """
    Validate API key by making a minimal test call.
    Returns (is_valid, message)
    """
    if not api_key:
        return False, "ยังไม่ได้ใส่ API key"
    if not api_key.startswith("sk-ant-"):
        return False, "รูปแบบ API key ไม่ถูกต้อง (ต้องขึ้นต้นด้วย sk-ant-)"
    try:
        client = get_client(api_key)
        client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            messages=[{"role": "user", "content": "hi"}],
        )
        return True, "✅ API key ใช้งานได้"
    except anthropic.AuthenticationError:
        return False, "❌ API key ไม่ถูกต้องหรือหมดอายุ"
    except anthropic.RateLimitError:
        return False, "⚠️ Rate limit — key ถูกต้อง แต่ถูก limit ชั่วคราว"
    except Exception as e:
        return False, f"❌ เกิดข้อผิดพลาด: {str(e)}"
