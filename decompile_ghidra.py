import os
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
import argparse
from dotenv import load_dotenv

load_dotenv()

GHIDRA_INSTALL = Path(os.getenv("GHIDRA_INSTALL_DIR", ""))

if len(f"{GHIDRA_INSTALL}") < 3:
    print("[Error] Please enter the folder where ghidra is installed in the .env file into GHIDRA_INSTALL_DIR. ")
    sys.exit(0)

GHIDRA_HEADLESS = GHIDRA_INSTALL / 'support' / 'analyzeHeadless'

GHIDRA_APP_PROPERTIES = GHIDRA_INSTALL / 'Ghidra' / 'application.properties'

def main(file_name, results_dir):
    with tempfile.TemporaryDirectory() as tempdir:
        inname = file_name

        project_dir = tempfile.TemporaryDirectory(dir=tempdir)
        output_dir = tempfile.TemporaryDirectory(dir=tempdir)

        output_file = Path(output_dir.name + "/out")
        parent_dir = Path(__file__).resolve().parent

        decompile_command = [
            f"{GHIDRA_HEADLESS}",
            project_dir.name,
            "temp",
            "-import",
            f"{inname}",
            "-scriptPath",
            f"{parent_dir}",
            "-postScript",
            f"{parent_dir / 'DecompilerExplorer.java'}",
            f"{output_file}"
        ]
        print(' '.join(decompile_command))
        env = os.environ.copy()
        env['PATH'] = f"{parent_dir}/jdk/bin:{env['PATH']}"

        if not os.path.exists(output_file):
            if platform.system() == "Windows":
                decomp = subprocess.run(decompile_command, capture_output=True, env=env, shell=True)
            else :
                decomp = subprocess.run(decompile_command, capture_output=True, env=env)
            if decomp.returncode != 0 or not os.path.exists(output_file):
                print(f'[Error]\n{decomp.stdout.decode()}\n{decomp.stderr.decode()}')
                sys.exit(1)
        with open(output_file, 'r', errors="ignore") as f:
            result = f.read()
            with open(results_dir / f"{file_name.stem}.txt", 'w') as ff:
                ff.write(result)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--version':
        version = None
        revision = None
        for line in GHIDRA_APP_PROPERTIES.read_text().splitlines():
            parts = line.split('=')
            if len(parts) < 2:
                continue
            name, val = parts
            if name == 'application.version':
                version = val
                break
        for line in GHIDRA_APP_PROPERTIES.read_text().splitlines():
            parts = line.split('=')
            if len(parts) < 2:
                continue
            name, val = parts
            if name == 'application.revision.ghidra':
                revision = val
                break
        if version is not None and revision is not None:
            print(version)
            print(revision)
        else:
            print("Unknown")
            print("Unknown")
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == '--name':
        print('Ghidra')
        sys.exit(0)

    parser = argparse.ArgumentParser(description="testing auto decompiler with Ghidra")
    
    parser.add_argument("--file", required=True, help="File Path to Decompile.")
    parser.add_argument("--output_dir", default="./results", help="Save Decompiled Results Directory. default: ./results")
    
    args = parser.parse_args()
    file = Path(args.file)
    if file.exists() is False:
        print("[Error] --file: There are no files in this path.")
        sys.exit(0)
    output_dir = Path(args.output_dir)
    if output_dir.exists() is False:
        print("[Warning] --output_dir: There are no folders in that path. Create a folder...")
        output_dir.mkdir()        
    main(file.resolve(), output_dir.resolve())