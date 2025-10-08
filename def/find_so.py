from config import llvm_bin_fdr, binary_fdr
from pathlib import Path
import subprocess

def find_symbol_in_binaries(symbol_name: str):
    llvm_objdump = Path(llvm_bin_fdr) / "llvm-objdump"
    
    for so_file in binary_fdr.glob("*.so"):
        try:
            # Run llvm-objdump -T on the .so file
            result = subprocess.run(
                [str(llvm_objdump), "-T", str(so_file)],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Check if symbol exists in output
            if symbol_name in result.stdout:
                print(f"Symbol '{symbol_name}' found in {so_file.name}")
                # Print matching lines
                for line in result.stdout.splitlines():
                    if symbol_name in line:
                        print(f"  {line.strip()}")
        
        except subprocess.CalledProcessError as e:
            print(f"Error processing {so_file.name}: {e}")
        except Exception as e:
            print(f"Unexpected error with {so_file.name}: {e}")

find_symbol_in_binaries("OH_LOG_PrintMsg")