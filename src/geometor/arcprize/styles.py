from geometor.render.styles.z_levels import *

# Fixed color palette for classes 0 to 9
COLOR_PALETTE = [
    "#111111",  # 0: Dark grey (almost black) as requested
    "#FF0000",  # 1: Red
    "#00FF00",  # 2: Green
    "#0000FF",  # 3: Blue
    "#FF00FF",  # 4: Magenta
    "#FFFF00",  # 5: Yellow
    "#00FFFF",  # 6: Cyan
    "#FF8000",  # 7: Orange
    "#8000FF",  # 8: Purple
    "#00FF80",  # 9: Spring Green
]

def generate_class_style(class_num):
    color = COLOR_PALETTE[class_num]
    return {
        "point_inner": {
            "color": "w",
            "linestyle": "",
            "marker": ".",
            "markersize": 2,
            "zorder": Z_POINT_INNER,
        },
        "point_outer": {
            "color": "k",
            "linestyle": "",
            "marker": ".",
            "markersize": 5,
            "zorder": Z_POINT_OUTER,
        },
        "point_selected": {
            "color": "yellow",
            "linestyle": "",
            "fillstyle": "none",
            "marker": "o",
            "markersize": 24,
            "markeredgecolor": "yellow",
            "markeredgewidth": 2,
            "zorder": Z_SELECTED,
        },
        "point_highlight": {
            "color": color,
            "linestyle": "",
            "marker": "o",
            "markersize": 30,
            "markeredgecolor": color,
            "markeredgewidth": 3,
            "zorder": Z_POINT_HILITE,
        },
    }

# Generate styles for classes 0 to 9
# use plotter.add_styles(ARC_STYLES)
ARC_STYLES = {str(i): generate_class_style(i) for i in range(10)}


