# Run EthioPulse-Forecaster dashboard (Streamlit)
# Use this if "streamlit" is not recognized (e.g. not installed in your venv).
$ProjectRoot = $PSScriptRoot
$VenvPath = Join-Path $ProjectRoot ".venv"
if (-not (Test-Path (Join-Path $VenvPath "Scripts\pip.exe"))) {
    $VenvPath = Join-Path (Split-Path $ProjectRoot -Parent) ".venv"
}

# Prefer venv's pip and streamlit if .venv exists
if (Test-Path (Join-Path $VenvPath "Scripts\pip.exe")) {
    Write-Host "Using .venv at $VenvPath"
    & (Join-Path $VenvPath "Scripts\pip.exe") install streamlit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & (Join-Path $VenvPath "Scripts\streamlit.exe") run (Join-Path $ProjectRoot "dashboard\app.py")
} else {
    # Fallback: use current Python (e.g. already activated venv or system)
    python -m pip install streamlit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -m streamlit run (Join-Path $ProjectRoot "dashboard\app.py")
}
