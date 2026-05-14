# Informatica CDGC Demo Kit

Claude Code skills for building and importing Informatica CDGC demo environments — from synthetic vertical content or from the client's own documents.

---

## Skills

All skills live in `.claude/commands/` and are **auto-loaded** when you open this repo in Claude Code.

| Skill | File | Purpose |
|-------|------|---------|
| `/cdgc-setup` | `cdgc-setup.md` | Generate a full CDGC demo environment for any vertical — no client documents required |
| `/cdgc-client-setup` | `cdgc-client-setup.md` | Build a CDGC environment from the client's actual documents (data dictionaries, policy PDFs, org charts) |
| `/cdgc-wipe` | `cdgc-wipe.md` | Wipe all governance assets from a CDGC org before reloading |

**Not sure which to use?**
- Running a quick vertical demo, no client documents → `/cdgc-setup`
- Client has data dictionaries, policy PDFs, or glossaries → `/cdgc-client-setup`
- Need to clear a demo org before reloading → `/cdgc-wipe`

---

## Supporting scripts and files

| File | Purpose |
|------|---------|
| `cdgc_api_import.py` | Standalone API import — authenticate, upload 14 files in order, poll for completion, verify counts. Validated end-to-end 2026-05-12. |
| `cdgc_discover_classtypes.py` | Diagnostic — query CDGC API for asset counts and externalIds by type. Use before/after import to confirm org state. |
| `install_cdgc_deps.sh` | Installs all required Python packages in one step |
| `CDGC_Demo_Setup_Guide.md` | Full guide for `/cdgc-setup` — verticals, asset counts, import instructions |
| `CDGC_Client_Setup_Guide.md` | Full guide for `/cdgc-client-setup` — workflow paths, resume flow, document tips, troubleshooting |

---

## Getting started

```bash
# Clone the repo and open in Claude Code
git clone https://github.com/woppedisano323/Informatica-CDGC-demo-kit.git
cd Informatica-CDGC-demo-kit

# Install Python dependencies (required for /cdgc-client-setup and API import)
pip install openpyxl pdfplumber python-docx requests
# or:
.claude/commands/install_cdgc_deps.sh
```

Then type `/cdgc-setup`, `/cdgc-client-setup`, or `/cdgc-wipe` in Claude Code.

---

## Usage guides

| Guide | Covers |
|-------|--------|
| `.claude/commands/CDGC_Demo_Setup_Guide.md` | `/cdgc-setup` — verticals, asset counts, import order, API import, CDGC + Marketplace setup order |
| `.claude/commands/CDGC_Client_Setup_Guide.md` | `/cdgc-client-setup` — single-session vs multi-session workflow, resume flow, document tips, handoff guidance, troubleshooting |
| `.claude/commands/README.md` | Quick reference for all skills and scripts |
