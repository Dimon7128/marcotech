#!/usr/bin/env bash
# sync-github-vars.sh — push Terraform outputs to GitHub repo
# Variables (non-secret config) and Secrets (credentials), so the
# CI/CD workflows can read them as ${{ vars.X }} / ${{ secrets.X }}.
#
# Why this exists:
#   Terraform already knows ECR_REGISTRY, EC2 instance IDs/hosts, the
#   region, and the deploy role ARN. Re-typing these into the GitHub
#   UI is error-prone and goes stale on every `terraform destroy && apply`.
#   This script is the single command that re-syncs everything from
#   Terraform's source of truth.
#
# Prerequisites:
#   1. `terraform apply` has been run in this directory (so outputs exist).
#   2. `gh auth login` was completed once on this machine. Verify with:
#        gh auth status
#   3. AWS_PROFILE is set (or default profile works) so `terraform output`
#      can read state — only needed if your backend requires AWS auth.
#      For a local-state setup like this one, no AWS auth is needed for
#      `terraform output` itself.
#   4. `jq` is installed (Homebrew: `brew install jq`).
#
# Usage:
#   cd Etgar/food-tier-app/infra
#   ./sync-github-vars.sh                       # auto-detect repo from git remote
#   ./sync-github-vars.sh Dimon7128/marcotech   # explicit owner/repo
#
# Idempotent: re-run whenever Terraform outputs change.

set -euo pipefail

# ---------------------------------------------------------------------------
# 1. Resolve the target GitHub repository (owner/name).
# ---------------------------------------------------------------------------
REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || true)}"
if [ -z "${REPO:-}" ]; then
  echo "ERROR: could not determine GitHub repo." >&2
  echo "  Pass it explicitly:  $0 <owner>/<repo>" >&2
  exit 1
fi
echo "==> Target repo: $REPO"

# ---------------------------------------------------------------------------
# 2. Sanity-check tooling so we fail fast with a useful message.
# ---------------------------------------------------------------------------
for cmd in terraform gh jq; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "ERROR: required command '$cmd' is not on PATH." >&2
    exit 1
  fi
done

# ---------------------------------------------------------------------------
# 3. Sync the Variables bundle (non-secret config). `gh variable set` is
#    idempotent: it creates the variable if missing, updates otherwise.
# ---------------------------------------------------------------------------
echo "==> Pushing GitHub Actions Variables (non-secret config)..."
terraform output -json github_actions_variables \
  | jq -r 'to_entries[] | [.key, .value] | @tsv' \
  | while IFS=$'\t' read -r KEY VAL; do
      gh variable set "$KEY" --repo "$REPO" --body "$VAL"
      echo "    set var:    $KEY = $VAL"
    done

# ---------------------------------------------------------------------------
# 4. Sync the Secrets bundle (credentials). `gh secret set` is also
#    idempotent. Values are POSTed encrypted and never echoed back, so we
#    deliberately don't print them.
# ---------------------------------------------------------------------------
echo "==> Pushing GitHub Actions Secrets (credentials)..."
terraform output -json github_actions_secrets \
  | jq -r 'to_entries[] | [.key, .value] | @tsv' \
  | while IFS=$'\t' read -r KEY VAL; do
      printf '%s' "$VAL" | gh secret set "$KEY" --repo "$REPO" --body -
      echo "    set secret: $KEY = (masked)"
    done

echo "==> Done. Verify in https://github.com/$REPO/settings/variables/actions"
