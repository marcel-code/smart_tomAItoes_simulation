from pathlib import Path

root = Path(__file__).parent.parent
print(root)
TESTING_PATH = root / "testing/"
TRAINING_PATH = root / "training/"
EVALUATION_PATH = root / "evaluation/"
DATA_PATH = root / "src/" / "data/"
