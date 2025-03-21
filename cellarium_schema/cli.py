import logging
import sys

import click


logger = logging.getLogger("cellarium_schema")


@click.group(
    name="schema",
    subcommand_metavar="COMMAND <args>",
    short_help="Apply and validate the cellxgene data integration schema to an h5ad file.",
    context_settings=dict(max_content_width=85, help_option_names=["-h", "--help"]),
)
@click.option("-v", "--verbose", help="When present will set logging level to debug", is_flag=True)
def schema_cli(verbose):
    logging.basicConfig(level=logging.ERROR)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)


@schema_cli.command(
    name="validate",
    short_help="Check that an h5ad follows the cellxgene data integration schema.",
    help="Check that an h5ad follows the cellxgene data integration schema. If validation fails this command will "
    "return an exit status of 1 otherwise 0. When the '--add-labels <FILE>' tag is present, the command will add "
    "ontology/gene labels based on IDs and write them to a new h5ad.",
)
@click.argument("h5ad_file", nargs=1, type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-a",
    "--add-labels",
    "add_labels_file",
    help="When present it will add labels to genes and ontologies based on IDs",
    required=False,
    default=None,
    type=click.Path(exists=False, dir_okay=False, writable=True),
)
@click.option(
    "-v",
    "--gencode-version",
    "gencode_version",
    help="Can specify either 43 or 44 for the version of human gencode gene annotations.",
    required=False,
    default=44,
    type=click.INT,
)
@click.option("-i", "--ignore-labels", help="Ignore ontology labels when validating", is_flag=True)
def schema_validate(h5ad_file, add_labels_file, gencode_version, ignore_labels):
    # Imports are very slow so we defer loading until Click arg validation has passed
    logger.info("Loading dependencies")
    try:
        import anndata  # noqa: F401
    except ImportError:
        raise click.ClickException("cellarium-schema requires anndata") from None

    logger.info("Loading validator modules")
    from .validate import validate

    is_valid, _, _ = validate(h5ad_file, add_labels_file, gencode_version=gencode_version, ignore_labels=ignore_labels)
    if is_valid:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    schema_cli()
