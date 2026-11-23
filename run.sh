#!/usr/bin/env bash
set -e

# Base directory
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$BASE_DIR"

# Virtual environment python binary
PYTHON_BIN="$BASE_DIR/odoo-venv/bin/python3"
ODOO_BIN="$BASE_DIR/odoo/odoo-bin"
CONFIG_FILE="$BASE_DIR/odoo.conf"

if [ ! -f "$PYTHON_BIN" ]; then
    echo "Error: Virtual environment python not found at $PYTHON_BIN"
    echo "Please ensure odoo-venv is set up."
    exit 1
fi

if [ ! -f "$ODOO_BIN" ]; then
    echo "Error: Odoo executable not found at $ODOO_BIN"
    exit 1
fi

# Check if PostgreSQL is listening on port 5432
if ! "$PYTHON_BIN" -c "import socket; s = socket.socket(); s.settimeout(1); exit(0 if s.connect_ex(('localhost', 5432)) == 0 else 1)" 2>/dev/null; then
    echo "=================================================="
    echo "⚠️  PostgreSQL is NOT running on localhost:5432!"
    echo ""
    echo "Start it using Docker Compose:"
    echo "  sudo docker compose up -d"
    echo ""
    echo "Or allow your user to run docker without sudo:"
    echo "  sudo usermod -aG docker \$USER"
    echo "  newgrp docker"
    echo "  docker compose up -d"
    echo "=================================================="
    echo ""
fi

echo "=================================================="
echo "Starting Odoo 18.0..."
echo "Configuration: $CONFIG_FILE"
echo "Web URL:       http://localhost:8069"
echo "=================================================="

exec "$PYTHON_BIN" "$ODOO_BIN" -c "$CONFIG_FILE" "$@"
