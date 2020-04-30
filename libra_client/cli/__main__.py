import sys

try:
    from libra_client.cli.main import main
except ImportError:
    # Failed to import our package, which likely means we were started directly
    # Add the additional search path needed to locate our module.
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
    from libra_client.cli.main import main

sys.exit(int(main() or 0))
