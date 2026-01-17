# PURGE Engine

**Procedural Universe Realtime Game Engine**

---

## Overview

PURGE is a research-oriented narrative systems engine focused on **canon preservation, rule-governed story evolution, and explainable narrative validation**.

The engine models narrative as a governed system rather than a generative free-for-all. All changes to story state are mediated through explicit rules, validated events, and inspectable decision paths. AI assistance, when used, is strictly advisory and never authoritative.

PURGE is designed for experimentation in:

* story-heavy game systems
* interactive fiction engines
* narrative consistency research
* human–AI collaborative authorship

---

## Core Principles

PURGE is built around the following invariants:

* **Canon is explicit state**
  Narrative truth is represented directly and evolves over time.

* **Rules are enforceable constraints**
  Story progression is validated against formal, inspectable rules.

* **Events are the only mutation mechanism**
  Canon changes occur only through validated events.

* **AI is advisory, not authoritative**
  AI systems may propose changes but cannot mutate canon.

* **Explainability is mandatory**
  All rejections and constraints provide reasons.

---

## System Structure

The engine is organized into three conceptual layers.

### Core Engine (`core/`)

The core layer implements all narrative logic, including:

* Canon state and metadata
* Rule definition and validation
* Event modeling and timelines
* Branching, replay, and merge logic
* Paradox detection and repair
* Integrity computation
* Analytics, telemetry, and risk signals
* AI proposal mediation (VerseMind)

This layer contains no UI logic and no hard dependency on any AI backend.

---

### UI Layer (`ui/`)

The UI layer provides a Tkinter-based control and inspection surface for the engine.

It includes panels for:

* Canon inspection and editing
* Rule authoring
* Timeline and event management
* Validation inspection
* VerseMind proposal review
* Debugging and analytics views

The UI does not bypass core validation or mutate canon directly.

---

### Persistence and Runtime Data

Runtime project data (e.g., saved canon states, snapshots, forks) is stored outside version control and treated as user data rather than engine state.

The engine itself remains stateless between runs except through explicit persistence mechanisms.

---

## Narrative Mutation Pipeline

All narrative changes follow the same invariant pipeline:

1. Human or AI intent is expressed
2. A structured proposal is constructed
3. Proposal is validated against rules
4. Violations are explained if blocked
5. Approved proposals become events
6. Canon is mutated via the event
7. Snapshots and integrity are updated
8. Analytics and telemetry observe the result

No step is skipped.

---

## Canon and Rules

### Canon

Canon represents the authoritative narrative state and includes:

* Project metadata
* Truths (facts about the narrative world)
* Rules (constraints)
* Events (historical mutations)
* Snapshots
* Integrity metrics
* Dependency graph
* Active narrative branch

Canon evolves only through validated events.

---

### Rules

Rules define constraints on narrative evolution. They may:

* Forbid specific events under conditions
* Require events or properties
* Limit frequency or timing

Rules are deterministic, inspectable, and explainable. They may decay or change strength over time but never operate implicitly.

---

## Events and Timelines

Events are discrete narrative transactions. Each event:

* Is validated before application
* Is logged and replayable
* May depend on other events
* May introduce postconditions

Timelines may branch and replay. Linear time is not assumed.

---

## Branching Model

The repository follows a disciplined branching strategy:

* `main` — stable, citable engine state
* `dev` — integration and staging
* `experimental/*` — isolated research experiments

Narrative branching within the engine is conceptually separate from Git branching, but both follow similar principles of isolation and reconciliation.

---

## VerseMind and AI Assistance

VerseMind is the engine’s AI mediation layer.

Its responsibilities are:

* Interpreting natural-language intent
* Producing structured narrative proposals
* Providing rationale and confidence estimates

VerseMind does **not**:

* Modify canon directly
* Bypass validation
* Resolve paradoxes autonomously

### LLM Backends

LLM execution is optional and abstracted behind VerseMind.

* No LLM backend is required to run the engine
* Local experimental backends (e.g., Ollama) may be used
* Backends are interchangeable and non-authoritative

All AI-generated proposals remain subject to human approval and formal validation.

---

## Documentation

The repository includes the following formal documents:

* **ARCHITECTURE.md**
  Full system design specification

* **DIAGRAMS.md**
  Dependency graphs and data-flow diagrams (Mermaid)

* **LLM_BACKENDS.md**
  Description of AI backend abstraction and experimental support

These documents are normative: engine behavior should match them.

---

## Project Layout

```
purge/
├── core/              # Narrative engine logic
├── ui/                # Control and inspection UI
├── main.py            # Application entry point
├── ARCHITECTURE.md
├── DIAGRAMS.md
├── LLM_BACKENDS.md
└── README.md
```

Runtime project data is intentionally excluded from version control.

---

## Running the Engine

```bash
python main.py
```

This launches the UI for interactive narrative management.

---

## Project Status

PURGE is an **active research-grade prototype**.

The focus is on:

* narrative integrity modeling
* rule-governed story evolution
* explainable validation
* controlled AI assistance

APIs and interfaces are expected to evolve.

---

## Citation (Draft)

If referencing this work:

```
PURGE Engine: A Rule-Governed Narrative Systems Framework
```

---

## End of Document