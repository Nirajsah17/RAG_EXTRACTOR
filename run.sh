#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

export PYTHONPATH="$ROOT_DIR/src"

usage() {
  cat <<EOF
Usage: $0 {test|run} [args]

Commands:
  test            Validate Python syntax and run the CLI help command.
  run <pdf_path>  Run the ingestion pipeline against a PDF file or directory.

Examples:
  $0 test
  $0 run ./data/raw/myfile.pdf
EOF
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

command="$1"
shift

case "$command" in
  test)
    echo "Running syntax check..."
    find "$ROOT_DIR/src" -name '*.py' | sort | xargs python3 -m py_compile
    echo "Syntax check passed."

    echo "Running CLI help..."
    python3 "$ROOT_DIR/src/main.py" --help
    echo "CLI help displayed successfully."
    ;;

  run)
    if [[ $# -ne 1 ]]; then
      echo "Error: run requires a path to a PDF file or directory."
      usage
      exit 2
    fi

    TARGET_PATH="$1"
    echo "Starting ingestion for: $TARGET_PATH"
    python3 "$ROOT_DIR/src/main.py" "$TARGET_PATH"
    ;;

  *)
    echo "Unknown command: $command"
    usage
    exit 3
    ;;
esac
