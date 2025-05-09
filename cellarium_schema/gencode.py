import gzip
import logging
import os
import warnings

from cellxgene_schema.gencode import GeneChecker, SupportedOrganisms
from cellxgene_schema.env import GENCODE_DIR as CZI_GENCODE_DIR

from .env import GENCODE_DIR

logger = logging.getLogger(__name__)


class ExtendedGeneChecker(GeneChecker):
    """Handles checking gene ids, retrieves symbols"""

    GENE_FILES = GeneChecker.GENE_FILES
    GENE_FILES[SupportedOrganisms.HOMO_SAPIENS] = {
        "v43": os.path.join(GENCODE_DIR, "genes_homo_sapiens_v43.csv.gz"),
        "v44": os.path.join(CZI_GENCODE_DIR, "genes_homo_sapiens.csv.gz"),
    }

    def __init__(self, species: SupportedOrganisms, gencode_version: int | None):
        """
        :param enum.Enum.SupportedSpecies species: item from SupportedOrganisms
        """
        if species not in self.GENE_FILES:
            raise ValueError(f"{species} not supported.")

        self.species = species
        self.gencode_version = gencode_version
        self.gene_dict = {}
        if self.species.value == "NCBITaxon:9606":  # human
            if self.gencode_version == 43:
                file = self.GENE_FILES[species]["v43"]
            elif self.gencode_version == 44:
                file = self.GENE_FILES[species]["v44"]
            else:
                raise ValueError(f"gencode_version must be in [43, 44]: got {self.gencode_version}")
        else:
            if self.gencode_version is not None:
                warnings.warn("gencode_version is ignored if species is not HOMO_SAPIENS", UserWarning)
            file = self.GENE_FILES[species]
        logger.info(f"using file {file}")

        with gzip.open(file, "rt") as genes:
            for gene in genes:
                gene = gene.rstrip().split(",")  # type: ignore
                gene_id = gene[0]
                gene_label = gene[1]
                gene_length = int(gene[3])
                gene_type = gene[4]

                self.gene_dict[gene_id] = (gene_label, gene_length, gene_type)
