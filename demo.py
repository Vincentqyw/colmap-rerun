"""Command line interface for visualizing COLMAP reconstructions."""

from argparse import ArgumentParser
from pathlib import Path

from src.colmap_rerun.core.reconstruction import load_sparse_model
from src.colmap_rerun.visualization.visualizer import visualize_reconstruction

import rerun as rr


def main() -> None:
    """Main entry point for visualizing COLMAP sparse reconstruction."""
    parser = ArgumentParser(description="Visualize the output of COLMAP's sparse reconstruction on a video.")
    parser.add_argument(
        "--sparse_model",
        help="Spare reconstruction dataset path, e.g., /path/to/dataset/sparse",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--images_path",
        help="Path to the folder containing images, e.g., /path/to/dataset/images",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--dense_model",
        help="Dense reconstruction dataset path, e.g., /path/to/dataset/dense",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--resize",
        nargs=2,
        type=int,
        help="Target resolution to resize images as width height, e.g., 640 480",
    )
    parser.add_argument(
        "--unfiltered",
        action="store_true",
        help="If set, we don't filter away any noisy data.",
    )
    rr.script_add_args(parser)
    args = parser.parse_args()
    rr.script_setup(args, application_id="colmap_rerun")
    if args.resize:
        args.resize = tuple(args.resize)

    # If a dense model is provided, we use the sparse model from the dense model path.
    # This is useful for visualizing the sparse model from a dense reconstruction.
    # The spare model is expected to be in the format /path/to/dataset/dense/sparse.
    # The images path is expected to be in the format /path/to/dataset/dense/images.
    # The depth maps path is expected to be in the format /path/to/dataset/dense/stereo/depth_maps.
    if args.dense_model is not None:
        args.sparse_model = args.dense_model / "sparse"
        args.images_path = args.dense_model / "images"
    else:
        if args.sparse_model is None:
            raise ValueError("Sparse model path is required.")
        if args.images_path is None:
            raise ValueError("Images path is required.")
        if not args.sparse_model.exists():
            raise ValueError(f"Sparse model path {args.sparse_model} does not exist.")
        if not args.images_path.exists():
            raise ValueError(f"Images path {args.images_path} does not exist.")

    recon = load_sparse_model(
        model_path=args.sparse_model,
        images_root=args.images_path,
        depths_root=args.dense_model / "stereo" / "depth_maps",
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
    rr.script_teardown(args)


if __name__ == "__main__":
    main()
