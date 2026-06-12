# Scoring Model

The scoring model is intentionally simple and explainable.

## Signals

- Relevance: repository name, description, language, and topics match the query.
- Stars: adoption signal, useful but never enough by itself.
- Activity: recent `updated_at` values are better than stale repositories.
- Language fit: direct match to the preferred language.
- License clarity: repositories with a license are easier to adopt.
- Risk: archived or disabled repositories are penalized.

## Why Not Stars Alone?

A high-star project can still be the wrong choice if it is stale, too broad, missing a license, or mismatched with the user's goal.

The goal is to help the user decide:

> Should I learn, install, compare, or avoid this repository?

## Future Improvements

- Release cadence
- Issue closure rate
- Contributor diversity
- Documentation quality
- Package ecosystem signals
- Security advisories
