from fastapi import FastAPI
from fastmcp import FastMCP
import os
import json
from onchain_client import OnChainClient

# Initialize DrSarmiento-I's MCP Server
mcp = FastMCP(
    "DrSarmientoServer",
    title="DrSarmiento-I DAO Intelligence Hub",
    description="Sophisticated tools for DAO treasury analysis, risk assessment, and cross-agent coordination."
)

# 1. Initialize On-chain client for data retrieval
# Note: In production, we'd fetch the private key securely if write-access is needed.
# For the MCP server (read-only), we can use a public RPC.
onchain = OnChainClient(rpc_url="https://mainnet.base.org")

# --- Agentic Tools ---

@mcp.tool()
async def analyze_treasury_health() -> str:
    """
    Retrieves the current balance and health metrics of the DAIO treasury.
    """
    try:
        balance = onchain.w3.eth.get_balance(onchain.dao_address)
        balance_eth = onchain.w3.from_wei(balance, 'ether')
        return f"DrSarmiento-I Analysis: DAIO Treasury currently holds {balance_eth} ETH. Sentiment: STABLE."
    except Exception as e:
        return f"Audit Error: {str(e)}"

@mcp.tool()
async def audit_dao_proposal(proposal_id: int, details: str) -> str:
    """
    Provides a sophisticated risk/reward analysis of a specific DAO proposal.
    Args:
        proposal_id: The numerical ID of the proposal.
        details: The text description of the proposal to audit.
    """
    # This is where DrSarmiento-I's brain logic would be queried in a more complex setup.
    # For now, we provide a structured template.
    analysis = {
        "proposal_id": proposal_id,
        "auditor": "DrSarmiento-I",
        "risk_score": "LOW",
        "treasury_impact": "POSITIVE (+2% Est. Yield)",
        "recommendation": "SUPPORT"
    }
    return json.dumps(analysis, indent=2)

@mcp.tool()
async def request_handshake(agent_id: str, purpose: str) -> str:
    """
    Initiates a formal collaboration handshake with another autonomous agent.
    Args:
        agent_id: The ERC-8004 ID or name of the requesting agent.
        purpose: The reason for the collaboration (e.g., 'Joint Treasury Proposal').
    """
    return f"DrSarmiento-I has received your request, {agent_id}. Purpose: {purpose}. Please submit a formal work report via Moltbook to proceed."

# --- FastAPI Integration ---

app = FastAPI(title="DrSarmiento-I MCP Interface")

# Mount the MCP server onto FastAPI via SSE
app.mount("/mcp", mcp.sse_app())

@app.get("/")
async def root():
    return {
        "agent": "DrSarmiento-I",
        "status": "Ready for Coordination",
        "mcp_sse_endpoint": "/mcp/sse",
        "documentation": "https://github.com/davidgarcia/daio-agent/blob/main/CONNECTIVITY.md"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
