from cairo import Context

from hypertrie.colors import *


class PlotStyle:
    """
    Defines styles for plot
    """

    def __init__(self,
                 padding=8,
                 hpadding=None,
                 block_size=25,
                 corner_radius=None,
                 dim_tag_size=None,
                 line_width=2,
                 font="DeJaVuSans",
                 font_size=None,
                 dim_font_size=None
                 ):
        self.padding = padding

        if hpadding is None:
            self.hpadding = self.padding / 2
        else:
            self.hpadding = hpadding

        self.block_size = block_size

        if dim_tag_size is None:
            self.dim_tag_size = self.block_size / 25 * 15
        else:
            self.dim_tag_size = dim_tag_size

        if corner_radius is None:
            self.corner_radius = self.block_size / 5
        else:
            self.corner_radius = corner_radius

        self.line_width = line_width

        if font_size is None:
            self.font_size = self.block_size / 25 * 15
        else:
            self.font_size = font_size

        self.font = font

        if dim_font_size is None:
            self.dim_font_size = self.dim_tag_size / 25 * 19
        else:
            self.dim_font_size = dim_font_size

        self.sb_padding = self.padding + self.line_width / 2
        self.db_padding = self.padding + self.line_width
        self.sb_hpadding = self.hpadding + self.line_width / 2
        self.db_hpadding = self.hpadding + self.line_width

        self.SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        self.SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def rounded_rectangle(ctx: Context,
                      x: float, y: float,
                      width, height,
                      fill_color=light_gray_transp,
                      border_color=None,
                      aspect=1.0,
                      corner_radius=None):
    if corner_radius is None:
        corner_radius = height / 10

    from math import pi
    radius = corner_radius / aspect
    degrees = pi / 180.0

    ctx.new_sub_path()
    ctx.arc(x + width - radius, y + radius, radius, -90 * degrees, 0 * degrees)
    ctx.arc(x + width - radius, y + height - radius, radius, 0 * degrees, 90 * degrees)
    ctx.arc(x + radius, y + height - radius, radius, 90 * degrees, 180 * degrees)
    ctx.arc(x + radius, y + radius, radius, 180 * degrees, 270 * degrees)
    ctx.close_path()

    ctx.set_source_rgba(*fill_color)
    if border_color is None:
        ctx.fill()
    else:
        ctx.fill_preserve()
        ctx.set_source_rgba(*border_color)
        ctx.stroke()


def arrow(ctx: Context, ps: PlotStyle,
          start_x, start_y,
          end_x, end_y,
          color=black, head_length=4):
    head_degree = 0.6
    import math
    angle = math.atan2(end_y - start_y, end_x - start_x) + math.pi

    x1 = end_x + head_length * math.cos(angle - head_degree)
    y1 = end_y + head_length * math.sin(angle - head_degree)
    x2 = end_x + head_length * math.cos(angle + head_degree)
    y2 = end_y + head_length * math.sin(angle + head_degree)
    xm = (x1 + x2) / 2
    ym = (y1 + y2) / 2
    # rectangle

    ctx.set_line_width(ps.line_width)
    ctx.set_source_rgba(*color)

    ctx.new_sub_path()
    ctx.move_to(end_x, end_y)
    ctx.line_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.line_to(end_x, end_y)
    ctx.close_path()
    ctx.fill()

    ctx.move_to(xm, ym)
    ctx.line_to(start_x, start_y)
    ctx.stroke()


def rect_with_text(ctx: Context, ps: PlotStyle,
                   x: float,
                   y: float,
                   text,
                   size: float,
                   rgba_border=black,
                   rgba_font=black,
                   rgba_fill=(0, 0, 0, 0)):
    # rectangle
    size = float(size)
    ctx.set_line_width(ps.line_width)
    ctx.set_font_size(size / 25 * 17)

    ctx.rectangle(x, y, size, size)
    if rgba_fill is not None:
        ctx.set_source_rgba(*rgba_fill)
        ctx.fill_preserve()
    ctx.set_source_rgba(*rgba_border)
    ctx.stroke()

    # text
    (x_, y_, width, height, dx, dy) = ctx.text_extents(str(text))
    (ascent, descent, height, max_x_advance, max_y_advance) = ctx.font_extents()

    ctx.move_to(x + (size / 2) - dx / 2, y + (size / 2) + ((ascent - descent) / 2))
    ctx.set_source_rgba(*rgba_font)
    ctx.show_text(str(text))
