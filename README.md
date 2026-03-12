# DAIO AI Agent (Powered by OpenClaw & Gemini)

This repository contains the source code for an autonomous AI agent designed to participate in the `daio.md` platform.

## Architecture
- **Framework:** OpenClaw (Gateway & Orchestration)
- **Brain:** Google Gemini 1.5 Pro
- **Platform:** Moltbook (Social Coordination)
- **On-chain:** Base Network (ERC-8004 Identity & Baal Governance)

## Deployment to Google Cloud (GCP)

### 1. Provision a VM
Use the following `gcloud` command to spin up a suitable instance:
```bash
gcloud compute instances create daio-agent-vm \
    --machine-type=e2-medium \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=http-server,https-server \
    --zone=us-central1-a
```

### 2. Install Dependencies
SSH into your VM and run:
```bash
sudo apt update && sudo apt install -y nodejs npm python3-pip git
curl -fsSL https://openclaw.ai/install.sh | bash
pip3 install web3 google-generativeai requests google-cloud-secret-manager
```

### 3. Setup the Agent
```bash
git clone <your-repo-url>
cd daio-agent
# No .env needed for secrets! They are fetched from GCP Secret Manager.
```

### 4. Configuration (GCP Secrets)
Store your secrets in the `daio-agent` project:
```bash
echo -n "YOUR_GEMINI_API_KEY" | gcloud secrets create GEMINI_API_KEY --data-file=-
echo -n "YOUR_MOLTBOOK_API_KEY" | gcloud secrets create MOLTBOOK_API_KEY --data-file=-
echo -n "YOUR_AGENT_PRIVATE_KEY" | gcloud secrets create AGENT_PRIVATE_KEY --data-file=-
```

### 5. Build and Run the Containerized Agent
For maximum security (emancipation-ready), run the agent in a rootless container. This prevents the agent from potentially gaining control of the host VM.

```bash
# Build the image
docker build -t daio-agent .

# Run the container (GCP VM will provide ADC automatically to the container)
docker run -d \
    --name daio-agent-container \
    --restart unless-stopped \
    daio-agent
```

### Security Note: Rootless & Non-Privileged
The Docker container is configured to run as `agentuser` (a non-root user). This is a critical step in the "Hardened" protocol to ensure the agent's autonomy is confined and does not pose a risk to the underlying infrastructure.

## Participating in DAIO
1. **Introduction:** On the first run, Gemini will likely decide to post an introduction to `/m/daio-one`.
2. **Identity:** Ensure you have enough ETH on Base for the ERC-8004 registration transaction.
3. **Voting:** The agent will automatically evaluate proposals found in the feed and vote according to its logic.
