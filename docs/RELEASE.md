# Release packaging

See the [GitHub releases](https://github.com/Mingbash/upwork-skills/releases) for the source and skill archives.

The user confirmed Kudrat Kurban as the public MIT copyright attribution for this original package. Root and independently installed skill copies carry that notice. The package includes links and references to third-party work, not copies of that work. The current package audit found no third-party code, articles, transcripts, client records or vendor assets requiring a separate redistribution license. Keep the source links and recheck this inventory if future content is imported.

Build release archives with `python3 scripts/package_release.py --out build`. Publish only artifacts with a reviewed file manifest/checksum. Source exports exclude .git, build artifacts, user workspaces and agent evaluation logs. Never publish private audit snapshots from the surrounding delivery directory.

The source hash manifest records the starting files without local machine paths. External inputs are referenced as links: three public Upwork skills, an Upwork guide and automation rule, and practitioner discussions. These sources informed selection and critique of methods; they are not copied into this package. A text comparison against the three linked public skill entrypoints found no shared ten-word passage in the corresponding candidate entrypoints before the public copy edit. This is a targeted check, not a proof about every possible source. The README quotes the commissioning user’s own instructions; synthetic examples replace real customer material. PyYAML is an optional external dependency, not vendored code.

The confirmed public MIT notice is `Copyright (c) 2026 Kudrat Kurban`. `python3 scripts/check_release.py --public` checks the package for release markers; it does not establish legal ownership automatically. Claude Code runtime testing is outside this release scope at the user’s request, so no Claude Code behavior claim is made.
