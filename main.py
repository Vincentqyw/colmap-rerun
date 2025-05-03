"""Command line interface for visualizing COLMAP reconstructions."""

from argparse import ArgumentParser
from pathlib import Path

from src.colmap_rerun.core.reconstruction import load_sparse_model
from src.colmap_rerun.visualization.visualizer import visualize_reconstruction


def main() -> None:
    """Main entry point for visualizing COLMAP sparse reconstruction."""
    parser = ArgumentParser(
        description="Visualize the output of COLMAP's sparse reconstruction on a video."
    )
    parser.add_argument(
        "--dataset",
        action="store",
        default="colmap_rusty_car",
        choices=["colmap_rusty_car", "colmap_fiat"],
        help="Which dataset to download",
    )

    parser.add_argument(
        "--unfiltered",
        action="store_true",
        help="If set, we don't filter away any noisy data.",
    )

    parser.add_argument(
        "--resize",
        nargs=2,
        type=int,
        help="Target resolution to resize images as width height, e.g., 640 480",
    )
    args = parser.parse_args()

    if args.resize:
        args.resize = tuple(args.resize)

    dataset_path = Path("tussock_tiny_v2/dense")
    recon = load_sparse_model(
        model_path=dataset_path / "sparse",
        images_root=dataset_path / "images",
        depths_root=dataset_path / "stereo" / "depth_maps",
    )
    visualize_reconstruction(
        recon.cameras,
        recon.images,
        recon.points3D,
        recon.images_root,
        recon.depths_root,
        filter_output=not args.unfiltered,
        resize=args.resize,
    )


if __name__ == "__main__":
    main()
