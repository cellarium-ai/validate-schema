import logging
import os
from datetime import datetime
from typing import Tuple, Union

import dask

from cellxgene_schema.validate import Validator
from cellxgene_schema.gencode import get_organism_from_feature_id

from .gencode import ExtendedGeneChecker


logger = logging.getLogger(__name__)


class ExtendedValidator(Validator):
    """Handles validation of AnnData"""

    def __init__(self, gencode_version: int, **kwargs):
        super().__init__(**kwargs)
        self.gencode_version = gencode_version

    def _validate_feature_id(self, feature_id: str, df_name: str):
        """
        Validates a feature id, i.e. checks that it's present in the reference
        If there are any errors, it adds them to self.errors and adds it to the list of invalid features

        :param str feature_id: the feature id to be validated
        :param str df_name: name of dataframe the feauter id comes from (var or raw.var)

        :rtype none
        """

        organism = get_organism_from_feature_id(feature_id)

        if not organism:
            self.errors.append(
                f"Could not infer organism from feature ID '{feature_id}' in '{df_name}', "
                f"make sure it is a valid ID."
            )
            return
        
        if organism not in self.gene_checkers:
            self.gene_checkers[organism] = ExtendedGeneChecker(organism, gencode_version=self.gencode_version)

        if not self.gene_checkers[organism].is_valid_id(feature_id):
            self.errors.append(f"'{feature_id}' is not a valid feature ID in '{df_name}'.")

        return


def validate(
    h5ad_path: Union[str, bytes, os.PathLike],
    add_labels_file: str = None,
    gencode_version: int = 44,
    ignore_labels: bool = False,
) -> Tuple[bool, list, bool]:
    from cellxgene_schema.write_labels import AnnDataLabelAppender

    """
    Entry point for validation.

    :param Union[str, bytes, os.PathLike] h5ad_path: Path to h5ad file to validate
    :param str add_labels_file: Path to new h5ad file with ontology/gene labels added
    :param int gencode_version: Version of human gencode gene annotations to use (default 44)
    :param bool ignore_labels: When True, will ignore ontology labels when validating

    :return (True, [], False) if successful validation, (False, [list_of_errors], False) otherwise;
    last bool is for seurat convertability which is deprecated / unused
    :rtype tuple
    """

    # Perform validation
    start = datetime.now()
    validator = ExtendedValidator(
        gencode_version=gencode_version,
        ignore_labels=ignore_labels,
    )

    validator.validate_adata(h5ad_path)
    logger.info(f"Validation complete in {datetime.now() - start} with status is_valid={validator.is_valid}")

    # Stop if validation was unsuccessful
    if not validator.is_valid:
        return False, validator.errors, validator.is_seurat_convertible

    if add_labels_file:
        label_start = datetime.now()
        writer = AnnDataLabelAppender(validator)
        writer.write_labels(add_labels_file)
        logger.info(
            f"H5AD label writing complete in {datetime.now() - label_start}, was_writing_successful: "
            f"{writer.was_writing_successful}"
        )

        return (
            validator.is_valid and writer.was_writing_successful,
            validator.errors + writer.errors,
            validator.is_seurat_convertible,
        )

    return True, validator.errors, validator.is_seurat_convertible
