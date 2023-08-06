import math
from collections import OrderedDict, defaultdict
from typing import List, Tuple, Union, Dict

import cairo
from cairo import Context

from hypertrie.colors import *
from hypertrie.hypertrie2 import HypertrieContext, hash_t, HypertrieNode
from hypertrie.hypertrie_commons import HTKey
from hypertrie.cairo_commons import PlotStyle, rect_with_text, rounded_rectangle, arrow


class DimBox:

    def dim_font_height(self):
        self.ctx.set_font_size(self.ps.dim_font_size)
        (ascent, descent, font_height, max_x_advance, max_y_advance) = self.ctx.font_extents()
        return (ascent - descent)

    def __init__(self, ctx: Context, ps: PlotStyle, x: float, y: float, data, dim: int, n_dim: int):
        self.ctx = ctx
        self.ps = ps
        self.x = x
        self.y = y

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
            dx += self.ps.block_size + self.ps.db_hpadding


def add_referencable_hypertrie_node(ctx: Context, ps: PlotStyle, x: float, y: float,
                                    id: str, ref_count: int, size: int,
                                    data: Union[List[List[Tuple[Union[int, str], Union[int, str]]]],
                                                List[int]], node: HypertrieNode
                                    ):
    rect_with_text(ctx, ps, x + ps.corner_radius, y,
                   text=id,
                   size=ps.block_size,
                   rgba_border=dark_gray,
                   rgba_fill=persian_green,
                   rgba_font=white)
    y_offset = ps.block_size + .5 * ps.line_width
    arrow_start = (x + ps.corner_radius + ps.block_size / 2, y + y_offset)
    arrow_tip = (arrow_start[0], arrow_start[1] + ps.line_width * 2.5)
    arrow(ctx, ps, *arrow_start, *arrow_tip, color=dark_gray_transp, head_length=2 * ps.line_width)
    y_offset += ps.line_width * 2.5
    node_x, node_y = x, y + y_offset
    assert (isinstance(data, list) and len(data) != 0 and isinstance(data[0], int)) == (size == 1)
    if size == 1:

        asset = CompressedHypertrieNode(ctx, ps, node_x, node_y,
                                        id=id,
                                        ref_count=ref_count,
                                        size=size,
                                        data=data)
    else:
        asset = UncomressedHypertrieNode(ctx, ps, node_x, node_y,
                                         id=id,
                                         ref_count=ref_count,
                                         size=size,
                                         data=data)

    asset.draw()

    return asset.width, asset.height + y_offset



class UncomressedHypertrieNode:

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
        return pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height

    def __init__(self, ctx: Context, ps: PlotStyle, x: float, y: float, id: str, ref_count: int, size, data):
        self.ctx = ctx
        self.ps = ps
        self.id = id
        self.ref_count = ref_count
        self.data = data
        self.n_dim = len(data)
        self.size = size
        self.x = x
        self.y = y

        dy = self.ps.sb_padding
        dx = self.ps.sb_padding

        max_dim_box_height = 0

        self.dim_boxes = list()
        for dim, dim_data in enumerate(self.data, 1):
            dim_box = DimBox(self.ctx,
                             self.ps,
                             self.x + dx,
                             self.y + dy,
                             n_dim=self.n_dim,
                             dim=dim,
                             data=dim_data)

            dim_box_width, dim_box_height = dim_box.width, dim_box.height
            self.dim_boxes.append(dim_box)

            max_dim_box_height = max(max_dim_box_height, dim_box_height)

            dx += dim_box_width + self.ps.db_hpadding

        self.mapping_dx = dx

        self.height = dy + max_dim_box_height + self.ps.sb_padding

        pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height = self.text_widths(
            self.ref_count, self.size)

        self.width = self.mapping_dx + pre_width + whitespace_width + post_width + self.ps.padding

    def draw(self):
        rounded_rectangle(self.ctx, self.x, self.y, self.width, self.height, corner_radius=self.ps.corner_radius)

        for dim_box in self.dim_boxes:
            dim_box.draw()

        pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height = self.text_widths(
            self.ref_count, self.size)

        text_dy = font_height + self.ps.corner_radius
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


