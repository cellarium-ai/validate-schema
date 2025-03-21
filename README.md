# validate-schema

Some additional flexibility for [CZI single-cell-curation](https://github.com/chanzuckerberg/single-cell-curation).

In particular, this repository adds the ability to use different gencode versions for human data: v43 and v44.

This repository depends strongly on `single-cell-curation`, and just extends it in a minimal way.

## Usage

```bash
cellarium-schema validate test.h5ad
```

is identical to

```bash
cellxgene-schema validate test.h5ad
```

But for human data you can additionally specify the gencode version (in [43, 44] where 44 is the current `cellxgene-schema` default) as

```bash
cellarium-schema validate --gencode-version 43 test.h5ad
```

Similar to the `cellxgene-schema` tool, you can add human-readable labels based on ontology terms using

```bash
cellarium-schema validate --gencode-version 43 --add-labels test_labeled.h5ad test.h5ad
```
