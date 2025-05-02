# Structure from Motion Visualization

Visualize COLMAP sparse reconstruction output using Rerun.

## Installation

Install from source:

```bash
git clone https://github.com/vincentqyw/colmap_rerun.git
cd colmap_rerun
pip install -e .
```

## Usage

```bash
visualize-colmap [--unfiltered] [--dataset DATASET] [--resize WxH]
```


### Options
- `--unfiltered`: Disable filtering of noisy 3D points
- `--dataset`: Dataset to visualize (colmap_rusty_car or colmap_fiat)
- `--resize`: Target resolution (e.g. 640x480)

## Development

Install development dependencies:

```bash
pip install -e ".[test]"
```

Run tests:

```bash
pytest
```

## License

MIT
