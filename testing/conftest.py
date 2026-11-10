"""Make the model package's modules importable for the tests in this folder."""
import pathlib
import sys

MODEL_DIR = pathlib.Path(__file__).resolve().parent.parent / "Quillan-v4.2-model"
if str(MODEL_DIR) not in sys.path:
    sys.path.insert(0, str(MODEL_DIR))
