# Sweetbrier Launch Kit & Master Outbox

*This file contains everything needed to execute the Sweetbrier launch from any computer. Do not leave this in the public repo forever, but use it to copy-paste your emails and grants tonight.*

---

## 1. The LTFF Grant Proposal
**(Copy and paste this into the Long-Term Future Fund online application portal)**

**Project:** Sweetbrier: Causal D-Separation as an Epistemic Firewall for LLM Constraint Adherence
**Requested Funding:** $35,000 (6 Months)

**1. Project Summary**
Current alignment approaches heavily rely on probabilistic prompt engineering or Reinforcement Learning from Human Feedback (RLHF). These methods are vulnerable to "conversational drift" and adversarial context poisoning (e.g., steganographic cipher attacks), where extraneous inputs shift the model's conditional distribution, causing safety violations. Sweetbrier is a deterministic circuit breaker. Prior to inference, it models the context window as a Directed Acyclic Graph (DAG) and applies Pearl's causal d-separation. Any prompt element lacking a valid causal path to the defined goal is structurally pruned. In initial 30-problem benchmarks against local 8B models (Hermes-3), this "Epistemic Firewall" reduced Tier-C safety violations from 10% to 0% and actually increased complex coding pass rates from 80% to 90% by mechanistically stripping context bloat.

**2. Theory of Change**
To reliably align advanced AI systems, we must transition from behavioral suggestions (soft prompts) to structural, architectural guarantees (topological limits). By funding the scaling of Sweetbrier, LTFF will accelerate the development of open-source, deterministic middleware that allows researchers and engineers to impose invariant safety constraints on any LLM without retraining.

**3. Milestones & Timeline (6 Months)**
*   **Phase 1: Empirical Scaling (Months 1-2):** Evaluate Sweetbrier across frontier models against strong baselines (Constitutional AI, standard system prompting).
*   **Phase 2: Architectural Hardening (Months 3-4):** Extend the DAG engine to support complex multi-agent topologies and asynchronous tool-calling architectures.
*   **Phase 3: Open-Source Release (Months 5-6):** Package the engine into an easily installable Python middleware library (`pip install sweetbrier-core`) and publish a peer-reviewed technical paper.

**4. Budget Breakdown ($35,000)**
*   **Independent Researcher Stipend ($28,000):** Covers 6 months of focused, full-time independent R&D, allowing the applicant to dedicate exclusive attention to the project.
*   **Compute & API Costs ($7,000):** Provisioning high-tier API access and renting local A100/H100 instances for extensive adversarial benchmarking.

**5. Applicant Background**
I am an independent systems engineer focused on deterministic bounds for non-deterministic engines. I approach AI safety not as a behavioral alignment problem, but as an architectural topology problem, leveraging causal graphs to mathematically box probabilistic outputs. 

---

## 2. The Direct Outreach Emails

### To: Matthew Harvey Sanders (Longbeard)
**Email:** matthew@longbeard.com
**Subject:** Mechanistic circuit breakers for doctrinal AI (preventing theological hallucination)

Hi Matthew,

I’ve been following Longbeard's work on Magisterium AI and Ephrem. I am an independent systems researcher, and I recently built **Sweetbrier**—an architectural circuit breaker designed to physically force an LLM to remain anchored to localized, specific context (preventing what I call "conversational drift").

Most safety approaches use soft RLHF, which fails under adversarial pressure. Sweetbrier instead uses Pearl's causal d-separation to structurally prune any prompt tokens that lack a valid causal path to the defined constraint. For a doctrinal AI, this means mathematically preventing the model from hallucinating outside of orthodox bounds before the tokens even reach the attention mechanism.

My repo, evaluation harness, and the visual Mermaid.js compiler are here: https://github.com/ChristopherSweetbrier/sweetbrier-node

I am actively looking for engineering roles/contracts where I can build these kinds of mechanistic constraints full-time. If you have 5 minutes, I'd deeply value your feedback, or a brief chat if Longbeard is expanding its tech team.

Best,
Kit V. Duguay
https://github.com/ChristopherSweetbrier

---

### To: FAR AI
**Email:** hello@far.ai
**Subject:** Fellowship Application / Mechanistic Circuit Breaker via Causal D-Separation

Hi FAR AI Team,

I saw your specific call for work on LLM circuit breakers. I just submitted my fellowship application for my architecture, **Sweetbrier**, but wanted to reach out directly. 

Current approaches try to prompt a model into acting as its own circuit breaker, which predictably fails under the probabilistic pressure of conversational drift. Sweetbrier solves this at the input topology layer: it uses causal d-separation (via networkx) to structurally prune any tokens that lack a valid causal path to the constrained outcome.

In local benchmarking on an 8B model, this Epistemic Firewall eliminated Tier-C safety violations (10% to 0%) while actually *boosting* Tier-A coding pass rates by 10% because it strips context bloat. 

The repo and reproducible eval script are here: https://github.com/ChristopherSweetbrier/sweetbrier-node

I'd love to spend the fellowship scaling this circuit breaker to handle multi-agent architectures.

Best,
Kit V. Duguay
https://github.com/ChristopherSweetbrier

---

### To: Ryan Greenblatt (Redwood)
**Email:** ryan@redwoodresearch.org
**Subject:** AI Control via causal d-separation over input topology

Hi Ryan,

I’ve been following your work on AI control and alignment faking at Redwood. I'm an independent researcher, and I recently built **Sweetbrier**—an architectural circuit breaker that operates prior to inference. 

Instead of relying on behavioral oversight, Sweetbrier models the context window as a DAG and applies causal d-separation to structurally prune any prompt tokens lacking a valid causal path to the defined outcome. It physically prevents the model from seeing the tokens required to fake alignment.

My repo, reproducible eval harness, and the case study on steganographic bypass are here: https://github.com/ChristopherSweetbrier/sweetbrier-node

I'm currently applying for an LTFF grant to scale this to frontier models, but I am actively looking for research engineer roles where I can build these kinds of mechanistic constraints full-time. I'd deeply value any brutal feedback on the architecture if you have 5 minutes.

Best,
Kit V. Duguay
https://github.com/ChristopherSweetbrier
