import numpy as np
from pathlib import Path


DATA_DIR = Path(__file__).parent

for folder in DATA_DIR.iterdir():
    if not folder.is_dir():
        continue
    
    print("-" * 5, f"Đang xử lý thư mục {folder.name}", "-" * 5)

    for filepath in (folder / 'map').glob('*.map'):
        print(f"Đang xử lý file {filepath.name}")

        grid = []
        reading_map = False

        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('map'):
                    reading_map = True
                    continue

                if reading_map:
                    row = []
                    for char in line:
                        if char == '.':
                            row.append(0)
                        else:
                            row.append(1)
                    grid.append(row)

        grid = np.array(grid, dtype=np.int8)
        np.save(filepath.with_suffix('.npy'), grid)
        filepath.unlink()
