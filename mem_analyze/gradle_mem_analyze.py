#!/usr/bin/env python3
"""
Analyze memory consumption of a Gradle build and its spawned processes on macOS.
Uses footprint to measure physical footprint; outputs interactive HTML plots.
"""

import argparse
import csv
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    HAS_PLOTLY = True
except ImportError:
    HAS_PLOTLY = False

DEFAULT_INTERVAL = 1
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUT = SCRIPT_DIR / "mem_analyze_output"
FOOTPRINT_REGEX = re.compile(r"phys_footprint(?:_peak)?:\s*(\d+)")
SUMMARY_FOOTPRINT_REGEX = re.compile(r"Summary Footprint:\s*(\d+)\s*B")
PROCESS_HEADER_REGEX = re.compile(r"^(\S+)\s+\[(\d+)\]:", re.MULTILINE)
VM_STAT_PAGE_SIZE = re.compile(r"page size of (\d+) bytes")
VM_STAT_PAGES_FREE = re.compile(r"Pages free:\s*([\d.]+)")


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    sys.exit(code)


def run_footprint_tree(pid: int) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["footprint", "-f", "bytes", "-t", "-p", str(pid)],
        capture_output=True,
        text=True,
        timeout=60,
    )


def parse_footprint_tree_output(out: str) -> tuple[dict[int, dict], dict[str, int]]:
    """
    Parse footprint -t output. Returns (by_pid, tree_data).
    by_pid: {pid: {phys_footprint, phys_footprint_peak, name}}
    tree_data: {summary_footprint}
    """
    by_pid: dict[int, dict] = {}
    tree_data: dict[str, int] = {}

    m = SUMMARY_FOOTPRINT_REGEX.search(out)
    if m:
        tree_data["summary_footprint"] = int(m.group(1))

    # For each "name [pid]:" find its section (until next process or Summary/Shared Cache)
    for m in PROCESS_HEADER_REGEX.finditer(out):
        name, pid_str = m.group(1), m.group(2)
        start = m.start()
        end = len(out)
        next_h = PROCESS_HEADER_REGEX.search(out, start + 1)
        for pos in (
            next_h.start() if next_h else len(out),
            out.find("Summary Footprint", start),
            out.find("Shared Cache", start),
        ):
            if 0 <= pos < end:
                end = pos
        sec = out[start:end]
        aux_match = FOOTPRINT_REGEX.findall(sec)
        phys = int(aux_match[0]) if len(aux_match) > 0 else None
        phys_peak = int(aux_match[1]) if len(aux_match) > 1 else phys
        if phys is not None:
            by_pid[int(pid_str)] = {
                "phys_footprint": phys,
                "phys_footprint_peak": phys_peak or phys,
                "name": name,
            }
    return by_pid, tree_data


def run_vm_stat() -> subprocess.CompletedProcess:
    return subprocess.run(
        ["vm_stat"],
        capture_output=True,
        text=True,
        timeout=5,
    )


