$env:PYTHONUNBUFFERED="TRUE"
$env:CORS_ORIGINS="http://localhost:3000"
$env:DATABASE_URI="postgresql://postgres:postgres@127.0.0.1:5432/spendkey"
$env:ENABLE_OPENAPI_DOCS="true"
$env:OPENAI_KEY="dummy-key"
.\venv\Scripts\python.exe -m uvicorn --factory app.server.factory:create_app --port 8000
