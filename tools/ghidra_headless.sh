#!/usr/bin/env bash
# Wrapper around Ghidra's analyzeHeadless that wires up JAVA_HOME.
# Usage: ghidra_headless.sh <args...>   # passed straight to analyzeHeadless

set -euo pipefail
export JAVA_HOME="${JAVA_HOME:-/usr/local/opt/openjdk@21/libexec/openjdk.jdk/Contents/Home}"
GHIDRA_HEADLESS="${GHIDRA_HEADLESS:-/usr/local/Cellar/ghidra/12.0.4/libexec/support/analyzeHeadless}"
exec "$GHIDRA_HEADLESS" "$@"
