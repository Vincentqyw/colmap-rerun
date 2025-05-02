"""Visualization of COLMAP reconstructions using Rerun."""

import os
import re
from pathlib import Path
from typing import Dict, Any, Optional, Tuple

import cv2
import numpy as np
import numpy.typing as npt
import rerun as rr
import rerun.blueprint as rrb
from tqdm import tqdm

from ..core.model import Camera, Image, Point3D, read_array

FILTER_MIN_VISIBLE: int = 100  # Minimum number of visible points to keep an image

def scale_camera(camera: Camera, resize: Tuple[int, int]) -> Tuple[Camera, npt.NDArray[np.float64]]:
    """Scale camera intrinsics to match resized image dimensions."""
    assert camera.model == "PINHOLE"
    new_width, new_height = resize
    scale_factor = np.array([new_width / camera.width, new_height / camera.height])

    # For PINHOLE camera model, params are: [focal_length_x, focal_length_y, principal_point_x, principal_point_y]
    new_params = np.append(
        camera.params[:2] * scale_factor, 
        camera.params[2:] * scale_factor
    )

    return (
        Camera(camera.id, camera.model, new_width, new_height, new_params),
        scale_factor,
    )

def convert_simple_radial_to_pinhole(camera: Camera) -> Camera:
    """Convert COLMAP SIMPLE_RADIAL camera model to PINHOLE model."""
    if camera.model != "SIMPLE_RADIAL":
        return camera
        
    assert len(camera.params) == 4
    assert camera.width > 0 and camera.height > 0

    # For SIMPLE_RADIAL camera model, params are: [focal_length, principal_point_x, principal_point_y, k1]
    new_params = np.array(
        [camera.params[0], camera.params[0], camera.params[1], camera.params[2]]
    )

    return Camera(camera.id, "PINHOLE", camera.width, camera.height, new_params)

def visualize_reconstruction(
    cameras: Dict[int, Camera],
    images: Dict[int, Image], 
    points3D: Dict[int, Point3D],
    images_root: Path,
    depth_root: Optional[Path] = None,
    filter_output: bool = True,
    resize: Optional[Tuple[int, int]] = None
) -> None:
    """Log COLMAP reconstruction to Rerun for visualization."""
    print("Building visualization by logging to Rerun")

    rr.init("colmap_sparse_model", spawn=True)
    blueprint = rrb.Blueprint(
        rrb.Horizontal(
            rrb.Spatial3DView(name="3D", origin="/"),
            rrb.Vertical(
                rrb.Spatial2DView(name="Camera", origin="/camera/image"),
                rrb.Spatial2DView(name="Depth", origin="/camera/depth"),
                rrb.TimeSeriesView(origin="/plot"),
            ),
        )
    )
    rr.send_blueprint(blueprint)

    rr.log("/", rr.ViewCoordinates.RIGHT_HAND_Y_DOWN, static=True)
    rr.log("plot/avg_reproj_err", rr.SeriesLines(colors=[240, 45, 58]), static=True)

    if filter_output:
        # Filter out noisy points
        points3D = {
            id: point
            for id, point in points3D.items()
            if point.rgb.any() and len(point.image_ids) > 4
        }
    
    # Log all 3D points (static, visible at all times)
    all_points = [point.xyz for point in points3D.values()]
    all_colors = [point.rgb for point in points3D.values()]
    rr.log("points/all", rr.Points3D(all_points, colors=all_colors), static=True)

    # Iterate through images (video frames) logging data related to each frame.
    for image in tqdm(sorted(images.values(), key=lambda im: im.name)):
        image_file = images_root / image.name

        if not os.path.exists(image_file):
            continue

        # COLMAP sets image ids that don't match the original video frame
        idx_match = re.search(r"\d+", image.name)
        assert idx_match is not None
        frame_idx = int(idx_match.group(0))

        quat_xyzw = image.qvec[[1, 2, 3, 0]]  # COLMAP uses wxyz quaternions
        camera = cameras[image.camera_id]
        camera = convert_simple_radial_to_pinhole(camera)
        if resize:
            camera, scale_factor = scale_camera(camera, resize)
        else:
            scale_factor = np.array([1.0, 1.0])

        visible = [
            id != -1 and points3D.get(id) is not None for id in image.point3D_ids
        ]
        visible_ids = image.point3D_ids[visible]

        if filter_output and len(visible_ids) < FILTER_MIN_VISIBLE:
            continue

        visible_xyzs = [points3D[id] for id in visible_ids]
        visible_xys = image.xys[visible]
        if resize:
            visible_xys *= scale_factor

        rr.set_time("frame", sequence=frame_idx)

        points = [point.xyz for point in visible_xyzs]
        point_colors = [[255, 0, 0] for point in visible_xyzs]
        point_errors = [point.error for point in visible_xyzs]

        rr.log("plot/avg_reproj_err", rr.Scalars(np.mean(point_errors)))

        rr.log(
            "points",
            rr.Points3D(points, colors=point_colors, radii=[0.05] * len(points)),
            rr.AnyValues(error=point_errors),
        )

        # COLMAP's camera transform is "camera from world"
        rr.log(
            "camera",
            rr.Transform3D(
                translation=image.tvec.tolist(),
                rotation=rr.Quaternion(xyzw=quat_xyzw),
                relation=rr.TransformRelation.ChildFromParent,
            ),
        )
        rr.log(
            "camera", rr.ViewCoordinates.RDF, static=True
        )  # X=Right, Y=Down, Z=Forward

        # Log camera intrinsics
        assert camera.model == "PINHOLE"
        rr.log(
            "camera/image",
            rr.Pinhole(
                resolution=[camera.width, camera.height],
                focal_length=camera.params[0:2],
                principal_point=camera.params[2:4],
            ),
        )

        bgr = cv2.imread(str(image_file))
        if depth_root:
            depth_path = depth_root / f"{image.name}.geometric.bin"
            if depth_path.exists():
                depth = read_array(depth_path)
                if resize:
                    depth = cv2.resize(depth, resize)
                rr.log("camera/depth", rr.DepthImage(depth, colormap="Turbo"))

        if resize:
            bgr = cv2.resize(bgr, resize)
            
        rr.log("camera/image", rr.Image(bgr, color_model="BGR").compress(jpeg_quality=75))
        rr.log("camera/image/keypoints", rr.Points2D(visible_xys, colors=[34, 138, 167]))
