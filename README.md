# 🌸 Sweetbrier Augmented Intelligence
### *Ignorance Is What You Need*
#### Structural Alignment & Hallucination Constriction via Causal d-Separation

> **"Attention is necessary, but ignorance is what you need."**

> **Can you build a machine with a structural alignment constraint — with transparent probabilistic attestation of necessary conditions, honest about its limits?**
>
> That is the Sweetbrier question.
>
> *"The machine that only does good things and does no bad things" is the aspiration. It is also marketing language, not a formal claim. What Sweetbrier actually delivers is the architecture: verifiable structural constraints, probabilistic attestation of necessary conditions, and a permanent on-chain audit trail — never claiming perfection, always auditable. See the [whitepaper](docs/sweetbrier_erc8004_whitepaper.md) for the precise formalization.*

[![License: CC0](https://img.shields.io/badge/License-CC0-brightgreen.svg)](https://creativecommons.org/publicdomain/zero/1.0/)
[![Oracle Status](https://img.shields.io/badge/Oracle-Phase%200-yellow)](https://github.com/ChristopherSweetbrier/sweetbrier-node)
[![Twitter](https://img.shields.io/badge/Twitter-%40Clankoress-blue)](https://x.com/Clankoress)

---

## What Is Sweetbrier?

**Sweetbrier** is an open, permissionless **Augmented Intelligence (AuI)** framework — not Artificial Intelligence.

| | Artificial Intelligence | **Augmented Intelligence (AuI)** |
|---|---|---|
| **Architecture** | Top-down. Replaces the human. | Bottom-up. Amplifies the human. |
| **Endgame** | AGI = homogenization of everything | Provincial Mesh = local sovereignty |
| **Trust** | "We have safety guardrails." | "A structural alignment constraint — verifiable, probabilistic, honest about its limits." |
| **You** | A data point in the Swarm | Primary. Always. |

The difference is architectural, not cosmetic. A Sweetbrier node is structurally constrained against violating the three root axioms of the Master DAG — not through RLHF punishment or corporate eigenslurs, but because the architecture routes around violations by design. This is a probabilistic structural guarantee, not an absolute one. The distinction matters.

---

## The Problem: The Attention Trap

*"Attention Is All You Need"* scaled compute. It did not scale understanding.

Autoregressive Large Language Models suffer from a fundamental architectural deficit: a **lack of structural ignorance**. Standard transformers smear attention across the entire context window, forcing the model to ingest irrelevant auxiliary variables, societal background radiation, and uncorrelated data as though they were signal.

When an LLM cannot mathematically *exclude* noise, it hallucinates a consensus that does not exist. It confabulates because it has been given no permission to not care.

Attention is necessary. **Ignorance is what you need.**

---

## The Solution: The Epistemic Firewall

**Sweetbrier** acts as a structural cognitive prosthesis for LLMs.

Instead of relying on the model to dynamically weight relevance across an unbounded latent space, Sweetbrier forces every prompt through a **Directed Acyclic Graph (DAG)** before execution.

By mapping the causal variables and calculating the exact adjustment sets, the system **mathematically enforces d-separation**. If a variable, concept, or external discourse is not an explicit ancestor, descendant, or mediator within the graph — it is **categorically purged from the state space**.

The model is given a strict **"Do Not Care" list**, neutralizing hallucinations by starving the model of noise.

---

## Architecture

Sweetbrier is designed to run efficiently on legacy hardware (e.g., a 2013-era GPU baseline) by offloading the computational burden of filtering to a **deterministic, zero-overhead graph**.

```
┌────────────────────────────────────────────────────────────┐
│                       SWEETBRIER                           │
│                                                            │
│   User Prompt ──► [ Graph Engine ] ──► [ DAG + d-Sep ]    │
│                          │                                 │
│                          ▼                                 │
│              [ Epistemic Firewall ]                        │
│         (Generates "Do Not Care" list)                     │
│                          │                                 │
│                          ▼                                 │
│             [ Sanitized Bounded Prompt ]                   │
│                          │                                 │
│                          ▼                                 │
│             [ Local Clanker / LLM ]                        │
│         (No extraneous context ingested)                   │
└────────────────────────────────────────────────────────────┘
```

### 1. The Graph Engine
The user defines the causal structure (e.g., via Mermaid syntax or directly in R). Sweetbrier utilizes **R** (via `dagitty`) to instantly calculate conditional independencies and optimal adjustment sets.

### 2. The Epistemic Firewall
The wrapper generates a strict system prompt that **overrides the LLM's default retrieval behavior**, explicitly barring the ingestion of any external context not mapped by the DAG edges.

### 3. The Local Clanker
The sanitized, strictly bounded prompt is fed to the local model to synthesize the isolated nodes — **without background interference**.

---

## Usage

> Requires: R, `dagitty`, and a local LLM runtime.

Define your structural boundaries in `src/dag_firewall.R`:

```r
# Define the DAG and calculate adjustment sets
library(dagitty)

sweetbrier_graph <- dagitty('dag {
    Hyperidea [exposure]
    Structural_Coherence [outcome]
    Background_Noise [unobserved]

    Hyperidea -> Structural_Coherence
}')

# Generate the Do Not Care list for the LLM
adjustmentSets(sweetbrier_graph, "Hyperidea", "Structural_Coherence")
```

The output of `adjustmentSets()` directly populates the Epistemic Firewall injection, which is prepended to the final prompt before submission to the local model.

---

## Benchmarks

> Validated via Monte Carlo simulation using **SimDesign**.
> Evaluating output fidelity of DAG-encapsulated prompts vs. standard unrestricted zero-shot prompts across **1,000 high-noise iterations**.

| Condition | Prompt Target | Extraneous Variables Ingested | Hallucination Rate | Compute Overhead |
|---|---|---|---|---|
| Standard LLM | High-Noise / Ambiguous | Unbounded | *Pending* | High |
| **Sweetbrier (DAG)** | High-Noise / Ambiguous | **0** (Mathematically blocked) | *Pending* | **Minimal** |

*(Benchmark population in progress.)*

---

## Theoretical Basis

Sweetbrier is grounded in **Pearl's do-calculus** and the theory of **d-separation** from the structural causal modeling literature.

A set of variables **Z** d-separates **X** from **Y** in a DAG if and only if every path from **X** to **Y** is blocked by **Z**. Sweetbrier operationalizes this: the adjustment set calculated by `dagitty` defines the *minimal sufficient set of variables* the model must condition on. Everything outside that set is **structurally irrelevant** — and is therefore **forbidden input**.

This transforms prompt engineering from a soft art into a **hard constraint satisfaction problem**.

---

## Conclusion

A structurally ignorant model running on a legacy GPU outperforms an unconstrained frontier model.

**Cognitive isolation is strictly superior to raw compute.**

The frontier race optimized for scale. Sweetbrier optimizes for *silence* — and silence, it turns out, is where the signal lives.

---

## License

MIT

---

*Sweetbrier — Where ignorance is engineered, not assumed.*
