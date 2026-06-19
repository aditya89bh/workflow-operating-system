"""Allow running the CLI via ``python -m workflow_os``."""

from workflow_os.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
