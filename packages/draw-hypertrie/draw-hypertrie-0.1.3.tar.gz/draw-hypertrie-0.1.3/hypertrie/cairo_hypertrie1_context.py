import math
from collections import OrderedDict, defaultdict
from typing import List, Tuple, Union, Dict

import cairo
from cairo import Context

from hypertrie.colors import *
from hypertrie.hypertrie1 import Hypertrie1Context, SliceKey, Hypertrie1Node

from hypertrie.cairo_hypertrie2_context import DimBox
from hypertrie.hypertrie_commons import HTKey, slice_key2str, next_slice_key
from hypertrie.cairo_commons import PlotStyle, rect_with_text, rounded_rectangle, arrow


class References:
    def __init__(self):
        self.source: Dict[SliceKey, List[Tuple[float, float]]] = defaultdict(list)
        self.destination: Dict[SliceKey, Tuple[float, float]] = dict()


class DimBox1:

    def dim_font_height(self):
        self.ctx.set_font_size(self.ps.dim_font_size)
        (ascent, descent, font_height, max_x_advance, max_y_advance) = self.ctx.font_extents()
        return (ascent - descent)

    def __init__(self, ctx: Context, ps: PlotStyle, refs: References, x: float, y: float, data, dim: int, n_dim: int,
                 slice_key: SliceKey):
        self.ctx = ctx
        self.ps = ps
        self.refs = refs
        self.x = x
        self.y = y

        self.slice_key = slice_key

        self.font_height = self.dim_font_height()
        self.arrow_dx = self.ps.block_size / 2
        self.arrow_length = self.ps.line_width * 3

        self.data = data
        self.dim = dim
        self.n_dim = n_dim
        self.width = len(data) * self.ps.block_size + (len(data) + 1) * self.ps.db_hpadding
        self.height = self.ps.sb_hpadding + self.dim_font_height() + self.ps.sb_hpadding + \
                      +self.ps.block_size + \
                      (self.n_dim > 1) * (self.ps.block_size + self.arrow_length + self.ps.line_width / 2) + \
                      +  self.ps.db_hpadding

    def draw(self):
        # draw background
        rounded_rectangle(self.ctx, self.x, self.y,
                          width=self.width,
                          height=self.height,
                          fill_color=desert_sand,
                          border_color=white,
                          corner_radius=self.ps.corner_radius
                          )

        # draw dim x text
        dx = self.ps.db_hpadding
        text = f"dim {self.dim}"
        self.ctx.set_font_size(self.ps.dim_font_size)
        self.ctx.move_to(self.x + dx, self.y + self.ps.sb_hpadding + self.dim_font_height())
        self.ctx.set_source_rgba(*white)
        self.ctx.show_text(text)

        ref_points = []

        # draw mapping
        for (key_part, value) in self.data:
            dy = self.ps.sb_hpadding + self.dim_font_height() + self.ps.sb_hpadding
            rect_with_text(self.ctx, self.ps, self.x + dx, self.y + dy,
                           text=key_part,
                           size=self.ps.block_size,
                           rgba_border=white,
                           rgba_font=white,
                           rgba_fill=dark_grey_blue
                           )
            if self.n_dim > 1:
                dy += self.ps.block_size
                arrow_start = (self.x + dx + self.arrow_dx, self.y + dy)
                arrow_tip = (arrow_start[0], arrow_start[1] + self.arrow_length)
                arrow(self.ctx, self.ps, *arrow_start, *arrow_tip, color=white, head_length=2 * self.ps.line_width)

                dy += self.arrow_length + self.ps.line_width / 2
                rect_with_text(self.ctx, self.ps, self.x + dx, self.y + dy,
                               text=value,
                               size=self.ps.block_size,
                               rgba_border=white,
                               rgba_font=white,
                               rgba_fill=dark_grey_blue if type(value) is int else light_persian_green
                               )
                self.refs.source[next_slice_key(self.slice_key, self.dim - 1, key_part)].append(
                    (self.x + dx + .5 * self.ps.block_size, self.y + dy + 0.5 * self.ps.block_size))
            dx += self.ps.block_size + self.ps.db_hpadding


