Unreleased
-------------------
- CI runs pylint and unit tests on Python 3.12 and 3.13, on current actions; pylint is `>=4.1,<5`.
- Remove the PyPI publish workflow. This fork is installed from git tags, never from PyPI.

1.1.4 (2026-08-03)
-------------------
First gopuff release tag (`v1.1.4`, on merge commit `5ac50a48`). Covers everything since upstream 1.1.2:
- Python 3.12 support: `requests` and `singer-python` unpinned, the singer-python fork swapped for upstream (1.1.3).
- Quieter INFO logging for long-running syncs, and METRIC HTTP logs suppressed under Meltano (`8d1390d`, `94fcfbf`, `a0cc902`).

1.1.2 (2021-03-16)
-------------------
- Fix missing elements for streams without ordered response

1.1.1 (2021-02-23)
-------------------
- Fix wrong JSON parsing of state.json

1.1.0 (2021-02-22)
-------------------
- Transforms stringified JSONs to JSON objects
- Enable streams to by synced since the last bookmark or start_date with query parameter
- Get more fields for events stream

1.0.2 (2021-01-21)
-------------------
- Fix publishing to PyPI

1.0.1 (2021-01-19)
-------------------
- Fix UsageRecords and UsageTriggers schemas
- Fix pagination for Account subresources

1.0.0 (2021-01-12)
-------------------

- Add programmable chat schemas and streams
- Add taskrouter streams

0.0.1 (2020-10-23)
-------------------

- Initial fork of singer-io/tap-twilio 0.0.1
