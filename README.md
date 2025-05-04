# COLMAP Rerun Visualizer

[![PyPI Version](https://img.shields.io/pypi/v/colmap-rerun)](https://pypi.org/project/colmap-rerun/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
<!-- [![Python Version](https://img.shields.io/pypi/pyversions/colmap-rerun)](https://pypi.org/project/colmap-rerun/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) -->

Interactive 3D visualization of COLMAP sparse/dense reconstruction output using Rerun's visualization capabilities.

https://github.com/user-attachments/assets/590b9902-6213-4545-985a-af478ab6d576

## Features

- Interactive 3D visualization of COLMAP reconstructions
- Dataset-specific visualization presets
- Resolution scaling for performance optimization
- Python API and CLI interface

## Installation

### From PyPI

```bash
pip install colmap-rerun
```

### From Source

```bash
git clone https://github.com/vincentqyw/colmap_rerun.git
cd colmap_rerun
pip install -e .
```

For development:

```bash
pip install -e ".[dev]"
```

## Getting Started

### Download Example Dataset

Download sample reconstruction data:

1. Get sample data from [Google Drive](https://drive.google.com/drive/folders/1pqhjHtgIESKB_QL8NSaFQdwysFZluLSs?usp=drive_link)
2. Unzip to get directory structure:

```text
sample_data/dense/
├── images/               # Input images
├── sparse/               # COLMAP sparse reconstruction
│   ├── cameras.bin       # Camera intrinsics
│   ├── images.bin        # Camera poses
│   └── points3D.bin      # 3D point cloud
└── stereo/
    └── depth_maps/       # Depth maps (optional)
```

## Usage

### Demo Script (Quick Start)

Basic usage:
```bash
python demo.py --dense_model sample_data/dense
```

Advanced options:
```bash
python demo.py --dense_model sample_data/dense --resize 640 480 --unfiltered
```

### Python API

```python
from pathlib import Path
from colmap_rerun import visualize_reconstruction
from colmap_rerun.core.read_write_model import read_model

data_root = Path("sample_data/dense")
cameras, images, points3D = read_model(data_root / "sparse")

visualize_reconstruction(
    cameras=cameras,
    images=images,
    points3D=points3D,
    images_root=Path(data_root / "images"),
    depths_root=Path(data_root / "stereo/depth_maps"),  # optional
)
```

### Command Line Interface

After installing with `pip install -e .`:

```bash
viz-colmap --dense_model sample_data/dense
```

#### CLI Options

| Argument            | Description                                  | Required |
|---------------------|----------------------------------------------|----------|
| `--dense_model`     | Path to dense reconstruction folder          | No       |
| `--sparse_model`    | Path to sparse reconstruction folder         | Yes*     |
| `--images_path`     | Path to input images folder                  | Yes*     |
| `--resize W H`      | Resize images to width W and height H        | No       |
| `--unfiltered`      | Show unfiltered point cloud (with noise)     | No       |

*Required if not using dense_model

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Acknowledgements

- [Rerun](https://github.com/rerun-io/rerun) team for visualization framework
- Based on [structure_from_motion example](https://github.com/rerun-io/rerun/tree/main/examples/python/structure_from_motion)
- COLMAP team for 3D reconstruction work

## License

MIT - See [LICENSE](LICENSE) for details.
