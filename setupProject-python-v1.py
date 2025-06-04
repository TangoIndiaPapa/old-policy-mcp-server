"""
File name: setupProject-python-v1.py
File description: Project scaffolding script for MCP server (policy-mcp-server).
Author: AI Generated
Date created: 2025-06-02
Last modified date: 2025-06-02
Version number: 1.0
AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.
"""
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# Updated for new package structure (2025-06-04)
SERVER_DIR = PROJECT_ROOT
SRC_DIR = os.path.join(PROJECT_ROOT, "src", "policy_mcp_server")
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
folders = [SRC_DIR, TESTS_DIR, CONFIG_DIR, LOGS_DIR]

def py_header(file_name, desc):
    """Return a valid Python file header using # comments."""
    return (
        f'# File name: {file_name}\n'
        f'# File description: {desc}\n'
        f'# Author: AI Generated\n'
        f'# Date created: 2025-06-02\n'
        f'# Last modified date: 2025-06-02\n'
        f'# Version number: 1.0\n'
        f'# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.\n'
        f'# MIT License\n'
    )

def md_header(file_name, desc):
    """Return a Markdown comment header."""
    return f'<!--\nFile name: {file_name}\nFile description: {desc}\nAuthor: AI Generated\nDate created: 2025-06-02\nLast modified date: 2025-06-02\nVersion number: 1.0\nAI WARNING: This file is generated with AI assistance. Please review and verify the content before use.\nMIT License\n-->'

def env_header(file_name, desc):
    """Return a shell-style comment header for .env files."""
    return f'# File name: {file_name}\n# File description: {desc}\n# Author: AI Generated\n# Date created: 2025-06-02\n# Last modified date: 2025-06-02\n# Version number: 1.0\n# AI WARNING: This file is generated with AI assistance. Please review and verify the content before use.\n# MIT License\n'

files = {
    os.path.join(SERVER_DIR, "README.md"): md_header("README.md", "Project overview and instructions.") + "\n" + "# Policy MCP Server\n\n> AI WARNING: This content includes AI-generated code. Verify for accuracy and security before use.\n\n## Overview\nA Model Context Protocol (MCP) server following the FAST MCP specification. Modular, secure, XAI-compliant, and fully tested.\n\n## Architecture Diagram (ASCII)\n\n```\n+-------------------+\n|  Client/Consumer  |\n+--------+----------+\n         |\n         v\n+--------+----------+\n|   MCP Server API  |\n+--------+----------+\n         |\n         v\n+--------+----------+\n|   Core Logic      |\n+--------+----------+\n         |\n         v\n+--------+----------+\n|   Storage/Config  |\n+-------------------+\n```\n\n## Project Structure\n\n```\npolicy-mcp-server/\n  src/\n  tests/\n  config/\n  logs/\n  README.md\n  .env.example\n  pyproject.toml\n```\n\n## Setup\n\n1. Install uv (if not installed):\n   ```bash\n   pip install uv\n   ```\n2. Install dependencies:\n   ```bash\n   uv pip install --system -r requirements.txt\n   ```\n3. Copy `.env.example` to `.env` and configure as needed.\n\n## Running\n\n```bash\npython -m src.main\n```\n\n## Testing\n\n```bash\npython -m unittest discover tests\n```\n\n## License\nMIT\n",
    os.path.join(SERVER_DIR, ".env.example"): env_header(".env.example", "Example environment variables for MCP server.") + "\n" + "LOG_LEVEL=INFO\nMCP_SERVER_PORT=8000\nMCP_SERVER_HOST=0.0.0.0\n",
    os.path.join(SERVER_DIR, "pyproject.toml"): "[project]\nname = \"policy-mcp-server\"\nversion = \"0.1.0\"\ndescription = \"MCP server following FAST MCP spec.\"\nauthors = [\"AI Generated <ai@example.com>\"]\nlicense = \"MIT\"\n\n[tool.uv]\n# uv configuration placeholder\n",
    os.path.join(SERVER_DIR, "requirements.txt"): "flask\npydantic\n",
    os.path.join(SRC_DIR, "main.py"): py_header("main.py", "Main entry point for the MCP server.") + "\nimport logging\nfrom .server import create_app\n\ndef main():\n    app = create_app()\n    app.run()\n\nif __name__ == \"__main__\":\n    main()\n",
    os.path.join(SRC_DIR, "server.py"): py_header("server.py", "MCP server app factory.") + "\nimport logging\nfrom .settings import get_settings\nfrom flask import Flask\n\ndef create_app():\n    settings = get_settings()\n    app = Flask(__name__)\n    app.config['ENV'] = 'production'\n    app.config['DEBUG'] = False\n    # Logging setup\n    logging.basicConfig(level=settings.LOG_LEVEL)\n    @app.route(\"/healthz\")\n    def healthz():\n        return {\"status\": \"ok\"}\n    return app\n",
    os.path.join(SRC_DIR, "settings.py"): py_header("settings.py", "Configuration management using Pydantic BaseSettings.") + "\nfrom pydantic import BaseSettings\nimport os\n\nclass Settings(BaseSettings):\n    LOG_LEVEL: str = os.getenv(\"LOG_LEVEL\", \"INFO\")\n    MCP_SERVER_PORT: int = int(os.getenv(\"MCP_SERVER_PORT\", 8000))\n    MCP_SERVER_HOST: str = os.getenv(\"MCP_SERVER_HOST\", \"0.0.0.0\")\n\n    class Config:\n        env_file = '.env'\n\ndef get_settings():\n    return Settings()\n",
    os.path.join(TESTS_DIR, "test_healthz.py"): py_header("test_healthz.py", "Basic health check test for MCP server.") + "\nimport unittest\nfrom src.server import create_app\n\nclass TestHealthz(unittest.TestCase):\n    def setUp(self):\n        self.app = create_app().test_client()\n\n    def test_healthz(self):\n        resp = self.app.get(\"/healthz\")\n        self.assertEqual(resp.status_code, 200)\n        self.assertEqual(resp.json, {\"status\": \"ok\"})\n\nif __name__ == \"__main__\":\n    unittest.main()\n"
}

def main():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    for path, content in files.items():
        with open(path, "w") as f:
            f.write(content)
    print("Project structure created under policy-mcp-server/")

if __name__ == "__main__":
    main()
