from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

module_path = Path(__file__).parent / "billpayment-api" / "app.py"
spec = spec_from_file_location("billpayment_app", module_path)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load app module from {module_path}")

module = module_from_spec(spec)
spec.loader.exec_module(module)
app = module.app
