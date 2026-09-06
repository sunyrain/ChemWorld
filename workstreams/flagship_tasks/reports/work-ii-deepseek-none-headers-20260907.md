# DeepSeek none: header controls

Two fixed engineering requests; identical public constant body.

```json
{
  "formal_result": false,
  "scheduled": 2,
  "real_requests": 2,
  "provider_retries": 0,
  "results": [
    {
      "condition": "full_codex_headers",
      "forwarded_header_names": [
        "User-Agent",
        "Accept",
        "Content-Type",
        "Originator",
        "Session-Id",
        "Thread-Id",
        "X-Client-Request-Id",
        "X-Codex-Beta-Features",
        "X-Codex-Turn-Metadata",
        "X-Codex-Window-Id"
      ],
      "http_status": 200,
      "usage": {
        "input_tokens": 4671,
        "input_tokens_details": {
          "cached_tokens": 2304
        },
        "output_tokens": 55,
        "output_tokens_details": {
          "reasoning_tokens": 49
        },
        "total_tokens": 4726
      },
      "response_status": "completed",
      "valid_json": true,
      "reasoning_tokens": 49,
      "passed": false,
      "wall_seconds": 1.0940000000409782
    },
    {
      "condition": "codex_user_agent_only",
      "forwarded_header_names": [
        "User-Agent"
      ],
      "http_status": 200,
      "usage": {
        "input_tokens": 4671,
        "input_tokens_details": {
          "cached_tokens": 4608
        },
        "output_tokens": 21,
        "output_tokens_details": {
          "reasoning_tokens": 15
        },
        "total_tokens": 4692
      },
      "response_status": "completed",
      "valid_json": true,
      "reasoning_tokens": 15,
      "passed": false,
      "wall_seconds": 0.5
    }
  ]
}
```
