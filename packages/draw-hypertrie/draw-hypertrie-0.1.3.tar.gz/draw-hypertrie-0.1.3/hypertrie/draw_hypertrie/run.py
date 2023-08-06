import csv
from typing import Optional, NamedTuple

import click

from hypertrie.draw_hypertrie_context import draw_hypertrie_context
from hypertrie.hypertrie1 import Hypertrie1Context
from hypertrie.hypertrie2 import HypertrieContext


class OutputCSVRows(NamedTuple):
    format: str
    dataset: str
    triplestore: str
    queryID: int
    qps: float
    succeeded: bool
    failed: bool
    httpCode: int
    errorMessage: str
    time: float
    contentLength: int
    parsingSucceeded: bool
    numberOfVariables: Optional[int]
    numberOfSolutions: Optional[int]
    numberOfBindings: Optional[int]
    resultParsingTime: Optional[float]
    parsingErrorMessage: Optional[str]


@click.command()
@click.option('--output', '-o', required=False, type=str, default=None,
              help='Filename or path of generate PNG, SVG and PDF files. '
                   'By default the name and location of the input file is used.')
@click.argument('tsv_file', type=click.File('r'))
def cli(tsv_file, output):
    """
    Provide a tab-separated file (TSV) containing integer IDs in three rows.
    """
    click.echo(f"Reading TSV file {tsv_file.name} ... ", nl=False)
    tsv_reader = csv.reader(tsv_file, delimiter='\t')
    keys = list(set(tuple(int(cell) for cell in row) for row in tsv_reader))
    assert all(len(key) == 3 for key in keys)
    click.echo(f"done.", nl=True)

    click.echo(f"Generating hypertries:")
    click.echo(f"\t v1 ... ", nl=False)
    ht_v1_ctx = Hypertrie1Context()
    ht_v1_ctx.create_hypertrie(keys=keys, depth=3)
    click.echo(f"done.", nl=True)

    click.echo(f"\t v2 ... ", nl=False)
    ht_v2_ctx = HypertrieContext()
    ht_v2_ctx.create_hypertrie(keys=keys, depth=3)
    click.echo(f"done.", nl=True)

    click.echo(f"Drawing hypertries:")
    from pathlib import Path
    output_name = output if output is not None else Path(tsv_file.name).stem

    import itertools
    for file_name in itertools.chain(draw_hypertrie_context(ht_ctx=ht_v1_ctx, name=output_name + "-v1"),
                                     draw_hypertrie_context(ht_ctx=ht_v2_ctx, name=output_name + "-v2")):
        if file_name != "":
            click.echo(f"\t{file_name} ... ", nl=False)
        else:
            click.echo(f"done.", nl=True)


if __name__ == '__main__':
    cli()
