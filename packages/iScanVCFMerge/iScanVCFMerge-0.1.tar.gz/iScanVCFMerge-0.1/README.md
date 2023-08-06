# iScanVCFMerge
        
## Installation

iScanVCFMerge has been tested with Python 3.9.2 on MacOS Big Sur 11.3 and on Ubuntu 21.04. 

### Option 1: Github clone and run with Python3

    git clone "https://github.com/baneslab/iScanVCFMerge.git"
    $ cd iScanVCFMerge
    $ python3 iScanVCFMerge.py

If running the script directly with Python, you may also need to install the required packages, _e.g._:

    python3 -m pip install pandas
    
### Run Option 2: Install with pip

    pip install iScanVCFMerge

or

    python3 -m pip install iScanVCFMerge

## Usage

    iScanVCFMerge [-h] -R <reference_vcf> -I <iScan_vcf> -O <output_directory>

Optional arguments:

    -h, --help                  Show the help message
    -R, --reference_vcf         Reference VCF file against which iScan file will be merged (.vcf or .vcf.gz)
    -I, --iScan_vcf             iScan VCF file  (.vcf or .vcf.gz)
    -O, --output_directory      Name of the output directory (will be created if it doesn't exist)

## Citation

Please cite the use of this software as follows:

> Fountain, E. D., Zhou, L-C., Karklus, A., Liu, Q-X., Meyers, J., Fontanilla, I. K., Rafael, E. F., Yu, J-Y., Zhang, Q., Zhu, X-L., Pei, E-L., Yuan, Y-H. and Banes, G. L. (2021). Cross-species application of Illumina iScan microarrays for cost-effective, high-throughput SNP discovery. Frontiers in Ecology and Evolution, doi: 10.3389/fevo.2021.629252.