def parse_vm_stat(out: str) -> int | None:
    """Parse vm_stat output, return free memory in bytes or None."""
    page_size = 16384
    m = VM_STAT_PAGE_SIZE.search(out)
    if m:
        page_size = int(m.group(1))
    m = VM_STAT_PAGES_FREE.search(out)
    if m:
        pages = int(float(m.group(1).rstrip(".")))
        return pages * page_size
    return None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze Gradle build memory consumption (macOS, uses footprint)"
    )
    parser.add_argument("-d", "--dir", type=Path, required=True, help="Project directory with gradlew")
    parser.add_argument("-i", "--interval", type=float, default=DEFAULT_INTERVAL, help="Poll interval (seconds)")
    parser.add_argument(
        "gradle_args",
        nargs="*",
        help="Gradle command (e.g. ./gradlew :app:build)",
    )
    args = parser.parse_args()

    if not HAS_PLOTLY:
        die(
            "plotly is required for HTML plots. Install before running:\n"
            "  pip install plotly"
        )

    if sys.platform != "darwin":
        die("This script requires macOS (uses 'footprint' command)")

    proj_dir = args.dir.resolve()
    gradlew = proj_dir / "gradlew"
    if not gradlew.exists():
        die(f"gradlew not found in {proj_dir}")

    cmd = args.gradle_args
    if cmd[0] in ("./gradlew", "gradlew"):
        cmd[0] = str(proj_dir / "gradlew")
    elif not Path(cmd[0]).is_absolute():
        cmd[0] = str(proj_dir / cmd[0])

    out_dir = DEFAULT_OUT
    out_dir.mkdir(parents=True, exist_ok=True)
    run_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = out_dir / run_name
    run_dir.mkdir(parents=True, exist_ok=True)
    footprint_dir = run_dir / "footprint"
    footprint_dir.mkdir(exist_ok=True)

    # Stop daemons
    print("Stopping Gradle daemons...")
    subprocess.run(
        [str(gradlew), "--stop"],
        cwd=proj_dir,
        capture_output=True,
        timeout=60,
        check=False,
    )

    # Spawn build (output to log file; use tail -f to track progress)
    log_path = run_dir / "gradle_output.log"
    print(f"Starting: {' '.join(cmd)}")
    print(f"Build output: {log_path} (use 'tail -f' to track progress)")
    log_file = open(log_path, "w", encoding="utf-8", errors="replace")
    proc = subprocess.Popen(
        cmd,
        cwd=proj_dir,
        stdout=log_file,
        stderr=subprocess.STDOUT,
        text=True,
    )
    root_pid = proc.pid

    samples: list[dict] = []
    interval = args.interval
    all_pids_seen: dict[int, str] = {}
    pid_first_seen: dict[int, int] = {}
    sample_idx = 0

    try:
        time.sleep(0.5)  # brief moment for process to spawn
        while proc.poll() is None:
            try:
                r = run_footprint_tree(root_pid)
                vm_free_b: int | None = None
                try:
                    rv = run_vm_stat()
                    if rv.returncode == 0 and rv.stdout:
                        vm_free_b = parse_vm_stat(rv.stdout)
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass
                if r.stdout:
                    (footprint_dir / f"sample_{sample_idx:04d}_tree.txt").write_text(
                        r.stdout, encoding="utf-8", errors="replace"
                    )
                if r.returncode == 0 and r.stdout:
                    by_pid, tree_data = parse_footprint_tree_output(r.stdout)
                    for pid, data in by_pid.items():
                        if pid not in all_pids_seen:
                            all_pids_seen[pid] = data.get("name", f"pid:{pid}")
                            pid_first_seen[pid] = sample_idx
                    samples.append({
                        "time": time.time(),
                        "by_pid": by_pid,
                        "tree": tree_data,
                        "vm_free_bytes": vm_free_b,
                    })
                    sample_idx += 1
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
            time.sleep(interval)
    except KeyboardInterrupt:
        proc.terminate()
        proc.wait(timeout=10)
        print("Interrupted", file=sys.stderr)

    proc.wait()
    log_file.close()

    if not samples:
        die("No memory samples collected")

    # Compute peaks
    peak_by_pid: dict[int, int] = {}
    tree_peaks: list[int] = []

    for s in samples:
        for pid, data in s["by_pid"].items():
            p = data.get("phys_footprint_peak") or data.get("phys_footprint") or 0
            peak_by_pid[pid] = max(peak_by_pid.get(pid, 0), p)
        t = s["tree"].get("summary_footprint") or 0
        tree_peaks.append(t)

    tree_peak = max(tree_peaks) if tree_peaks else 0
    t0 = samples[0]["time"]

    # Print peak table
    print("\n--- Peak memory (phys_footprint_peak / phys_footprint) ---")
    rows = [(pid, all_pids_seen.get(pid, f"pid:{pid}"), peak) for pid, peak in sorted(peak_by_pid.items(), key=lambda x: -x[1])]
    for pid, name, peak in rows:
        mb = peak / (1024 * 1024)
        print(f"  {name} (pid {pid}): {mb:.2f} MB")
    print(f"  [Tree total peak]: {tree_peak / (1024 * 1024):.2f} MB")

    # Plotly HTML
    if HAS_PLOTLY and peak_by_pid:
        times = [s["time"] - t0 for s in samples]

        # Per-process: one line per process, X=time, Y=phys_footprint (current, non-shared)
        # Line starts from when that subprocess was first seen
        fig1 = go.Figure()
        for pid in sorted(peak_by_pid.keys(), key=lambda p: pid_first_seen.get(p, 0)):
            name = all_pids_seen.get(pid, f"pid:{pid}")
            first_idx = pid_first_seen.get(pid, 0)
            pts_t, pts_y = [], []
            for i, s in enumerate(samples):
                if i < first_idx:
                    continue
                data = s["by_pid"].get(pid)
                if not data:
                    continue
                val = data.get("phys_footprint") or data.get("phys_footprint_peak")
                if val is not None:
                    pts_t.append(times[i])
                    pts_y.append(val / (1024 * 1024))
            if pts_t:
                fig1.add_trace(
                    go.Scatter(x=pts_t, y=pts_y, mode="lines+markers", name=f"{name} (pid {pid})")
                )
        fig1.update_layout(
            title="Physical memory per process over time (non-shared, MB)",
            xaxis_title="Seconds since start",
            yaxis_title="MB",
        )
        fig1.write_html(run_dir / "phys_mem_per_process.html")

        # Per-process CSV
        pids_sorted = sorted(peak_by_pid.keys(), key=lambda p: pid_first_seen.get(p, 0))
        cols = ["time_sec"] + [f"{all_pids_seen.get(p, f'pid:{p}')}_{p}" for p in pids_sorted]
        with open(run_dir / "phys_mem_per_process.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(cols)
            for i, s in enumerate(samples):
                row = [round(times[i], 2)]
                for pid in pids_sorted:
                    data = s["by_pid"].get(pid)
                    val = ""
                    if data:
                        v = data.get("phys_footprint") or data.get("phys_footprint_peak")
                        if v is not None:
                            val = round(v / (1024 * 1024), 2)
                    row.append(val)
                w.writerow(row)

        # Tree: total memory over time + physical memory free
        tree_total = [
            (s["tree"].get("summary_footprint") or 0) / (1024 * 1024)
            for s in samples
        ]
        vm_free_mb = [(s.get("vm_free_bytes") or 0) / (1024 * 1024) for s in samples]
        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(x=times, y=tree_total, mode="lines+markers", name="Tree total (MB)")
        )
        fig2.add_trace(
            go.Scatter(
                x=times,
                y=vm_free_mb,
                mode="lines+markers",
                name="Physical memory free (MB)",
                yaxis="y2",
            )
        )
        fig2.update_layout(
            title="Tree total vs physical memory free over time",
            xaxis_title="Seconds since start",
            yaxis_title="Tree total (MB)",
            yaxis2=dict(
                title="Physical memory free (MB)",
                overlaying="y",
                side="right",
            ),
        )
        fig2.write_html(run_dir / "total_tree_over_time.html")

        # Tree CSV
        with open(run_dir / "total_tree_over_time.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["time_sec", "tree_total_mb", "physical_memory_free_mb"])
            for i in range(len(times)):
                w.writerow([
                    round(times[i], 2),
                    round(tree_total[i], 2),
                    round(vm_free_mb[i], 2),
                ])

        print(f"\nOutput: {run_dir.absolute()}/")
        print(f"  phys_mem_per_process.html, total_tree_over_time.html, *.csv, footprint/, gradle_output.log")


if __name__ == "__main__":
    main()
