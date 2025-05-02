"""Data structures for COLMAP reconstructions."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from .model import Camera, Image, Point3D, read_model

@dataclass
class ReconstructionData:
    """Container for COLMAP reconstruction data."""
    cameras: Dict[int, Camera]
    images: Dict[int, Image] 
    points3D: Dict[int, Point3D]
    images_root: Optional[Path] = None
    depth_root: Optional[Path] = None

def load_sparse_model(model_path: Path, images_root: Path, depths_root: Optional[Path] = None) -> ReconstructionData:
    """Load COLMAP sparse reconstruction from disk."""
    cameras, images, points3D = read_model(model_path)
    return ReconstructionData(
        cameras=cameras,
        images=images,
        points3D=points3D,
        images_root=images_root,
        depth_root=depths_root
    )
