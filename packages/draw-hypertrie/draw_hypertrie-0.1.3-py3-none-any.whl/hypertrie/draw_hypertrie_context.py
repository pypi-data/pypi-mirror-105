from typing import Optional, Union

from hypertrie.cairo_hypertrie2_context import PlotStyle
from hypertrie.hypertrie1 import Hypertrie1Context
from hypertrie.hypertrie2 import HypertrieContext


def draw_hypertrie_context(ht_ctx: Union[Hypertrie1Context, HypertrieContext], name: Optional[str] = None,
                           ps: Optional[PlotStyle] = None):
    version = 2 if type(ht_ctx) is HypertrieContext else 1
    if version == 1:
        from hypertrie.cairo_hypertrie1_context import cairo_draw_hypertrie1_context
        draw = cairo_draw_hypertrie1_context
    elif version == 2:
        from hypertrie.cairo_hypertrie2_context import cairo_draw_hypertrie2_context
        draw = cairo_draw_hypertrie2_context

    if ps is None:
        ps = PlotStyle(font_size=15,
                       dim_font_size=9,
                       )
    if name is None:
        import random
        name = "hypertrie2_plot_{}".format(random.randint(0, 10 ** 10))

    tmp_file = f"{name}.tmp.pdf"
    import cairo

    yield f"Preparing {name}"
    with cairo.PDFSurface(tmp_file, 500, 500) as surf_tmp:
        ctx = cairo.Context(surf_tmp)
        max_x, max_y, level_dxs = draw(ctx, ps, ht_ctx)
    from pathlib import Path
    Path(tmp_file).unlink()
    from math import ceil
    max_x = ceil(max_x)
    max_y = ceil(max_y)
    yield ""

    level_dxs = {level: .5 * max_x - .5 * dx for level, dx in level_dxs.items()}

    pdf_name = f"{name}.pdf"
    yield pdf_name
    with cairo.PDFSurface(pdf_name, max_x, max_y) as surf_pdf:
        ctx = cairo.Context(surf_pdf)
        draw(ctx, ps, ht_ctx, level_dxs.copy())
        ctx.save()
    yield ""

    svg_name = f"{name}.svg"
    yield svg_name
    with cairo.SVGSurface(svg_name, max_x, max_y) as surf_svg:
        ctx = cairo.Context(surf_svg)
        draw(ctx, ps, ht_ctx, level_dxs.copy())
        ctx.save()
    yield ""

    scale_png = 4
    png_name = f"{name}.png"
    yield png_name
    with cairo.ImageSurface(cairo.FORMAT_ARGB32, max_x * scale_png, max_y * scale_png) as surf_png:
        surf_png.set_device_scale(scale_png, scale_png)
        ctx = cairo.Context(surf_png)

        draw(ctx, ps, ht_ctx, level_dxs.copy())
        ctx.save()
        surf_png.flush()

        surf_png.write_to_png(png_name)

    yield ""
