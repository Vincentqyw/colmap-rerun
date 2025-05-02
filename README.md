# COLMAP Rerun Visualizer

<!-- [![PyPI Version](https://img.shields.io/pypi/v/colmap-rerun)](https://pypi.org/project/colmap-rerun/) -->
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
<!-- [![Python Version](https://img.shields.io/pypi/pyversions/colmap-rerun)](https://pypi.org/project/colmap-rerun/) -->
<!-- [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) -->

Visualize COLMAP sparse reconstruction output using Rerun's 3D visualization capabilities.

https://github.com/user-attachments/assets/590b9902-6213-4545-985a-af478ab6d576

## Features

- Interactive 3D visualization of COLMAP reconstructions
- Support for both filtered and unfiltered point clouds
- Dataset-specific visualization presets
- Resolution scaling for performance optimization
- Python API and CLI interface

## Installation

### From PyPI

TODO
<!-- ```bash
pip install colmap-rerun
``` -->

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

## Quick Start

### Example Dataset

We provide sample reconstruction data to help you get started:

1. Download the sample data from [Google Drive](https://drive.google.com/drive/folders/1pqhjHtgIESKB_QL8NSaFQdwysFZluLSs?usp=drive_link)
2. Unzip the downloaded file to get the following directory structure:
```
sample_data/dense
├── images/             # Input images
├── sparse/             # COLMAP sparse reconstruction
│   ├── cameras.bin     # Camera parameters
│   ├── images.bin      # Image poses
│   └── points3D.bin    # 3D point cloud
└── stereo/depth_maps/  # Optional depth maps
```

3. Visualize the reconstruction:

Using CLI:
```bash
visualize-colmap --dataset sample_data/dense
```

Or using Python API:

```python
from pathlib import Path
from colmap_rerun import visualize_reconstruction
from colmap_rerun.core.read_write_model import read_model

# Setting data root
data_root = Path("sample_data/dense")

# Load reconstruction
cameras, images, points3D = read_model(data_root / "sparse")

# Visualize
visualize_reconstruction(
    cameras=cameras,
    images=images,
    points3D=points3D,
    images_root=Path(data_root / "images"),
    depth_root=Path(data_root / "stereo/depth_maps"),  # optional
)
```

### CLI Usage

```bash
visualize-colmap [--unfiltered] [--dataset DATASET] [--resize WxH]
```

#### Options
- `--unfiltered`: Disable filtering of noisy 3D points
- `--dataset`: Dataset to visualize (colmap_rusty_car or colmap_fiat)
- `--resize`: Target resolution (e.g. 640x480)

### Python API

```python
from pathlib import Path
from colmap_rerun import visualize_reconstruction
from colmap_rerun.core.read_write_model import read_model

# Load COLMAP reconstruction
cameras, images, points3D = read_model("path/to/colmap/reconstruction")

# Visualize
visualize_reconstruction(
    cameras=cameras,
    images=images,
    points3D=points3D,
    images_root=Path("path/to/images"),
    depth_root=Path("path/to/depth"),  # optional
)
```

## Documentation

Full documentation is available at [docs/](docs/).

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

1. Install development dependencies:
```bash
pip install -e ".[dev]"
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
black .
```

## Code of Conduct

This project adheres to the Contributor Covenant [code of conduct](CODE_OF_CONDUCT.md).

## Acknowledgements

- This project uses [Rerun](https://github.com/rerun-io/rerun) for visualization
- Inspired by COLMAP's 3D reconstruction capabilities

## License

MIT - See [LICENSE](LICENSE) for details.
