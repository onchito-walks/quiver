#!/usr/bin/env bash
set -euo pipefail

REPO="${QUIVER_REPO:-/home/ubuntu/src/quiver}"
TARGET="${QUIVER_BIN:-/usr/local/bin/quiver}"

if [[ ! -f "$REPO/quiver/cli.py" ]]; then
  echo "Quiver CLI not found at $REPO/quiver/cli.py" >&2
  exit 1
fi

cat > /tmp/quiver-wrapper <<EOF
#!/usr/bin/env bash
export HERMES_HOME="\${HERMES_HOME:-/srv/minio/hermes-native/.hermes}"
exec python3 "$REPO/quiver/cli.py" "\$@"
EOF

install -m 0755 /tmp/quiver-wrapper "$TARGET"
rm -f /tmp/quiver-wrapper
printf 'installed %s -> %s\n' "$TARGET" "$REPO/quiver/cli.py"
printf 'run: quiver doctor\n'
