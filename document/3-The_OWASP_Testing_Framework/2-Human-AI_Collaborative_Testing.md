# Human-AI Collaborative Testing

## Overview

"Human-AI Collaborative Testing" is a working term describing how modern security testing can integrate AI tools while retaining human expertise and judgment. It is not a new testing philosophy, but a recognition that AI tooling is accelerating certain testing activities - candidate generation, request chaining, triage, report normalization - while the fundamental skill of knowing what to test, why, and how to interpret results remains uniquely human.

This does not change the WSTG's testing categories or techniques (covered in [Section 4](../4-Web_Application_Security_Testing/README.md)). It describes how fast and how repeatably those techniques can now be executed. This section does not cover testing AI or Large Language Model (LLM) applications themselves - that is the domain of the [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/) and the [OWASP Top 10 for Large Language Model Applications](https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/). What follows is about testing *with* AI tools, not testing *of* AI systems.

## Case in Point: The HTTP Terminator

In August 2026, PortSwigger Research's "HTTP Terminator" system generated 30,000 HTTP request-smuggling vectors, tested them against authorized targets, and discovered a new vulnerability class ("shared-parser confusion") that humans had not previously published. The key insight: findings only became valuable because a human expert designed the research methodology, constrained the AI with deterministic code to prevent combinatorial explosion, and filtered the output to separate true vulnerabilities from false positives. This exemplifies human-AI collaboration: AI accelerates scale and discovery; human expertise provides strategy, validation, and accountability. See [Can AI Do Novel Security Research? Meet the HTTP Terminator](https://portswigger.net/research/http-terminator) for the full technical presentation.

## What Changes and What Doesn't

**What changes**: repeatability, automation, and speed. A human tester running one manual fuzzing run takes hours. An AI-assisted fuzzer can run millions of mutations and flag the most interesting responses in the same time. A tester manually chaining reconnaissance steps takes days. An AI system can orchestrate multiple steps and try variations in hours.

**What doesn't change**: judgment, accountability, and scope. A tester must still decide what application to test, what data to probe, what results matter, and what gets reported. The WSTG's testing framework, categories, and reporting standards remain unchanged. An AI tool cannot decide whether a finding is in scope, whether it violates the rules of engagement, or whether the business accepts the risk.

This guide covers testing *with* AI tools, not testing AI or LLM applications themselves.

## Where AI Assists Today

Modern security tools augmented by machine learning or large language models are improving specific tasks:

- **Large-scale candidate and payload generation**: Generate thousands of fuzzing payloads, SQL injection variants, or command-injection attempts. A human tester reviews which candidates are most likely to be interesting.
- **Anomaly and response triage**: Classify thousands of application responses by similarity, identify unusual behaviors (error messages, timing, status codes), flag responses that deviate from baseline.
- **Chaining and orchestration**: Automate multi-step attack sequences (e.g., enumerate users, then attempt password spray, then escalate privileges) without manual step-by-step execution.
- **Report drafting and normalization**: Generate initial findings descriptions, normalize severity ratings across tools, and structure findings in a consistent format for review.

In each case, a human tester must validate the output before treating anything as a confirmed finding or shipping it in a report.

## The Human's Role

Human expertise in AI-assisted testing includes:

- **Scope and methodology design**: defining what to test, why, and how (the research strategy from the HTTP Terminator example).
- **Tool direction and constraint**: instructing and constraining the AI tool (e.g., "test these parameters against this payload set, but stop if you exceed this response time").
- **Output validation and filtering**: reviewing AI-generated findings, discarding false positives, confirming exploitability, and assessing real-world impact.
- **Accountability**: the human tester owns the decision to report (or not report) each finding. An AI tool can suggest, but only a human can authorize.
- **Context and judgment**: understanding the application's intended behavior, business logic, and threat model - all things an AI tool cannot infer from scanning alone.

## Risks and Limitations

AI-assisted testing introduces new risks:

- **False positives and hallucinations**: An AI tool may misclassify benign responses as security issues, or suggest attack vectors that don't actually work. Always validate findings before reporting.
- **Over-trusting automated triage**: Severity or priority scores from an AI tool are suggestions, not facts. A critical business logic vulnerability might score lower than a cosmetic XSS in the algorithm.
- **Prompt injection and adversarial input**: If a testing tool ingests application responses as part of its own reasoning or prompt input, an attacker could craft responses designed to mislead the tool (e.g., embedding instructions in error messages). Validate that your tools are not vulnerable to this.
- **Tool opacity**: some AI tools are black-box (you cannot see why a finding was flagged). Prefer tools that explain their reasoning, and always validate findings by hand if you cannot understand the tool's logic.

## References

- [PortSwigger: Can AI Do Novel Security Research? Meet the HTTP Terminator](https://portswigger.net/blog/can-ai-invent-new-attack-techniques-new-research-from-james-kettle-and-portswigger-research)
- [HackerOne 2025 Hacker-Powered Security Report](https://www.hackerone.com/)
- [OWASP AI Testing Guide](https://owasp.org/www-project-ai-testing-guide/)
- [OWASP AI Exchange](https://owaspai.org/)
- [OWASP Top 10 for Large Language Model Applications](https://genai.owasp.org/initiatives/top-10-for-llm-and-genai/)
