AUDITCHAIN-AI: AI Governance Plane for Autonomous Sub-Agents

AuditChain-AI serves as enterprise-grade AI governance system that provides audit trails and overrides for autonomous sub-agents (HR, Dev, Finance, Marketing). We use Groq LLM inference, Vectorize Hindsight persistent memory, and an Ed25519 cryptographic hash ledger to ensure fidelity and guardrails across autonomous AI actions.


Features:::
Autonomous Agent Sandbox with Real-Time Interception & Composite Risk Scoring:
Agent activity across functions (HR, Engineering, Finance, Marketing) are intercepted and scored in real-time with customizable guardrails
Persistent Hindsight Memory for Continuous Learning:
Vectorize Hindsight stores historical agent performance data to enable evolving risk profiles and improved decision-making
Security & Guardrail Envelopes:
Detect and block attempts at prompt injection, secret key exposure (`sk_live_...`), or inappropriate micro-budget allocation attempts
Two-way Human Bargaining Channel:
Admins may engage in negotiation-style conversation to request justification, ask for itemized costs, or use auto-approve budget tolerances
Ed25519 Cryptographic Signing & Audit Trail:
All decisions are digitally signed and stored in an immutable ledger with SHA-256 hashing for complete auditability


TECH STACK:
UI / Dashboard: Streamlit
LLM Engine: Groq (llama-3.3-70b-versatile)
Persistent Memory: Vectorize Hindsight API
Cryptography: Ed25519 Signature Ledger & Cryptographic Hashing
Data / Analytics: Python, Pandas, Pydantic



Quickstart:
```bash
# Clone the repository
git clone [https://github.com/YOUR_GITHUB_USERNAME/AuditChain-AI.git](https://github.com/YOUR_GITHUB_USERNAME/AuditChain-AI.git)
cd AuditChain-AI
# Install dependencies
pip install -r requirements.txt
# Configure environment
echo "GROQ_API_KEY=your_groq_key_here" > .env
# Launch Dashboard
streamlit run app.py
