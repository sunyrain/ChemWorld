$ErrorActionPreference = "Stop"
$smokeRoot = Join-Path $env:TEMP ("chemworld-wellau-smoke-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $smokeRoot | Out-Null
try {
    $schemaPath = Join-Path $smokeRoot "schema.json"
    $instructionsPath = Join-Path $smokeRoot "instructions.md"
    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [IO.File]::WriteAllText($schemaPath, '{"type":"object","properties":{"ok":{"type":"boolean"}},"required":["ok"],"additionalProperties":false}', $utf8NoBom)
    [IO.File]::WriteAllText($instructionsPath, "Return the requested JSON object.", $utf8NoBom)
    $instructionConfig = "model_instructions_file=" + ($instructionsPath -replace '\\', '/')
    $providerConfigs = @(
        'model_providers.wellau.name="WellAU"',
        'model_providers.wellau.base_url="https://api.wellau.com/v1"',
        'model_providers.wellau.env_key="WELLAU_API_KEY"',
        'model_providers.wellau.wire_api="responses"',
        'model_providers.wellau.supports_websockets=false'
    )
    $arguments = @(
        "exec", "--json", "--ephemeral", "--ignore-user-config", "--ignore-rules",
        "--skip-git-repo-check", "--output-schema", $schemaPath,
        "--disable", "shell_tool", "--disable", "apps", "--disable", "multi_agent", "--disable", "plugins",
        "-c", 'approval_policy="never"', "-c", 'web_search="disabled"',
        "-c", 'model_provider="wellau"',
        "-c", $providerConfigs[0], "-c", $providerConfigs[1],
        "-c", $providerConfigs[2], "-c", $providerConfigs[3],
        "-c", $providerConfigs[4],
        "-c", 'model_reasoning_effort="high"', "-c", $instructionConfig,
        "-m", "gpt-5.6-sol", "-C", $smokeRoot,
        '{"required_json_shape":{"ok":"boolean"},"request":"return ok true"}'
    )
    & codex @arguments
    exit $LASTEXITCODE
}
finally {
    if (Test-Path -LiteralPath $smokeRoot) {
        Remove-Item -LiteralPath $smokeRoot -Recurse -Force
    }
}
