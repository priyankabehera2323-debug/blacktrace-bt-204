#!/usr/bin/env bash
set -euo pipefail

PLAYER="bt-player"

if id "$PLAYER" >/dev/null 2>&1; then
    echo "Player account already exists: $PLAYER"
else
    sudo useradd --create-home --shell /bin/bash "$PLAYER"
    echo "Created unprivileged player account: $PLAYER"
fi

echo
echo "Account details:"
id "$PLAYER"

echo
echo "Review the groups above before using this account."
echo "Do not add the player to sudo, lxd, or other administrative groups."
