# Sybex Oracle Node

A Python-based oracle system for prediction markets on the blockchain. The Sybex Oracle Node automatically resolves questions posed by users based on verifiable evidence using AI-powered research and multiple data sources.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Architecture](#architecture)
- [Environment Variables](#environment-variables)
- [Becoming a Resolver Operator](#becoming-a-resolver-operator)
- [Project Structure](#project-structure)
- [Development](#development)
- [License](#license)

## Features

- **Automated Question Resolution**: Automatically fetches and resolves prediction market questions
- **AI-Powered Research**: Uses multi-agentic AI system (OpenRouter/GPT) to research and determine outcomes
- **Multiple Data Sources**: Integrates NewsAPI, IPFS, and web scraping for evidence gathering
- **Blockchain Integration**: Direct interaction with smart contracts on Binance Smart Chain (BSC)
- **Evidence-Based Resolution**: Only resolves questions with verifiable evidence
- **Multiple Question Types**: Supports binary, categorical, numerical, and range numerical questions
- **Rich Logging**: Beautiful console output with detailed logging
- **Docker Support**: Includes IPFS container setup

## Prerequisites

Before running the Sybex Oracle Node, ensure you have the following installed:

- **Python 3.10+**: Required for running the application
- **uv**: Fast Python package installer and resolver (recommended for dependency management)
- **IPFS Node**: For decentralized storage (can run via Docker)
- **NewsAPI Key**: For fetching news articles
- **OpenRouter API Key**: For AI-powered resolution
- **Web3 Wallet**: With BNB for gas fees on Binance Smart Chain

### Installing uv

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sybex-node-python.git
cd sybex-node-python
```

### 2. Install Dependencies with uv

```bash
# Install all dependencies
uv pip install -e .

# Or install from pyproject.toml directly
uv pip install -r pyproject.toml
```

### 3. Set Up IPFS (Optional)

You can run a local IPFS node using Docker:

```bash
docker-compose up -d
```

Or run IPFS manually:

```bash
ipfs daemon
```

## Configuration

### 1. Environment Variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# News API Configuration - Get your key from https://newsapi.org/
NEWSAPI_API_KEY=your_newsapi_key_here

# Blockchain Configuration
RELAYER_RPC_URL=https://bsc-dataseed.binance.org/
RELAYER_PRIVATE_KEY=your_wallet_private_key_here

# IPFS Configuration
IPFS_NODE_URL=http://localhost:5001

# GraphQL API
GRAPHQL_API_URL=https://graph.sybex.app/subgraphs/name/sybex/graphql

# AI/Agentic Configuration - Get your key from https://openrouter.ai/
AGENTIC_BASE_URL=https://openrouter.ai/api/v1
AGENTIC_API_KEY=your_openrouter_key_here
AGENTIC_MODEL=gpt-4o-mini
```

### 2. Getting API Keys

| Service | Description | Link |
|---------|-------------|------|
| **NewsAPI** | For fetching news articles | https://newsapi.org/ |
| **OpenRouter** | For AI-powered resolution | https://openrouter.ai/ |

## Running the Application

### Using uv (Recommended)

```bash
# Run the main application
uv run app.py
```

### Using Python Directly

```bash
# Activate virtual environment (if using one)
source venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Run the application
python app.py
```

### What Happens When You Run the App

1. **Initialization**: The app initializes all services (logger, database, blockchain client, resolvers)
2. **Polling Service**: Starts polling every 5 seconds for new questions
3. **Question Processing**:
   - Fetches unanswered questions via GraphQL
   - Checks if deadlines have passed
   - Resolves eligible questions using AI research
   - Posts results back to the blockchain

### Stopping the Application

Press `Ctrl+C` to gracefully shut down the application.

## Architecture

The Sybex Oracle Node is built with a modular architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                         app.py                              │
│                    (Main Application)                       │
└───────────────────────────┬─────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Resolver    │   │   Relayer     │   │  Aggregator   │
│   Module      │   │   Module      │   │   Module      │
├───────────────┤   ├───────────────┤   ├───────────────┤
│ • GraphQL     │   │ • Web3 Client │   │ • NewsAPI     │
│ • Agentic AI  │   │ • AMM         │   │ • Web Scraper │
│ • Tools       │   │ • Contracts   │   │ • IPFS        │
└───────────────┘   └───────────────┘   └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                    ┌───────────────┐
                    │     IPFS      │
                    │     Storage   │
                    └───────────────┘
```

### Core Components

| Component | Description |
|-----------|-------------|
| **app.py** | Main entry point, manages polling and service initialization |
| **resolver/** | Question resolution logic using GraphQL and AI |
| **relayer/** | Blockchain interaction for posting resolutions |
| **aggregator/** | Data aggregation from NewsAPI and web sources |
| **ipfs.py** | IPFS client for decentralized storage |
| **orm/models.py** | Database models using Tortoise ORM |
| **logger.py** | Rich console logging configuration |

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEWSAPI_API_KEY` | Yes | - | API key for fetching news articles |
| `RELAYER_RPC_URL` | No | `https://bsc-dataseed.binance.org/` | BSC RPC endpoint |
| `RELAYER_PRIVATE_KEY` | Yes | - | Private key for signing transactions |
| `IPFS_NODE_URL` | No | `http://localhost:5001` | Local IPFS node URL |
| `GRAPHQL_API_URL` | No | `https://graph.sybex.app/subgraphs/name/sybex/graphql` | Sybex subgraph endpoint |
| `AGENTIC_BASE_URL` | No | `https://openrouter.ai/api/v1` | OpenRouter API base URL |
| `AGENTIC_API_KEY` | Yes | - | OpenRouter API key for AI services |
| `AGENTIC_MODEL` | No | `gpt-4o-mini` | AI model to use for resolution |

## Becoming a Resolver Operator

To become an authorized resolver operator for the Sybex Oracle Network, you need explicit permission from the Sybex team. This ensures network security and maintains the integrity of the oracle system.

### How to Apply

1. **Contact via X (Twitter)**: Reach out to the Sybex team via X to request operator status.

   - **X Profile**: [@sybexoracle](https://x.com/sybexoracle)

2. **Include in Your Request**:
   - Your experience with blockchain/oracle systems
   - Your technical infrastructure (server specs, uptime guarantees)
   - Your proposed operator node location
   - Any relevant background or references

3. **Review Process**:
   - The Sybex team will review your application
   - You may be asked for additional information
   - Approved operators will receive their operator credentials

4. **After Approval**:
   - You'll be added to the authorized operator list
   - Your node can start participating in the resolution process
   - You'll receive updates on network changes and requirements

### Operator Responsibilities

As an operator, you are expected to:
- Maintain high uptime for your node
- Ensure accurate and evidence-based resolutions
- Follow the network's resolution guidelines
- Keep your API keys and private keys secure
- Monitor your node's performance regularly

## Project Structure

```
sybex-node-python/
├── src/                     # Main source code
│   ├── app.py              # Core application logic
│   ├── resolver/           # Question resolution
│   │   ├── agentic.py      # AI-powered resolution
│   │   └── graphql.py      # GraphQL queries
│   ├── relayer/            # Blockchain interaction
│   │   ├── client.py       # Web3 client
│   │   ├── addresses.py    # Contract addresses
│   │   └── abis.py         # Contract ABIs
│   ├── aggregator/         # Data aggregation
│   │   └── newsapi.py      # News API client
│   ├── ipfs.py             # IPFS client
│   ├── orm/                # Database models
│   │   └── models.py
│   ├── logger.py           # Logging setup
│   ├── helpers.py          # Utility functions
│   └── constants.py        # Configuration constants
├── artifacts/              # Solidity contract artifacts
├── docker/                 # Docker configuration
├── app.py                  # Main entry point
├── pyproject.toml          # Project dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Development

### Running Tests

```bash
uv run pytest
```

### Building for Production

```bash
# Create executable using PyInstaller
uv run pyinstaller --onefile app.py
```

### Code Style

This project follows PEP 8 guidelines. Consider using:

```bash
# Format code with black
uv run black .

# Lint with flake8
uv run flake8 .
```

## License

Copyright (c) 2025 Sybex. All rights reserved.

---

## Support

For questions, issues, or to report bugs:
- Open an issue on GitHub
- Contact via X: [@sybexoracle](https://x.com/sybexoracle)

---

**Note**: This is oracle software for prediction markets. Always verify resolutions before relying on them for critical decisions.
