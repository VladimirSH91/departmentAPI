import sys
from pathlib import Path
import pytest

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

# Add the app directory to the Python path
app_path = src_path / "app"
sys.path.insert(0, str(app_path))

# Configure pytest-asyncio
pytest_plugins = ('pytest_asyncio',)
