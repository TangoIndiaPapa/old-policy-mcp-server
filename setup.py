from setuptools import setup, find_packages

setup(
    name="policy-mcp-server",
    version="0.1.0",
    description="MCP server following FAST MCP spec.",
    author="AI Generated",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],  # Dependencies are managed in requirements.txt
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "policy-mcp-server=policy_mcp_server.server:PolicyMCPServer"
        ]
    },
)
