"""Tests for visualization module."""

from colmap_rerun.visualization.visualizer import convert_simple_radial_to_pinhole, scale_camera


def test_convert_simple_radial_to_pinhole():
    """Test camera model conversion."""
    from colmap_rerun.core.read_write_model import Camera

    camera = Camera(id=1, model="SIMPLE_RADIAL", width=640, height=480, params=[500, 320, 240, 0.1])
    converted = convert_simple_radial_to_pinhole(camera)
    assert converted.model == "PINHOLE"
    assert len(converted.params) == 4
    assert converted.params[0] == converted.params[1]  # fx == fy


def test_scale_camera():
    """Test camera scaling."""
    from colmap_rerun.core.read_write_model import Camera

    camera = Camera(id=1, model="PINHOLE", width=640, height=480, params=[500, 500, 320, 240])
    scaled, scale_factor = scale_camera(camera, (320, 240))
    assert scaled.width == 320
    assert scaled.height == 240
    assert scale_factor[0] == 0.5
    assert scale_factor[1] == 0.5
    assert scaled.params[0] == 250  # fx scaled
    assert scaled.params[2] == 160  # cx scaled
