#!/usr/bin/env bash
set -euo pipefail

ARCHIVE="$(realpath "${1:-blacktrace-target-source.tar.gz}")"
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

if [[ $EUID -ne 0 ]]; then
    echo "ERROR: Run with sudo on a clean, dedicated Ubuntu target."
    exit 1
fi

. /etc/os-release
if [[ "${ID:-}" != ubuntu || "${VERSION_ID:-}" != 24.04 ]]; then
    echo "ERROR: Ubuntu 24.04 is required."
    exit 1
fi

if [[ ! -f "$ARCHIVE" ]]; then
    echo "ERROR: Archive not found: $ARCHIVE"
    exit 1
fi

if [[ -e /opt/blacktrace ]]; then
    echo "ERROR: /opt/blacktrace already exists; refusing to overwrite it."
    exit 1
fi

tar -tzf "$ARCHIVE" | grep -qx 'target-files/app/diagnostics.py' ||
    { echo "ERROR: Diagnostics app missing from archive."; exit 1; }

tar -tzf "$ARCHIVE" | grep -qx 'target-files/requirements.txt' ||
    { echo "ERROR: requirements.txt missing from archive."; exit 1; }

tar -tzf "$ARCHIVE" | grep -qx 'target-files/app/request-interface.py' ||
    { echo "ERROR: Request interface missing from archive."; exit 1; }

tar -tzf "$ARCHIVE" | grep -qx 'target-files/challenge/setup-challenge-state.sh' ||
    { echo "ERROR: Challenge-state setup script missing from archive."; exit 1; }

tar -tzf "$ARCHIVE" | grep -qx 'target-files/systemd/blacktrace-review.service' ||
    { echo "ERROR: Review service unit missing from archive."; exit 1; }
tar -tzf "$ARCHIVE" | grep -qx 'target-files/systemd/blacktrace-review.timer' ||
    { echo "ERROR: Review timer unit missing from archive."; exit 1; }

tar -xzf "$ARCHIVE" -C "$STAGE"

python3 -m py_compile \
    "$STAGE/target-files/app/diagnostics.py" \
    "$STAGE/target-files/app/request-interface.py" \
    "$STAGE/target-files/challenge/bin/process-request.py" \
    "$STAGE/target-files/challenge/bin/review_policy.py"

command -v apt-get >/dev/null
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y python3-flask

getent group bt-operator >/dev/null ||
    groupadd --system bt-operator

id bt-operator >/dev/null 2>&1 ||
    useradd --system --gid bt-operator --home-dir /nonexistent \
        --shell /usr/sbin/nologin bt-operator

id bt-player >/dev/null 2>&1 ||
    useradd --create-home --shell /bin/bash bt-player

if id -nG bt-player | tr ' ' '\n' | grep -Eq '^(sudo|lxd|adm)$'; then
    echo "ERROR: bt-player has an administrative group."
    exit 1
fi

install -d -o root -g root -m 0755 /opt/blacktrace
cp -a "$STAGE/target-files/app" /opt/blacktrace/
cp -a "$STAGE/target-files/challenge" /opt/blacktrace/
chmod 0755 /opt/blacktrace/challenge/setup-challenge-state.sh

install -d -o root -g bt-operator -m 2770 \
    /var/lib/blacktrace/inbox /var/log/blacktrace

printf '%s\n' '{"ticket":"BT-204","action":"review"}' \
    > /var/lib/blacktrace/inbox/request.json
chown bt-operator:bt-operator /var/lib/blacktrace/inbox/request.json
chmod 0640 /var/lib/blacktrace/inbox/request.json
printf '%s\n' '{"ticket":"BT-204","action":"review"}' \
    > /var/lib/blacktrace/inbox/README.txt
chown root:root /var/lib/blacktrace/inbox/README.txt
chmod 0644 /var/lib/blacktrace/inbox/README.txt

chown -R root:root /opt/blacktrace
chmod 0755 /opt/blacktrace/challenge/bin/process-request.py
chmod 0755 /opt/blacktrace/challenge/bin/review_policy.py
chown -R root:root /opt/blacktrace/app
chmod 0644 /opt/blacktrace/app/workflow/maintenance.conf

# Initialize the protected root-proof object and challenge directories.
 /opt/blacktrace/challenge/setup-challenge-state.sh

cat > /etc/systemd/system/blacktrace-diagnostics.service <<'UNIT'
[Unit]
Description=Project BlackTrace Diagnostics
After=network.target

[Service]
Type=simple
User=bt-operator
Group=bt-operator
WorkingDirectory=/opt/blacktrace/app
ExecStart=/usr/bin/python3 /opt/blacktrace/app/diagnostics.py
Restart=on-failure
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
UNIT

install -m 0644 "$STAGE/target-files/systemd/blacktrace-review.service" \
    /etc/systemd/system/blacktrace-review.service
install -m 0644 "$STAGE/target-files/systemd/blacktrace-review.timer" \
    /etc/systemd/system/blacktrace-review.timer

cat > /etc/systemd/system/blacktrace-request-interface.service <<'UNIT'
[Unit]
Description=BlackTrace Maintenance Request Interface
After=network.target

[Service]
Type=simple
User=bt-operator
Group=bt-operator
WorkingDirectory=/opt/blacktrace/app
ExecStart=/usr/bin/python3 /opt/blacktrace/app/request-interface.py
Restart=on-failure
RestartSec=3
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
UNIT

systemctl daemon-reload
systemctl enable --now blacktrace-diagnostics.service
systemctl enable --now blacktrace-request-interface.service
# Deliberately leave the privileged review timer disabled until end-to-end validation.

echo "PASS: BlackTrace files and diagnostics service installed."
echo "NOTE: The privileged review workflow remains disabled."
echo "NOTE: This installer does not yet create the intended escalation path."
