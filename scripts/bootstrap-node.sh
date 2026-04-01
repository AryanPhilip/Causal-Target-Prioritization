#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOLS_DIR="${ROOT_DIR}/.tools"
NODE_VERSION="${NODE_VERSION:-v20.20.2}"
NODE_ARCHIVE="node-${NODE_VERSION}-darwin-arm64.tar.gz"
NODE_URL="https://nodejs.org/dist/latest-v20.x/${NODE_ARCHIVE}"

mkdir -p "${TOOLS_DIR}"
cd "${TOOLS_DIR}"

if [ ! -f "${NODE_ARCHIVE}" ]; then
  curl -fsSLO "${NODE_URL}"
fi

if [ ! -d "node-${NODE_VERSION}-darwin-arm64" ]; then
  tar -xzf "${NODE_ARCHIVE}"
fi

ln -sfn "node-${NODE_VERSION}-darwin-arm64" node

echo "Repo-local Node installed at ${TOOLS_DIR}/node"
echo "Add it to PATH with:"
echo "  export PATH=\"${ROOT_DIR}/.tools/node/bin:\$PATH\""
