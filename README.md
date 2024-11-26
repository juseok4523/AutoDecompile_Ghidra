# Auto Decompile with Ghidra

Ghidra를 활용하여 바이너리 데이터를 디컴파일링 하는 도구.

## Install

1. [Ghidra](https://github.com/NationalSecurityAgency/ghidra/releases) 를 원하는 위치에 설치.
2. .env 파일을 생성하고, 해당 파일에 `GHIDRA_INSTALL_DIR=[Ghidra가 설치된 위치]` 를 작성. 또는 각 운영체제에 맞는 환경 변수에 `GHIDRA_INSTALL_DIR=[Ghidra가 설치된 위치]`를 추가.
3. `pip install python-dotenv` : Python 필요 모듈 설치.

## Usage

```console
usage: decompile_ghidra.py [-h] --file FILE [--output_dir OUTPUT_DIR]        

testing auto decompiler with Ghidra

options:
  -h, --help            show this help message and exit
  --file FILE           File Path to Decompile.
  --output_dir OUTPUT_DIR
                        Save Decompiled Results Directory. default: ./results
```
