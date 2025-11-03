#!/usr/bin/env python3
"""
Compare difference between 2 capi versions.
Reads two CSV files, extracts full_signature column into sets, and shows differences.
"""

import csv

def load_signatures(file_path):
    """Load full_signature column from CSV into a set."""
    signatures = set()
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            signature = row.get('full_signature', '').strip()
            if signature:
                signatures.add(signature)
    return signatures

def main():
    file_low = "header_16.csv"
    file_high = "header_20.csv"
    
    # Load signatures from both files
    sigs_low = load_signatures(file_low)
    sigs_high = load_signatures(file_high)
    
    # Calculate differences
    only_in_low = sigs_low - sigs_high
    only_in_high = sigs_high - sigs_low
    
    # Print results
    print(f"=== Only in {file_low} ({len(only_in_low)} functions) ===")
    for sig in sorted(only_in_low):
        print(sig)
    
    print(f"\n=== Only in {file_high} ({len(only_in_high)} functions) ===")
    for sig in sorted(only_in_high):
        print(sig)
    
    print(f"\n=== Summary ===")
    print(f"Only in {file_low}: {len(only_in_low)}")
    print(f"Only in {file_high}: {len(only_in_high)}")
    print(f"Common: {len(sigs_low & sigs_high)}")
    print(f"Total unique: {len(sigs_low | sigs_high)}")

if __name__ == "__main__":
    main()