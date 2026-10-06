#!/usr/bin/env bash
#
# Fail if anything that looks like a credential is present in the commits
# being examined. Exits 0 when clean, 1 when it finds something, 2 on a
# usage or tooling error.
#
# Run by .githooks/pre-push on every push, or by hand:
#
#     scripts/check-secrets.sh              # everything reachable from HEAD
#     scripts/check-secrets.sh origin/main..HEAD
#
# Patterns are deliberately high-confidence for the token classes and
# deliberately boring for the generic ones, because a scanner that cries
# wolf gets disabled on the first false positive. Every pattern here is
# checked against this repository's full history before being added: all
# three content patterns return zero hits today, so the first line this
# ever prints is a genuine finding.
set -uo pipefail

cd "$(git rev-parse --show-toplevel)" 2>/dev/null || {
	echo "check-secrets: not inside a git repository" >&2
	exit 2
}

range="${1:-HEAD}"

# Vendor-shaped tokens: AWS, GitHub, OpenAI/Anthropic-style, Slack, Google,
# GitLab, and a JSON Web Token recognised by its double eyJ header so that
# ordinary dotted content cannot match.
HIGH_CONFIDENCE="AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|xox[baprs]-[0-9A-Za-z-]{10,}|AIza[0-9A-Za-z_-]{35}|glpat-[A-Za-z0-9_-]{20,}|eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.|-----BEGIN [A-Z ]*PRIVATE KEY-----"

# The cheap check that actually catches the common mistake: a credential
# name on the left of = or :, quoted, and long enough to be a value rather
# than a placeholder like "" or "changeme". The keyword may sit anywhere in
# the identifier, because AWS_SECRET_ACCESS_KEY and GITLAB_TOKEN are both
# real names and neither starts with the keyword. Values must be quoted:
# that is what keeps terminalToken = match[1].trim() and other ordinary
# code out of the report. Six characters minimum likewise keeps
# API_KEY_SOURCE = "env" from being a finding.
GENERIC_ASSIGN="[A-Za-z0-9_-]*(password|passwd|pwd|secret|token|api[_-]?key|apikey|private[_-]?key|client[_-]?secret|passphrase|credential)[A-Za-z0-9_-]*[[:space:]]*[:=][[:space:]]*[\"'][^\"']{6,}"

# user:password@host in a URL. Tokens in a URL path are not caught here
# because they are indistinguishable from filenames.
CRED_URL="[a-zA-Z][a-zA-Z0-9+.-]*://[^/@[:space:]]+:[^/@[:space:]]+@"

# Filenames that should never be committed. .env.example is excepted below,
# matching the exception .gitignore already carries.
SECRET_FILENAMES="(^|/)\.env(\.[^/]+)?$|(^|/)(id_rsa|id_dsa|id_ecdsa|id_ed25519)(\.[^/]+)?$|\.(pem|key|p12|pfx|jks|keystore|asc)$|(^|/)(\.netrc|\.npmrc|\.pypirc|\.pgpass|\.htpasswd|credentials|secrets?)(\.[^/]+)?$|(^|/)(\.ssh|\.aws)(/|$)"

mapfile -t revs < <(git rev-list "$range" 2>/dev/null)
if [ "${#revs[@]}" -eq 0 ]; then
	printf 'check-secrets: no commits to scan in %s\n' "$range"
	exit 0
fi

hits="$(mktemp)"
trap 'rm -f "$hits"' EXIT

# Chunks keep git grep well inside ARG_MAX however long the push gets, and
# the sha prefix is stripped so the same line found in 40 consecutive
# commits reports once instead of 40 times. The flags argument exists
# because only the generic assignment pattern wants -i: apiKey and API_KEY
# are both mistakes worth catching, while AKIA is uppercase by construction
# and folding case there would only invite base64 to trip it.
#
# Remaining arguments are pathspecs. The generic scan excludes this file,
# because SECRET_FILENAMES="..." is exactly the shape it is looking for and
# a scanner that reports itself is a scanner people learn to ignore. Only
# that one scan is restricted: the token patterns and the URL pattern still
# read this file, so a real credential pasted into it is still found.
scan_content() {
	local label="$1" flags="$2" pat="$3"
	shift 3
	local -a paths=("$@")
	local i=0 chunk out rc
	while [ "$i" -lt "${#revs[@]}" ]; do
		chunk=("${revs[@]:i:200}")
		out="$(git grep -nIE $flags "$pat" "${chunk[@]}" -- "${paths[@]}" 2>/dev/null)"
		rc=$?
		if [ "$rc" -ge 2 ]; then
			echo "check-secrets: git grep failed for pattern: $pat" >&2
			exit 2
		fi
		if [ -n "$out" ]; then
			printf '%s\n' "$out" | sed -E 's/^[0-9a-f]{40}://' | sort -u |
				sed "s|^|$label: |" >>"$hits"
		fi
		i=$((i + 200))
	done
}

scan_content "high-confidence secret" "" "$HIGH_CONFIDENCE" .
scan_content "credentialed URL" "" "$CRED_URL" .
scan_content "hardcoded credential" "-i" "$GENERIC_ASSIGN" . ":(exclude)scripts/check-secrets.sh"

f="$(git ls-tree -r --name-only "${revs[0]}" |
	grep -aE "$SECRET_FILENAMES" | grep -avE '\.env\.example$' || true)"
if [ -n "$f" ]; then
	printf '%s\n' "$f" | sed 's|^|suspicious filename: |' >>"$hits"
fi

if [ -s "$hits" ]; then
	echo "check-secrets: PUSH BLOCKED - ${#revs[@]} commit(s) in '$range' contain things that look like credentials:" >&2
	sort -u "$hits" >&2
	echo "" >&2
	echo "If a match is a false positive, it does not belong in a pattern" >&2
	echo "that this script owns - remove the offending value instead, or" >&2
	echo "stop it matching by naming it differently." >&2
	exit 1
fi

printf 'check-secrets: OK - %d commit(s) in %s\n' "${#revs[@]}" "$range"
exit 0
