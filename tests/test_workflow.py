from pathlib import Path
import subprocess


def test_reproduce_main_results_runs():
    root = Path(__file__).resolve().parents[1]
    subprocess.run(['python', 'scripts/reproduce_main_results.py', '--config', 'configs/experiment_main.yaml'], cwd=root, check=True)
    assert (root / 'results/sample_outputs/reproduction_summary.csv').exists()
