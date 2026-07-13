import sys
from pathlib import Path

SRC_PATH = Path(__file__).parent / "src"
sys.path.insert(0, str(SRC_PATH))

import domain
print("[conftest] domain viene de:", domain.__file__, file=sys.stderr)
print("[conftest] domain.__path__:", list(domain.__path__), file=sys.stderr)

try:
    import domain.entities
    print("[conftest] domain.entities importado OK", file=sys.stderr)
except Exception as e:
    print("[conftest] ERROR importando domain.entities:", repr(e), file=sys.stderr)
