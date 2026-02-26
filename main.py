import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) != 2:
        print("Usage: eval <feature_name> OR  eval features/<feature_name>/")
        sys.exit(1)

    raw_input = sys.argv[1]

    #Normalize input
    feature_name = Path(raw_input).name #unpacks name of feature folder

    module_path = f"features.{feature_name}.main"

    project_root = Path(__file__).resolve().parent
  
    subprocess.run([
      "python3", "-m", module_path],
      cwd=project_root
      )

if __name__ == "__main__":
    main()