class CompressedHypertrieNode:

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
        return pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height

    def __init__(self, ctx: Context, ps: PlotStyle, x: float, y: float, id: str, ref_count: int, size, data):
        self.ctx = ctx
        self.ps = ps
        self.id = id
        self.ref_count = ref_count
        self.data = data
        self.n_dim = len(data)
        self.size = size
        self.x = x
        self.y = y

        self.mapping_dx = self.ps.sb_padding + self.ps.block_size + self.ps.sb_hpadding

        self.height = self.ps.sb_padding + self.ps.block_size * self.n_dim + self.ps.sb_padding

        pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height = self.text_widths(
            self.ref_count, self.size)

        self.width = self.mapping_dx + pre_width + whitespace_width + post_width + self.ps.padding

    def draw(self):
        rounded_rectangle(self.ctx, self.x, self.y, self.width, self.height, corner_radius=self.ps.corner_radius)

        dx = self.ps.sb_padding
        dy = self.ps.sb_padding

        for key_part in self.data:
            rect_with_text(self.ctx, self.ps, self.x + dx, self.y + dy,
                           text=key_part,
                           size=self.ps.block_size,
                           rgba_border=white,
                           rgba_font=white,
                           rgba_fill=dark_grey_blue
                           )
            dy += self.ps.block_size

        pre_width, whitespace_width, post_width, r_width, z_width, ref_width, size_width, ref_text, size_text, font_height = self.text_widths(
            self.ref_count, self.size)

        text_dy = font_height + self.ps.corner_radius
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


def cairo_draw_hypertrie2_context(ctx: Context, ps: PlotStyle, ht_ctx: HypertrieContext, level_dxs: Dict[int, float] = None):
    ctx.select_font_face(ps.font, cairo.FONT_SLANT_NORMAL,
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(ps.font_size)
    ctx.set_line_width(ps.line_width)

    node: HypertrieNode
    next_hash2id = OrderedDict()

    next_id = "A"

    def inc_id():
        nonlocal next_id
        next_id = chr(ord(next_id) + 1)

    def map_id(child: Union[int, hash_t]) -> str:
        nonlocal next_hash2id
        if type(child) is hash_t:
            if child not in next_hash2id:
                next_hash2id[child] = next_id
                inc_id()
            return next_hash2id[child]
        else:
            return child

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

        nodes: Dict[hash_t, HypertrieNode] = ht_ctx.storage[depth - 1]
        hash2id = next_hash2id.copy()
        next_hash2id.clear()
        if depth != ht_ctx.max_depth:
            assert len(nodes) == len(hash2id)

        for node_hash, node in nodes.items():
            if node_hash not in hash2id:
                hash2id[node_hash] = next_id
                id = next_id
                inc_id()
            else:
                id = hash2id[node_hash]

            if node.size == 1:
                assert depth != 1
                data = list(node.children)
            else:
                data = [list() for _ in range(depth)]

                for dim in range(depth):
                    if depth > 1:
                        entries = sorted(node.children[dim].items())
                        data[dim] = [(key_part, map_id(child)) for key_part, child in entries]
                    else:
                        entries = sorted(node.children[dim])
                        data[dim] = [(key_part, "") for key_part in entries]

            tmp_x_offset, tmp_y_offset = add_referencable_hypertrie_node(
                ctx, ps,
                x + x_offset, y,
                id=id,
                size=node.size,
                ref_count=node.count,
                data=data,
                node=node)
            y_offset = max(y_offset, tmp_y_offset)
            x_offset += tmp_x_offset + 15
        y_offset += 15
        level_dxs[depth] = x + x_offset - 15
        x_max = max(x_max, level_dxs[depth])
    y_offset -= 15
    return x_max, y + y_offset, level_dxs