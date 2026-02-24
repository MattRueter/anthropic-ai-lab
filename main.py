import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: eval <feature_name>")
        sys.exit(1)

    feature = sys.argv[1]
    module_path = f"{feature}.main"

    project_root = Path(__file__).resolve().parent

    subprocess.run([
      "python3", "-m", module_path],
      cwd=project_root
      )

if __name__ == "__main__":
    main()
