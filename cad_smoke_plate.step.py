"""Small text-to-CAD smoke test: a drilled mounting plate.

Units: millimeters. Origin is at the plate center on the bottom face;
the XY plane is the mounting plane and +Z is thickness.
"""

from build123d import Align, Box, Cylinder, Location, chamfer


WIDTH = 80.0
DEPTH = 50.0
THICKNESS = 6.0
HOLE_DIAMETER = 4.5  # M4 normal clearance
HOLE_X = 30.0
HOLE_Y = 15.0
CUTOUT_WIDTH = 20.0
CUTOUT_DEPTH = 12.0
PEDESTAL_WIDTH = 16.0
PEDESTAL_DEPTH = 10.0
PEDESTAL_HEIGHT = 8.0
PEDESTAL_Y = 17.5
EDGE_CHAMFER = 1.0


def gen_step():
    plate = Box(WIDTH, DEPTH, THICKNESS, align=(Align.CENTER, Align.CENTER, Align.MIN))

    # Four through holes, patterned from the plate center.
    for x in (-HOLE_X, HOLE_X):
        for y in (-HOLE_Y, HOLE_Y):
            plate -= Location((x, y, -1.0)) * Cylinder(
                HOLE_DIAMETER / 2.0,
                THICKNESS + 2.0,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )

    # Centered rectangular through-cutout.
    plate -= Location((0, 0, -1.0)) * Box(
        CUTOUT_WIDTH,
        CUTOUT_DEPTH,
        THICKNESS + 2.0,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    # Raised rectangular pedestal on the top face, clear of the cutout and holes.
    plate += Location((0, PEDESTAL_Y, THICKNESS)) * Box(
        PEDESTAL_WIDTH,
        PEDESTAL_DEPTH,
        PEDESTAL_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    # Cosmetic chamfer on the four outside vertical edges.
    vertical_edges = [edge for edge in plate.edges() if abs((edge @ 1 - edge @ 0).Z) > THICKNESS * 0.9]
    return chamfer(vertical_edges, length=EDGE_CHAMFER)
