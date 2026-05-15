import sys
from pathlib import Path
import pytest

src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

app_path = src_path / "app"
sys.path.insert(0, str(app_path))

pytest_plugins = ('pytest_asyncio',)
