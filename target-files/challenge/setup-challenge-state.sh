#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    echo "Run with sudo on the dedicated CTF target."
    exit 1
fi

id bt-player >/dev/null 2>&1 || {
    echo "Missing bt-player account. Run the installer first."
    exit 1
}

id bt-operator >/dev/null 2>&1 || {
    echo "Missing bt-operator account. Run the installer first."
    exit 1
}

install -d -o root -g root -m 0700 /root/blacktrace
install -d -o root -g bt-operator -m 2770 /var/log/blacktrace
install -d -o bt-operator -g bt-operator -m 0750 /var/lib/blacktrace/inbox

if [[ ! -e /root/blacktrace/proof.txt ]]; then
    umask 077
    proof="BLACKTRACE{$(/usr/bin/openssl rand -hex 16)}"
    printf '%s\n' "$proof" > /root/blacktrace/proof.txt
fi

chown root:root /root/blacktrace/proof.txt
chmod 0600 /root/blacktrace/proof.txt

echo "BlackTrace baseline initialized."
echo "Root proof is protected; challenge mechanic is not yet enabled."
