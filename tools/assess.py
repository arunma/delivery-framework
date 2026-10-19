#!/usr/bin/env python3
"""Assess a repository and write the delivery profile: surfaces, track, tier, risk flags, and which
framework phases are on, off or swapped.

    python3 tools/assess.py [REPO] [--tier S|M|L] [--track brownfield|greenfield|adopt-midway]
                            [--surface ui|api|data|cli|infra|ml ...] [--flag NAME ...] [--stdout]

Writes REPO/.delivery/profile.json and REPO/.delivery/PROFILE.md (or prints the JSON with
--stdout). Detection is a heuristic over file names and dependency manifests; the owner confirms
or corrects it (pass --surface/--track/--tier/--flag to override). Standard library only.
"""
import argparse
import json
import pathlib
import re
import sys

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "build", "dist", ".dart_tool",
             "target", ".delivery", "graphify-out", ".idea", ".gradle", "Pods"}
SOURCE_EXT = {".py", ".js", ".jsx", ".ts", ".tsx", ".dart", ".swift", ".kt", ".java", ".go", ".rs",
              ".rb", ".cs", ".sql", ".tf", ".scala", ".c", ".cpp", ".vue", ".svelte"}
MANIFESTS = ("package.json", "pyproject.toml", "requirements.txt", "pubspec.yaml", "Cargo.toml",
             "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "setup.py", "Gemfile")

# surface -> (dependency names, file-name regexes)
DEPS = {
    "ui-mobile": {"flutter", "react-native", "expo"},
    "ui-web": {"react", "react-dom", "vue", "svelte", "@angular/core", "next", "nuxt", "solid-js"},
    "ui-desktop": {"electron", "@tauri-apps/api"},
    "api": {"fastapi", "flask", "django", "starlette", "aiohttp", "grpcio", "express", "fastify",
            "@nestjs/core", "koa", "hono", "spring-boot-starter-web", "gin-gonic/gin", "labstack/echo",
            "go-chi/chi", "gorilla/mux", "actix-web", "axum", "rails", "sinatra"},
    "data": {"pandas", "polars", "pyspark", "apache-airflow", "dagster", "prefect", "dbt-core",
             "great-expectations", "great_expectations", "duckdb", "apache-beam", "pyarrow"},
    "ml": {"torch", "tensorflow", "scikit-learn", "sklearn", "transformers", "onnxruntime", "xgboost",
           "lightgbm", "keras", "jax", "tflite-runtime", "coremltools"},
}
FILES = {
    "ui-mobile": [r"(^|/)AndroidManifest\.xml$", r"\.xcodeproj(/|$)", r"(^|/)Info\.plist$"],
    "ui-web": [r"(^|/)(src|app|pages|components)/.+\.(jsx|tsx|vue|svelte)$"],
    "ui-desktop": [r"(^|/)tauri\.conf\.json$"],
    "api": [r"(^|/)(openapi|swagger|asyncapi)\.(ya?ml|json)$", r"\.proto$"],
    "data": [r"(^|/)dbt_project\.yml$", r"(^|/)dags/.+\.py$", r"(^|/)(models|sql|transforms)/.+\.sql$"],
    "infra": [r"\.tf$", r"(^|/)Pulumi\.yaml$", r"(^|/)cdk\.json$", r"(^|/)Chart\.yaml$",
              r"(^|/)kustomization\.ya?ml$", r"(^|/)serverless\.ya?ml$"],
    "ml": [r"\.(onnx|tflite|mlmodel|pt|ckpt|safetensors)$"],
}
CLIENT_DEPS = {"axios", "dio", "http", "retrofit", "alamofire", "@apollo/client", "graphql-request",
               "@tanstack/react-query", "swr", "ky", "requests", "httpx", "okhttp"}
SENSITIVE = ("encrypt", "crypto", "keychain", "secure_storage", "securestore", "pii", "stripe",
             "payment", "passport", "patient", "kms", "vault", "biometric")
REGULATED = ("hipaa", "gdpr", "pci-dss", "pci dss", "sox ", "fhir", "hl7", "finra", "psd2", "ferpa")

SURFACES = {
    "ui": {"contract": "Mockup atlas: design/atlas/ (source design/atlas-src/)",
           "contract_skill": "atlas",
           "gate": "Screenshot parity by an independent reviewer (design/parity/NNN.md)",
           "e2e": "Device or browser E2E on staging (Maestro, XCUITest, Espresso or Playwright)",
           "baseline": "Screenshots of today's app (design/before/)"},
    "api": {"contract": "API contract: contracts/api/ (OpenAPI, AsyncAPI or protobuf) plus Mermaid sequence diagrams",
            "contract_skill": "contract",
            "gate": "Contract tests, consumer-driven tests and an empty or approved contract diff",
            "e2e": "API and integration tests against an ephemeral or staging environment",
            "baseline": "Recorded responses of today's endpoints on synthetic data"},
    "data": {"contract": "Data contract: contracts/data/ (schemas, data dictionary, Mermaid lineage, SLAs, freshness)",
             "contract_skill": "contract",
             "gate": "Output equals the committed answer key; data-quality checks pass; a second run reproduces it",
             "e2e": "Pipeline run on the golden dataset (synthetic data only)",
             "baseline": "Today's outputs on the golden dataset, kept as the first answer key"},
    "cli": {"contract": "Public API surface: contracts/surface/API-SURFACE.md plus usage examples",
            "contract_skill": "contract",
            "gate": "Usage examples run as tests, golden CLI output matches, semver check agrees",
            "e2e": "Golden CLI runs and doctests",
            "baseline": "Golden output of today's commands and public API listing"},
    "infra": {"contract": "Architecture diagram plus the IaC plan: contracts/infra/",
              "contract_skill": "contract",
              "gate": "Plan diff holds only the intended changes; policy checks pass (plan-only in the pilot)",
              "e2e": "IaC plan against a sandbox account; never apply in the pilot",
              "baseline": "Today's plan output and resource inventory"},
    "ml": {"contract": "Eval set with an answer key, benchmark hardware and the decision rule: contracts/eval/",
           "contract_skill": "contract",
           "gate": "Eval scores meet the decision rule on the named hardware",
           "e2e": "Eval harness on the benchmark devices or hardware",
           "baseline": "Today's eval scores on the same set"},
}
ORDER = ["ui", "api", "data", "cli", "infra", "ml"]
FLAGS = ["sensitive_data", "regulated", "multi_repo", "backend_dependencies"]


def walk(root, depth=5):
    out = []
    def rec(d, level):
        try:
            entries = sorted(d.iterdir())
        except OSError:
            return
        for e in entries:
            if e.is_dir():
                if e.name not in SKIP_DIRS and level < depth:
                    out.append(e.relative_to(root).as_posix() + "/")
                    rec(e, level + 1)
            else:
                out.append(e.relative_to(root).as_posix())
    rec(root, 0)
    return out


def dependencies(root, files):
    """{dependency name: manifest path}, from the manifests found."""
    deps = {}
    for rel in files:
        name = rel.rsplit("/", 1)[-1]
        if name not in MANIFESTS and not re.match(r"requirements.*\.txt$", name):
            continue
        text = (root / rel).read_text(errors="replace")
        found = set()
        if name == "package.json":
            try:
                j = json.loads(text)
            except ValueError:
                j = {}
            for k in ("dependencies", "devDependencies", "peerDependencies"):
                found |= set(j.get(k) or {})
            if j.get("bin"):
                found.add("<bin>")
        elif name == "pubspec.yaml":
            found |= set(re.findall(r"^\s{2}([a-z_][\w]*):", text, re.M))
            if re.search(r"^\s+flutter:\s*$", text, re.M) or "sdk: flutter" in text:
                found.add("flutter")
        elif name in ("pyproject.toml", "setup.py") or name.startswith("requirements"):
            found |= {m.lower() for m in re.findall(r"^\s*\"?([A-Za-z][\w.-]*)", text, re.M)}
            found |= {m.lower() for m in re.findall(r"[\"']([A-Za-z][\w.-]*)\s*(?:[<>=~!\[;]|[\"'])", text)}
            if re.search(r"^\[(project|tool\.poetry)\.scripts\]", text, re.M) or "console_scripts" in text:
                found.add("<bin>")
        elif name == "Cargo.toml":
            found |= set(re.findall(r"^([a-z][\w-]*)\s*=", text, re.M))
            if "[[bin]]" in text or "[lib]" in text:
                found.add("<bin>")
        else:  # go.mod, pom.xml, Gradle, Gemfile: look for known names in the text
            known = set().union(*DEPS.values(), CLIENT_DEPS)
            found |= {n for n in known if re.search(r"[\s\"'/:]" + re.escape(n) + r"[\s\"'/:@]", text)}
        for f in found:
            deps.setdefault(f, rel)
    return deps


def detect(root):
    files = walk(root)
    deps = dependencies(root, files)
    evidence = {}

    def hit(surface, why):
        evidence.setdefault(surface, [])
        if why not in evidence[surface]:
            evidence[surface].append(why)

    for key, names in DEPS.items():
        surface = key.split("-")[0]
        for n in sorted(names & set(deps)):
            hit(surface, f"{deps[n]}: {n}")
    for key, patterns in FILES.items():
        surface = key.split("-")[0]
        matched = [f for f in files if any(re.search(p, f) for p in patterns)]
        for f in matched[:3]:
            hit(surface, f"file: {f.rstrip('/')}")
    if {"ios/", "android/"} <= set(files):
        hit("ui", "dirs: ios/ and android/")
    ui_kind = next((k.split("-")[1] for k in ("ui-mobile", "ui-desktop", "ui-web")
                    if DEPS[k] & set(deps) or any(re.search(p, f) for p in FILES[k] for f in files)), None)
    if ui_kind is None and "ui" in evidence:
        ui_kind = "mobile"
    if "<bin>" in deps:
        hit("cli", f"{deps['<bin>']}: declares an executable or library entry point")
    if "go.mod" in files and "cmd/" in files:
        hit("cli", "file: go.mod with cmd/")
    manifests = [f for f in files if f.rsplit("/", 1)[-1] in MANIFESTS]
    if not evidence and manifests:
        hit("cli", f"{manifests[0]}: a package with no other surface (library)")
    sources = [f for f in files if pathlib.PurePosixPath(f).suffix in SOURCE_EXT]

    text_blobs = " ".join(f.lower() for f in files) + " " + " ".join(sorted(deps))
    readme = " ".join((root / f).read_text(errors="replace").lower() for f in files
                      if re.match(r"(README|docs/.+)\.md$", f, re.I))[:200000]
    flags = {
        "sensitive_data": any(k in text_blobs for k in SENSITIVE),
        "regulated": any(k in readme for k in REGULATED),
        "multi_repo": ".gitmodules" in files,
        "backend_dependencies": "ui" in evidence and bool(CLIENT_DEPS & set(deps)),
    }
    adopt = any(f in files for f in ("specs/", ".specify/", "SESSIONS.md"))
    track = "greenfield" if not sources else ("adopt-midway" if adopt else "brownfield")
    return {"surfaces": [s for s in ORDER if s in evidence], "ui_kind": ui_kind if "ui" in evidence else None,
            "track": track, "flags": flags, "evidence": {s: evidence[s] for s in ORDER if s in evidence}}


def phases(surfaces, track, tier, flags):
    """Every framework phase: status on/off/swapped, the skill that runs it, and why."""
    big, mid = tier == "L", tier in ("M", "L")
    contract_with = " + ".join(SURFACES[s]["contract"].split(":")[0] for s in surfaces) or "none"
    gate_with = " + ".join(SURFACES[s]["gate"].split(";")[0] for s in surfaces) or "none"

    def ph(status, skill, why, with_=None):
        d = {"status": status, "skill": skill, "why": why}
        if with_:
            d["with"] = with_
        return d

    p = {}
    p["assess"] = ph("on", "assess", "always first")
    p["bootstrap"] = ph("on" if big else "off", f"bootstrap-{track}",
                        "tier L sets the project up from scratch" if big else "tier S/M reuse the project's setup")
    p["setup"] = ph("on" if mid else "off", "bootstrap-" + track,
                    "instructions, tracker and .env" if mid else "tier S works from the ticket")
    if track == "greenfield" or not big:
        p["capture-before"] = ph("off", "capture-before", "nothing to capture" if track == "greenfield"
                                 else "tier S/M compare against the existing contract")
    elif surfaces == ["ui"]:
        p["capture-before"] = ph("on", "capture-before", "brownfield UI: screenshots of today's app")
    else:
        p["capture-before"] = ph("swapped", "capture-before", "brownfield: baseline per surface",
                                 " + ".join(SURFACES[s]["baseline"] for s in surfaces))
    p["research"] = ph("on" if big else "off", "atlas" if "ui" in surfaces else "contract",
                       "research and review before the contract" if big else "not for tier S/M")
    if not mid:
        p["contract"] = ph("off", "contract", "tier S changes no contract; escalate to M if it does")
    elif surfaces == ["ui"]:
        p["contract"] = ph("on", "atlas", "UI: the atlas is the contract", contract_with)
    else:
        p["contract"] = ph("swapped", "atlas" if "ui" in surfaces else "contract",
                           "the contract artefact is the source of truth", contract_with)
    p["decisions"] = ph("on" if mid else "off", "decisions", "decisions, open questions, glossary, discrepancies")
    p["backend-split"] = ph("on" if mid and flags["backend_dependencies"] else "off", "backend-split",
                            "a client depends on a backend" if flags["backend_dependencies"]
                            else "no client-to-backend dependency found")
    p["constitution"] = ph("on" if big else "off", "constitution", "principles for a large piece of work"
                           if big else "use the existing constitution, if any")
    p["architecture"] = ph("on" if big else "off", "architecture", "graph and diagrams" if big else "not for tier S/M")
    p["specs"] = ph("on" if mid else "off", "specify-from-atlas", "one spec per feature, citing contract ids",
                    contract_with if mid else None)
    p["verify-specs"] = ph("on" if mid else "off", "verify-specs", "coverage and cross-references")
    p["plans"] = ph("on" if mid else "off", "plan-and-tasks", "plan grounded in code, tasks by session")
    p["sessions"] = ph("on" if big else "off", "sessionize", "many sessions" if big else "tier M is one session")
    p["tracker"] = ph("on" if mid else "off", "jira-sync", "tickets and links" if mid else "the ticket exists")
    p["execution"] = ph("on", "run-session", "test-first, three layers, evidence, ask before commit")
    p["verification"] = ph("on" if surfaces == ["ui"] else "swapped", "parity-review",
                           "independent check of built output against the contract", gate_with)
    p["wave-close"] = ph("on" if big else "off", "wave-close", "after each wave" if big else "no waves")
    p["learning"] = ph("on", "wave-close", "every miss becomes a rule")
    return p


def profile(root, args):
    d = detect(root)
    surfaces = [s for s in ORDER if s in (args.surface or d["surfaces"])]
    if not surfaces:
        surfaces = ["cli"]
    track = args.track or d["track"]
    tier = args.tier or "M"
    flags = dict(d["flags"])
    for f in args.flag or []:
        flags[f] = True
    return {
        "version": 1,
        "surfaces": surfaces,
        "ui_kind": d["ui_kind"] if "ui" in surfaces else None,
        "track": track,
        "tier": tier,
        "tier_source": "owner" if args.tier else "assumed (confirm with the tiering skill)",
        "risk_flags": flags,
        "contracts": [{"surface": s, **{k: SURFACES[s][k] for k in ("contract", "gate", "e2e")}}
                      for s in surfaces],
        "phases": phases(surfaces, track, tier, flags),
        "evidence": d["evidence"],
    }


def markdown(p):
    lines = ["# Delivery profile", "",
             "Generated by `tools/assess.py`; confirmed by the owner. Every delivery skill reads "
             "`.delivery/profile.json`. Re-run `/delivery:assess` when the project changes shape.", "",
             f"- **Surfaces:** {', '.join(p['surfaces'])}" + (f" ({p['ui_kind']})" if p["ui_kind"] else ""),
             f"- **Track:** {p['track']}", f"- **Tier:** {p['tier']} ({p['tier_source']})",
             "- **Risk flags:** " + (", ".join(k for k, v in p["risk_flags"].items() if v) or "none"), "",
             "## Contract and verification per surface", "",
             "| Surface | Contract artefact | Verification gate | E2E |", "| --- | --- | --- | --- |"]
    lines += [f"| {c['surface']} | {c['contract']} | {c['gate']} | {c['e2e']} |" for c in p["contracts"]]
    lines += ["", "## Phases", "", "| Phase | Status | Skill | With | Why |", "| --- | --- | --- | --- | --- |"]
    lines += [f"| {k} | {v['status']} | `{v['skill']}` | {v.get('with', '')} | {v['why']} |"
              for k, v in p["phases"].items()]
    lines += ["", "## Evidence", ""]
    for s, ev in p["evidence"].items():
        lines += [f"- **{s}:** " + "; ".join(ev)]
    if not p["evidence"]:
        lines.append("- none found (greenfield or an empty repo): surfaces come from the owner")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--tier", choices=["S", "M", "L"])
    ap.add_argument("--track", choices=["brownfield", "greenfield", "adopt-midway"])
    ap.add_argument("--surface", action="append", choices=ORDER, help="override detection (repeatable)")
    ap.add_argument("--flag", action="append", choices=FLAGS, help="set a risk flag (repeatable)")
    ap.add_argument("--stdout", action="store_true", help="print the profile JSON; write nothing")
    a = ap.parse_args(argv)
    root = pathlib.Path(a.repo).resolve()
    if not root.is_dir():
        print(f"assess.py: {root} is not a directory", file=sys.stderr)
        return 2
    p = profile(root, a)
    text = json.dumps(p, indent=2) + "\n"
    if a.stdout:
        sys.stdout.write(text)
        return 0
    out = root / ".delivery"
    out.mkdir(exist_ok=True)
    (out / "profile.json").write_text(text)
    (out / "PROFILE.md").write_text(markdown(p))
    on = [k for k, v in p["phases"].items() if v["status"] != "off"]
    print(f"wrote {out / 'profile.json'} and PROFILE.md: surfaces {', '.join(p['surfaces'])}; "
          f"track {p['track']}; tier {p['tier']}; phases on/swapped: {', '.join(on)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
