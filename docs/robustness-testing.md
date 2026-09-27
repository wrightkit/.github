# Robustness testing

This document defines how WrightKit tests components against hostile or
pathological input. Load it when a change affects how a parser, compiler,
analyzer, language service, protocol handler, or agent-facing tool handles
malformed, extreme, or adversarial input, or when adding fuzzing.

It is part of the [testing policy](testing-policy.md), whose core principles
also apply, including observable failures and negative-path coverage.

## Test robustness adversarially

Parsers, compilers, analyzers, language services, protocol handlers, and
agent-facing tools should be tested against hostile or pathological input where
relevant. Useful classes include:

- deep nesting;
- unexpected end-of-file at syntax boundaries;
- recursive or cyclic imports/includes;
- recursive macro expansion;
- large arrays or strings;
- extreme numeric literals;
- Unicode and encoding boundaries;
- duplicate declarations or identities;
- missing mappings or catalog entries;
- malformed external/process responses;
- resource limits and interruption behavior.

User-controlled input must not cause an uncontrolled panic, abort, hang, or
fabricated success result. Explicitly documented resource exhaustion or
unsupported behavior is acceptable when surfaced deterministically.

## Fuzzing

Fuzzing is encouraged for parsers, serializers, protocol boundaries, and other
high-input-space components when it adds meaningful coverage beyond hand-written
cases.