class Cairo_Hypertrie1Node:

    def text_widths(self, ref_count, size):
        self.ctx.set_font_size(self.ps.font_size)
        ascent, descent, font_height, max_x_advance, max_y_advance = self.ctx.font_extents()
        ref_text = f"{ref_count}"
        size_text = f"{size}"
        r_width = self.ctx.text_extents(str("r:")).x_advance
        z_width = self.ctx.text_extents(str("z:")).x_advance
        ref_width = self.ctx.text_extents(ref_text).x_advance
        size_width = self.ctx.text_extents(size_text).x_advance
        whitespace_width = self.ctx.text_extents(" ").x_advance
        pre_width = max(r_width, z_width)
        post_width = max(ref_width, size_width)
        return pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height, ascent, descent

    def __init__(self, ctx: Context, ps: PlotStyle, refs: References, x: float, y: float, id: HTKey, ref_count: int,
                 size,
                 data):
        self.ctx = ctx
        self.ps = ps
        self.refs = refs
        self.id = id
        self.id_str = slice_key2str(self.id)
        self.ref_count = ref_count
        self.data = data
        self.n_dim = len(data)
        self.size = size
        self.x = x
        self.y = y

        pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height, ascent, descent = self.text_widths(
            self.ref_count, self.size)

        dy = self.ps.padding
        dx = self.ps.sb_padding

        dy += ascent
        self.slice_key_dx = dx
        self.slice_key_dy = dy

        dy += self.ps.sb_hpadding + descent

        max_dim_box_height = 0

        self.dim_boxes = list()
        for dim, dim_data in enumerate(self.data, 1):
            dim_box = DimBox1(self.ctx, self.ps, self.refs,
                              self.x + dx, self.y + dy,
                              slice_key=self.id,
                              n_dim=self.n_dim,
                              dim=dim,
                              data=dim_data)

            dim_box_width, dim_box_height = dim_box.width, dim_box.height
            self.dim_boxes.append(dim_box)

            max_dim_box_height = max(max_dim_box_height, dim_box_height)

            dx += dim_box_width + self.ps.db_hpadding

        self.mapping_dx = dx

        self.height = dy + max_dim_box_height + self.ps.sb_padding

        self.width = self.mapping_dx + pre_width + whitespace_width + post_width + self.ps.padding
        self.refs.destination[self.id] = (self.x + .5 * self.width, self.y)

    def draw(self):
        rounded_rectangle(self.ctx, self.x, self.y, self.width, self.height, corner_radius=self.ps.corner_radius)

        self.ctx.set_source_rgba(*dark_gray)
        self.ctx.set_font_size(self.ps.font_size)
        text_offset = self.width - self.ctx.text_extents(self.id_str).x_advance - self.ps.padding
        self.ctx.move_to(self.x + text_offset, self.y + self.slice_key_dy)
        self.ctx.show_text(self.id_str)

        for dim_box in self.dim_boxes:
            dim_box.draw()

        pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height, ascent, descent = self.text_widths(
            self.ref_count, self.size)

        text_dy = self.slice_key_dy + font_height + self.ps.corner_radius
        self.ctx.set_source_rgba(*dark_gray)
        self.ctx.move_to(self.x + self.mapping_dx + (pre_width - r_width), self.y + text_dy)
        self.ctx.show_text("r:")
        self.ctx.move_to(self.x + self.mapping_dx + pre_width + whitespace_width + (post_width - ref_width),
                         self.y + text_dy)
        self.ctx.show_text(ref_text)

        text_dy += font_height
        self.ctx.move_to(self.x + self.mapping_dx + (pre_width - z_width), self.y + text_dy)
        self.ctx.show_text("z:")
        self.ctx.move_to(self.x + self.mapping_dx + pre_width + whitespace_width + (post_width - size_width),
                         self.y + text_dy)
        self.ctx.show_text(size_text)


def add_referencable_hypertrie_node(ctx: Context, ps: PlotStyle, refs: References, x: float, y: float,
                                    id: HTKey, ref_count: int, size: int,
                                    data: Union[List[List[Tuple[Union[int, str], Union[int, str]]]],
                                                List[int]]
                                    ):
    # assert (isinstance(data, list) and len(data) != 0 and isinstance(data[0], int)) == (size == 1)
    asset = Cairo_Hypertrie1Node(ctx, ps, refs, x, y,
                                 id=id,
                                 ref_count=ref_count,
                                 size=size,
                                 data=data)

    asset.draw()

    return asset.width, asset.height


def cairo_draw_hypertrie1_context(ctx: Context, ps: PlotStyle, ht_ctx: Hypertrie1Context, level_dxs: Dict[int, float] = None):
    ctx.select_font_face(ps.font, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(ps.font_size)
    ctx.set_line_width(ps.line_width)

    node: Hypertrie1Node

    refs = References()

    x = 0
    y = ps.line_width / 2
    x_max = x
    x_offset = 0
    y_offset = 0
    if level_dxs is None:
        level_dxs: Dict[int, float] = defaultdict(float)
    for depth in range(ht_ctx.max_depth, 0, -1):

        x_offset = level_dxs[depth]
        y += y_offset
        y_offset = 0

        nodes: Dict[SliceKey, Hypertrie1Node] = ht_ctx.storage[depth - 1]

        for slice_key, node in sorted(nodes.items(),
                                      key=lambda p: tuple(
                                          entry if entry is not None else float("inf") for entry in p[0])):
            id = slice_key

            data = [list() for _ in range(depth)]

            for dim in range(depth):
                if depth > 1:
                    entries = sorted(node.children[dim].items())
                    data[dim] = [(key_part, "·") for key_part, child in entries]
                else:
                    entries = sorted(node.children[dim])
                    data[dim] = [(key_part, "") for key_part in entries]

            tmp_x_offset, y_offset = add_referencable_hypertrie_node(
                ctx, ps, refs,
                x + x_offset, y,
                id=id,
                size=node.size,
                ref_count=1 if depth != 1 else 2,
                data=data)
            x_offset += tmp_x_offset + 15
        y_offset += 15
        if depth == 2:
            y_offset += 45
        level_dxs[depth] = x + x_offset - 15
        x_max = max(x_max, level_dxs[depth])
    y_offset -= 15
    for slice_key, arrow_destination in refs.destination.items():
        for arrow_source in refs.source[slice_key]:
            direction = (arrow_destination[0] - arrow_source[0], arrow_destination[1] - arrow_source[1])
            length = math.sqrt(direction[0]**2 + direction[1]**2)
            direction = (direction[0]/length, direction[1]/length)
            offseted_arrow_source = (arrow_source[0] + direction[0] * 1.5* ps.line_width, arrow_source[1] + direction[1] * 1.5* ps.line_width)
            arrow(ctx, ps, *offseted_arrow_source, *arrow_destination,
                  color=dark_gray_transp,
                  head_length=ps.line_width*4
                  )
    return x_max, y + y_offset, level_dxs