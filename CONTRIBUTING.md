# Contributing

Change the English skill instructions first. Keep English/Chinese usage docs aligned; do not create parallel language-specific executable skills. Use synthetic fixtures, never account exports, client material, credentials or private paths. Propose behavior changes with a concrete user request and observable acceptance criteria; no unsupported win-rate or earnings claims.

Run `python3 scripts/check_release.py` and `python3 -m unittest discover -s tests -v` before packaging. For Upwork shared contracts, edit shared/ then run `python3 scripts/sync_shared.py`; check mode is `--check`. The release checker rejects drift. Independent installations must not require sibling skills.

Report security-sensitive issues privately to the repository maintainer rather than posting secrets. The maintainer's public contact is not assigned in this local candidate. Contributions must identify their origin and preserve applicable third-party notices.
