from setuptools import setup, find_packages

setup(
    name="maverick-mcp-server",
    version="1.0.0",
    description="MCP Server for Maverick Site Management - Create and Query Sites",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.10.0",
        "httpx>=0.25.0",
    ],
    entry_points={
        "console_scripts": [
            "maverick-mcp-server=server:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
