import subprocess
import time
import resource
import logging
import json
import numpy as np
from pathlib import Path


DIR = Path(__file__).parent
DATA_DIR = DIR.parent / 'data'
MEMORY_LIMIT_MB = 8 * 1024
EXCUTABLES = {

}

logging.basicConfig(
    level = logging.INFO,
    format = '%(levelname)s - %(message)s',
    filename = DIR / 'evaluate.log',
    filemode='w'
)

def set_process_limit():
    mem_limit_bytes = MEMORY_LIMIT_MB * 1024 * 1024
    resource.setrlimit(resource.RLIM_AS, (mem_limit_bytes, mem_limit_bytes))

def run_test_case(test_file: Path, excutable_path: Path, dataset_name: str):
    logging.info(f"[Dataset: {dataset_name} | Algo: {test_file.name} - Started evaluating {test_file.name}]")

    gaps = []
    total_elapsed_time = 0
    num_test = 0
    with open(test_file, 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith('version'):
                continue

            num_test += 1
            parts = line.split()
            map_file = (DATA_DIR / parts[1]).with_suffix('.npy')
            x_start, y_start = int(parts[4]), int(parts[5])
            x_end, y_end = int(parts[6]), int(parts[7])
            optimal_value = float(parts[8])

            input_data = f'{map_file}\n{x_start} {y_start}\n{x_end} {y_end}\n'

            start_time = time.perf_counter()
            alg_value = None
            gap = None

            try:
                command = ['python3', excutable_path]
                process = subprocess.run(
                    command,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    preexec_fn=set_process_limit
                )

                elapsed_time = time.perf_counter() - start_time
                total_elapsed_time += elapsed_time

                if process.returncode == 0:
                    output = process.stdout.strip()
                    alg_value = float(output)

                    if alg_value == -1:
                        logging.info("No solution")

                    else:
                        gap = (alg_value - optimal_value) / optimal_value * 100
                        gaps.append(gap)

                        logging.info(f"AC | Gap: {gap:.2f}% | Time: {elapsed_time}s")

                else:
                    logging.warning("RE / MLE")

            except Exception as e:
                logging.error(e)

    return num_test, gaps, total_elapsed_time

def evaluate(excutable_path: Path, dataset_path: Path):
    if not excutable_path.exists():
        logging.error(f"{excutable_path} not found")

        return 0, 0, 0

    test_files = sorted([f for f in (dataset_path / 'scenario').glob('*.scen')])

    total_test = 0
    total_gaps = []
    total_time = 0
    for test_file in test_files:
        num_test, gaps, total_elapsed_time = run_test_case(test_file, excutable_path, dataset_path.name)
        total_test += num_test
        total_gaps.extend(gaps)
        total_time += total_elapsed_time

    passed_percentage = len(total_gaps) / total_test * 100
    avg_gap = np.mean(total_gaps)

    return passed_percentage, avg_gap, total_time

def save_to_json(results: dict, dataset_name: str):
    save_dir = DIR / 'results' / dataset_name
    save_dir.mkdir(parents=True, exist_ok=True)

    json_path = save_dir / 'result.json'

    data = {}
    if json_path.exists():
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

    for algo_name, result in results.items():
        data[algo_name] = result

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    logging.info(f"Saved results to {save_dir}")


for dataset_path in [f for f in DATA_DIR.iterdir() if f.is_dir()]:
    logging.info(f"=== Starting evaluation for Dataset: {dataset_path.name} ===")

    results = {}
    for algo_name, algo_path in EXCUTABLES.items():
        logging.info(f"--- Running Algorithm: {algo_name} on Dataset: {dataset_path.name} ---")

        passed_percentage, avg_gap, total_time = evaluate(algo_path, dataset_path)
        logging.info(f"[Summary Result] Dataset: {dataset_path.name} | Algo: {algo_name}")
        logging.info(f"Passed: {passed_percentage:.2f}% | Gap: {avg_gap:.2f}% | Time: {total_time:.2f}s")

        results[algo_name] = {
            'passed': passed_percentage,
            'gap': avg_gap,
            'time': total_time
        }
        save_to_json(results, dataset_path.name)
