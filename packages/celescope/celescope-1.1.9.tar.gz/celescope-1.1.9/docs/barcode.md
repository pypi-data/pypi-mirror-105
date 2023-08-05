# barcode

## Features
- Demultiplex barcodes.
- Filter invalid R1 reads, which includes:
    - Reads without linker: the mismatch between linkers and all linkers in the whitelist is greater than 2.  
    - Reads without correct barcode: the mismatch between barcodes and all barcodes in the whitelist is greater than 1.  
    - Reads without polyT: the number of T bases in the defined polyT region is less than 10.
    - Low quality reads: low sequencing quality in barcode and UMI regions.(`--lowQual` and `--lowNum`)

## Input
- Paired-end FASTQ files.

## Output
- `{sample}_2.fq` Demultiplexed R2 reads. Barcode and UMI are contained in the read name. The format of the read name is `{barcode}_{UMI}_{read ID}`.

- `fastqc.zip` `fastqc.html` Fastqc results.

## Parameters

`--fq1` Required, FASTQ R1 reads. Multiple FASTQ files are seperated by comma. 

`--fq2` Required, FASTQ R2 reads. Multiple FASTQ files are seperated by comma. 

`--chemistry` Predefined (pattern, barcode whitelist, linker whitelist) combinations. Can be one of:  
- `auto` Default value. Used for Singleron GEXSCOPE libraries >= scopeV2 and automatically detects the combinations.  
- `scopeV1` Used for legacy Singleron GEXSCOPE scopeV1 libraries.  
- `customized` Used for user defined combinations. You need to provide `pattern`, `whitelist` and `linker` at the same time.

`--pattern` The pattern of R1 reads, e.g. `C8L16C8L16C8L1U12T18`. The number after the letter represents the number of bases.  
- `C`: cell barcode  
- `L`: linker(common sequences)  
- `U`: UMI    
- `T`: poly T

`--whitelist` Cell barcode whitelist file path, one cell barcode per line.

`--linker` Linker whitelist file path, one linker per line.

`--lowQual` Default `0`. Bases in cell barcode and UMI whose phred value are lower than lowQual will be regarded as low-quality bases.

`--lowNum` Default `2`. The maximum allowed lowQual bases in cell barcode and UMI.

`--nopolyT` Outputs R1 reads without polyT.
    
`--noLinker` Outputs R1 reads without correct linker.

`--allowNoPolyT` Allow reads without polyT.

`--allowNoLinker` Allow reads with incorrect linker.

`--gzip` Output gzipped fastq.

## Metrics
-  Raw Reads: total read pairs from FASTQ files.

-  Valid Reads: reads pass filtering(filtered: reads without poly T, reads without linker, reads without correct barcode or low quality reads).

-  Q30 of Barcodes: percent of barcode base pairs with quality scores over Q30.

-  Q30 of UMIs: percent of UMI base pairs with quality scores over Q30.