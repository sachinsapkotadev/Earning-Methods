@echo off
echo ============================================
echo   Sachin's AI Earning Ecosystem - Setup
echo ============================================
echo.

echo [1/3] Installing Python dependencies...
pip install openai httpx rich jinja2 python-dotenv
echo.

echo [2/3] Checking Python version...
python --version
echo.

echo [3/3] Setup complete!
echo.
echo ============================================
echo   NEXT STEPS:
echo.
echo   1. Get FREE API key from https://console.groq.com
echo   2. Edit ai-system\.env and add your GROQ_API_KEY
echo   3. Run: python ai-system\main.py
echo.
echo   For individual tools:
echo   - python "Tier-1-Start-Immediately\data_entry\run.py"
echo   - python "Tier-1-Start-Immediately\content_writing\run.py"
echo   - python "Tier-2-Build-Skills\seo_content\run.py"
echo ============================================
pause
