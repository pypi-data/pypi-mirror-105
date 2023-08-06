#!/usr/bin/python3
'''iScanVCFMerge v0.1 build 2021-05-09'''

# MIT License
# Copyright © 2021 Banes, G. L., Meyers, J. and Fountain, E. D.

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software
# without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to
# whom the Software is furnished to do so, subject to the
# following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import time
import argparse
import io
import os
import pathlib
import gzip
from datetime import date
import pandas as pd
startTime = time.time()

def main():

  print("\033[1m" + "\n")
  print(r"  _ ____               __     _____" +
        "_ _____ __  __                      ")
  print(r" (_) ___|  ___ __ _ _ _\ \   / / __" +
        r"_|  ___|  \/  | ___ _ __ __ _  ___  ")
  print(r" | \___ \ / __/ _` | '_ \ \ / / |  " +
        r" | |_  | |\/| |/ _ \ '__/ _` |/ _ \ ")
  print(r" | |___) | (_| (_| | | | \ V /| |__" +
        r"_|  _| | |  | |  __/ | | (_| |  __/ ")
  print(r" |_|____/ \___\__,_|_| |_|\_/  \___" +
        r"_|_|   |_|  |_|\___|_|  \__, |\___| ")
  print("      https://www.github.com/banesla" +
        "b" + " \u2022 " + "build 2021-05-09 " +
        "\033[0m" + r"  |___/")

  print("\n" + "      Fountain, E. D., Zhou," +
        " L., Karklus, A., Liu, Q., Meyers, J., ")
  print("    Fontanilla, I. K. C., Rafael, E. F., " +
        "Yu, J., Zhang, Q., Zhu, X.,")
  print("Yuan, Y. and Banes, G. L. (2021). C" +
        "ross-species application of Illumina")
  print("  iScan microarrays for cost-effecti" +
        "ve, high-throughput SNP discovery. ")
  print("\t\t\033[1m" + "  Frontiers in Ecology" +
        " and Evolution." + "\033[0m")
  print ("               https://doi.org/10.3389/fev" +
        "o.2021.629252" + "\n")

  # #####################################################################
  # PROCESS COMMAND LINE VARIABLES
  # #####################################################################

  # Process command line variables

  parser = argparse.ArgumentParser()
  parser.add_argument('-R', '--reference_vcf', help='Path to your refe' +
                      'rence VCF file (.vcf or .vcf.gz)', required=True)
  parser.add_argument('-I', '--iScan_vcf', help='Path to your iScan VC' +
                      'F file (.vcf or .vcf.gz)', required=True)
  parser.add_argument('-O', '--output_directory', help='Name of the ou' +
                      'tput directory', required=True)
  args = vars(parser.parse_args())

  reference_file = args['reference_vcf']
  iScan_file = args['iScan_vcf']
  output_directory = args['output_directory']

  print("****************************************" +
        "******************************")
  print("\033[1m" +
        "User input variables were as follows:" +
        "\033[0m")
  print("****************************************" +
        "******************************")

  print('\n \u2022 Reference VCF:\t', reference_file)
  print(' \u2022 iScan VCF:\t\t', iScan_file)

  # #####################################################################
  # SET UP OUTPUT DIRECTORY
  # #####################################################################

  # Create output directory folder if it does not already exist
  parent_dir = pathlib.Path().absolute()
  path = os.path.join(parent_dir, output_directory)
  print(" \u2022 " + "Output directory:\t" + path + "\n")
  if not os.path.exists(path):
      os.makedirs(path)

  # #####################################################################
  # READ ISCAN VCF FILE INTO DATAFRAME AND SANITIZE RECORDS
  # #####################################################################

  print("****************************************" +
        "******************************")
  print("\033[1m" +
        "Analyzing VCF files:" +
        "\033[0m")
  print("****************************************" +
        "******************************")


  def read_iscanvcf(iscan_input):
      '''Reads iScan VCF file'''
      try:
          gzf = gzip.open(iscan_input, 'rb')
          # lines = []
          with io.BufferedReader(gzf) as procfile:
              lines = [ln for ln in procfile if not ln.startswith(b"##")]
          gzf.close()
          return pd.read_csv(
              io.BytesIO(b"".join(lines)),
              sep="\t",
          )
      except gzip.BadGzipFile:
          with open(iscan_input, "r") as procfile:
              lines = [ln for ln in procfile if not ln.startswith("##")]
          return pd.read_csv(
              io.StringIO("".join(lines)),
              sep="\t",
          )


  print("\n \u2022 " + "Reading iScan VCF file...")
  # Read iScan_file into dataframe
  df = read_iscanvcf(iScan_file)

  print(" \u2022 " + "Verifying data types...")
  # Correct the data types as Pandas may interpret CHROM as
  # an int64 without 'chr' prefix
  df = df.astype({'#CHROM': str, 'POS': int, 'ID': str, 'REF': str,
                  'ALT': str, 'QUAL': str, 'FILTER': str, 'INFO': str})

  print(" \u2022 " + "Preparing data for comparison...")
  # Rename columns to drop # in CHROM and add i prefixes
  df.rename(columns={'#CHROM': 'iCHROM',
                     'POS': 'iPOS',
                     'REF': 'iREF',
                     'ALT': 'iALT',
                     }, inplace=True)

  print(" \u2022 " + "Counting records...")
  # Count number of rows
  stat_iScan_total_before_sanitization = (len(df.index))

  print(" \u2022 " + "Checking positions targeted by multiple probes...")
  # Check for chrom and pos dupes
  indexDupes = df[df[['iCHROM', 'iPOS']].duplicated(keep='first') == True].index
  df.drop(indexDupes, inplace=True)
  stat_chrom_pos_dupes = (len(indexDupes))
  del indexDupes

  print(" \u2022 " + "Checking for REF INDELs...")
  # Drop rows where REF contains an INDEL
  indexREFindel = df[(df['iREF'].isin(['I', 'D']))].index
  df.drop(indexREFindel, inplace=True)
  stat_ref_was_indel = (len(indexREFindel))

  print(" \u2022 " + "Checking for ALT INDELs...")
  indexALTindel = df[(df['iALT'].isin(['I', 'D']))].index
  df.drop(indexALTindel, inplace=True)
  stat_alt_was_indel = (len(indexALTindel))

  print(" \u2022 " + "Checking for mitochondrial loci...")
  # Drop rows where CHROM is M or chrM
  indexmtDNA = df[(df['iCHROM'].isin(['M', 'chrM']))].index
  df.drop(indexmtDNA, inplace=True)
  stat_ref_mtDNA = (len(indexmtDNA))

  print(" \u2022 " + "Checking for invalid positions...")
  # Drop rows where CHROM or POS are zero
  indexChromZero = df[(df['iCHROM'] == 0)].index
  indexPosZero = df[(df['iPOS'] == 0)].index
  stat_CHROM_zero = (len(indexChromZero))
  stat_POS_zero = (len(indexPosZero))
  df.drop(indexChromZero, inplace=True)
  df.drop(indexPosZero, inplace=True)

  # Check if 'chr' prefix is added
  print(" \u2022 " + "Checking if iScan VCF 'CHROM' field has 'chr' prefix...")
  check_chr = df.loc[df['iCHROM'].str.contains("chr", case=False)]
  if check_chr.empty:
      print(" \u2022 " + "Adding required 'chr' prefix to 'CHROM' field now...")
      df['iCHROM'] = "chr" + df['iCHROM'].astype(str)
  del check_chr

  # Sort lexicographically in case iScan VCF is unsorted
  print(" \u2022 " + "Sorting the iScan VCF...")
  df.sort_values(by=["iCHROM", "iPOS"], inplace=True)

  # Reset index and count number of rows
  # This MUST happen before concatenating to LOCUS
  df.reset_index(drop=True)
  stat_iScan_total_after_sanitization = (len(df.index))

  # Concatenate CHROM and POS into LOCUS and convert to list
  print(" \u2022 " + "Concatenating CHROM and POS into locus...")
  df['LOCUS'] = df['iCHROM'] + ":" + df['iPOS'].astype(str)
  list_of_iScan_loci = df['LOCUS'].to_list()

  # #####################################################################
  # CONSTRUCT NEW VCF HEADER FROM REFERENCE VCF
  # #####################################################################

  print(" \u2022 " + "Preparing to construct new VCF header...")

  # Prepare the first few (hard-coded) header lines
  vcf_header = ["##fileformat=VCFv4.3"]
  vcf_header += ["##fileDate=" + date.today().strftime("%Y%m%d")]
  vcf_header += ["##source=iScanVCFMerge"]


  # Define function to read reference VCF header
  def read_referencevcfheader(file):
      '''Reads lines from reference VCF file to build header'''
      try:
          gzf = gzip.open(file, 'rb')
          # lines = []
          with io.BufferedReader(gzf) as procfile:
              # header_lines = list(
              # [ln.rstrip() for ln in procfile if
              #     ln.startswith((b"##contig", b"##CONTIG"))]
              # )
              header_lines = [ln.rstrip() for ln in procfile if
                              ln.startswith((b"##contig", b"##CONTIG"))]
              gzf.close()
          return io.BytesIO(b"\n".join(header_lines)).read()
      except gzip.BadGzipFile:
          with open(file, "r") as procfile:
              # header_lines = list(
              #    [ln.rstrip() for ln in procfile if
              #     ln.startswith(("##contig", "##CONTIG"))]
              # )
              header_lines = [ln.rstrip() for ln in procfile if
                              ln.startswith(("##contig", "##CONTIG"))]
          return "\n".join(header_lines)


  print(" \u2022 " + "Constructing new VCF header...")

  # Read the reference VCF header and work out what to do with it
  # depending on if it was from a GZIP or not
  derived_header = read_referencevcfheader(reference_file)
  try:
      decoded_header = derived_header.decode('UTF-8')
      vcf_header += [decoded_header]
  except (UnicodeDecodeError, AttributeError):
      vcf_header += [derived_header]

  # #####################################################################
  # READ THE REFERENCE VCF INTO A DATA FRAME USING CHUNKSIZE
  # #####################################################################

  # Read the reference VCF file
  print(" \u2022 " + "Reading reference VCF file...")


  def read_referencevcf(file):
      '''Reads reference VCF file'''
      try:
          gzf = gzip.open(file, 'rb')
          # lines = []
          with io.BufferedReader(gzf) as procfile:
              lines = [ln for ln in procfile if not ln.startswith(b"##")]
          gzf.close()
          return pd.read_csv(
              io.BytesIO(b"".join(lines)),
              dtype={
                  b"#CHROM": str,
                  b"POS": int,
                  b"ID": str,
                  b"REF": str,
                  b"ALT": str,
                  b"QUAL": str,
                  b"FILTER": str,
                  b"INFO": str,
              },
              sep="\t",
              chunksize=1000000,
          )
      except gzip.BadGzipFile:
          with open(file, "r") as procfile:
              lines = [ln for ln in procfile if not ln.startswith("##")]
          return pd.read_csv(
              io.StringIO("".join(lines)),
              dtype={
                  "#CHROM": str,
                  "POS": int,
                  "ID": str,
                  "REF": str,
                  "ALT": str,
                  "QUAL": str,
                  "FILTER": str,
                  "INFO": str,
              },
              sep="\t",
              chunksize=1000000,
          )


  print(" \u2022 " + "Splitting reference VCF into blocks...")

  # Chunking function adapted from:
  # https://towardsdatascience.com/why-and-how-to-use-
  # pandas-with-large-data-9594dda2ea4c


  def chunk_preprocessing(chunk_input):
      '''Reads reference VCF data in chunks '''
      section = chunk_input.copy()
      section.rename(columns={'#CHROM': 'CHROM'}, inplace=True)
      print(" \u2022 " + "Processing variant block...")
      section['LOCUS'] = section['CHROM'] + ":" + section['POS'].astype(str)
      print(" \u2022 " + "Pairing reference VCF positions " +
            "to iScan positions...")
      filter_by_locus_calc = section['LOCUS'].isin(list_of_iScan_loci)
      return section[filter_by_locus_calc]


  df_chunk = read_referencevcf(reference_file)
  chunk_list = []

  # Each chunk is in data frame format, so these need to be
  # appended in order on top of one another and then concatenated
  # into a single reference VCF data frame

  print(" \u2022 " + "Processing blocks...")

  for chunk in df_chunk:
      chunk_filter = chunk_preprocessing(chunk)
      chunk_list.append(chunk_filter)

  print(" \u2022 " + "Concatenating reference VCF blocks...")

  df_reference = pd.concat(chunk_list)

  print(" \u2022 " + "Sorting the reference VCF...")

  df_reference.sort_values(by=["CHROM", "POS"], inplace=True)

  stat_loci_preserved_reference = (len(df_reference.index))

  # #####################################################################
  # MATCH VARIANT POSITIONS SHARED BETWEEN THE TWO VCF DATA FRAMES
  # #####################################################################

  print(" \u2022 " + "Building list of loci in the reference VCF...")
  # Convert list of reference loci to list
  list_of_reference_loci = df_reference['LOCUS'].to_list()

  print(" \u2022 " + "Collecting loci in the iScan VCF that are " +
        "also in the reference VCF...\n")
  # This may not be necessary, but I feel happier doing it to make sure
  # there are no unanticipated overlaps!
  filter_by_locus = df['LOCUS'].isin(list_of_reference_loci)
  df_iScan = df[filter_by_locus]
  # Delete the original data frame as it's no longer needed
  del df

  stat_loci_preserved_iScan = (len(df_iScan.index))

  print("****************************************" +
        "******************************")
  print("\033[1m" +
        "Cleaning up the VCF files prior to concatenation:" +
        "\033[0m")
  print("****************************************" +
        "******************************")

  print("\n \u2022 " + "Dropping unnecessary columns in each VCF...")
  # Because the relevant iScan columns are joined on to the end of the Reference
  # columns, these are not needed in their respective data frames
  df_reference.drop(columns=['LOCUS'], inplace=True)
  df_iScan.drop(columns=['LOCUS', 'QUAL', 'FILTER', 'INFO'], inplace=True)

  # Both data frames need to be re-indexed so that their row numbers
  # are continuous from zero
  print(" \u2022 " + "Re-indexing the VCF records...")
  df_iScan.reset_index(drop=True, inplace=True)
  df_reference.reset_index(drop=True, inplace=True)

  # DEBUGG: print("iScan data index: " + str(df_iScan.index))
  # DEBUGG: print("Reference data index : " + str(df_reference.index))

  print(" \u2022 " + "Cleaning up old INFO, QUAL and FILTER values...")
  # These can be cleaned out because they'll differ between VCFs
  df_reference = df_reference.assign(INFO='.', QUAL='.', FILTER='.')

  print(" \u2022 " + "Updating reference VCF locus IDs from the iScan VCF...")
  # Locus ID values from iScan take precedent over the
  # (probably missing) ones in the Reference file
  df_reference.merge(df_iScan, on='ID')
  df_iScan.drop(columns=['ID'], inplace=True)

  print(" \u2022 " + "Checking for non-genotype records in the reference VCF...")
  # The 'FORMAT' column is optional in the VCF Standard, but if it's there,
  # it means there are more than just GT values in the sample columns.
  # These need to be cleaned out as only GT data can be retained.
  # The FORMAT column is then dropped.
  if 'FORMAT' in df_reference.columns:
      print(" \u2022 " + "Removing non-genotype records from the reference " +
            "VCF...\n")
      # Nine columns because 8 are mandatory, the 9th (FORMAT) is optional,
      # and we checked to make sure it's here
      num_samples = (len(df_reference.columns)-9)
      # Here we get a list of sample column names to loop over
      cols_all = df_reference.columns.tolist()
      # Starting with column 9 (because one is actually 0) -- i.e.
      # the first sample, to the end
      cols_samples = cols_all[9:]

      # We remove anything after the first colon. This is appropriate
      # because the VCF standard requires that the GT entry is always
      # first, even if other values follow. So we do this across
      # all sample columns:
      for column in cols_samples:
          df_reference[column] = [x.split(':')[0] for x in df_reference[column]]

      print(" \u2022 " + "The following " + str(num_samples) +
            " samples will be processed from the reference VCF:\n")
      from textwrap import fill
      print(fill(', '.join(cols_samples), width=70))

      # Drop FORMAT from the reference VCF:
      df_reference.drop(columns=['FORMAT'], inplace=True)
      # Drop if it exists in the iScan VCF:
      if 'FORMAT' in df_iScan.columns:
          df_iScan.drop(columns=['FORMAT'], inplace=True)

  # Collect information on samples in the iScan VCF
  # We minus only 4 because we only deleted four columns thus far
  iScan_num_samples = (len(df_iScan.columns)-4)
  # Here we get a list of sample column names to loop over
  iScan_cols_all = df_iScan.columns.tolist()
  # Starting with column 4 (because 1 is 0) -- i.e. the first sample, to the end
  iScan_cols_samples = iScan_cols_all[4:]
  print("\n \u2022 " + "The following " + str(iScan_num_samples) +
        " samples will be processed from the iScan VCF:\n")
  print(fill(', '.join(iScan_cols_samples), width=70))

  # Concatenate the data frames
  df_master = df_reference.join(df_iScan)
  print("\n \u2022 " + "Concatenation complete!\n")

  # Drop the old frames from memory
  # Now we just use the master data frame
  del df_iScan
  del df_reference

  # Create new data frame to hold passing records to merge
  df_merged = pd.DataFrame()

  # Set total records value
  total_records = (len(df_master.index))

  print("****************************************" +
        "******************************")
  print("\033[1m" +
        "Processing " + str(total_records) + " variant records:" +
        "\033[0m")
  print("****************************************" +
        "******************************")

  # #####################################################################
  # GET RECORDS WHERE REF AND ALT ALLELES MATCH EXACTLY
  # #####################################################################

  # Pull out exact matches and record stats
  print("\n \u2022 " + "Detecting variants where REF and ALT alleles " +
        "match exactly...")
  df_exact_match = pd.DataFrame(df_master.loc[(df_master['CHROM'] ==
                                               df_master['iCHROM']) &
                                              (df_master['POS'] ==
                                               df_master['iPOS']) &
                                              (df_master['REF'] ==
                                               df_master['iREF']) &
                                              (df_master['ALT'] ==
                                               df_master['iALT'])])
  stat_exact_match = len(df_exact_match)
  # If such records exist, write to file
  if not df_exact_match.empty:
      # Create an index to easily drop these from the master
      df_exact_match_index = df_exact_match.index
      # Drop the superfluous columns
      df_exact_match.drop(columns=['iCHROM', 'iPOS', 'iREF', 'iALT'],
                          inplace=True)
      # Sort lexicographically and export to VCF with header
      df_exact_match.sort_values(by=["CHROM", "POS"], inplace=True)
      df_exact_match.rename(columns={'CHROM': '#CHROM'}, inplace=True)
      with open(path + "/exact_matches_biallelic.vcf", 'w') as f:
          f.write("\n".join(vcf_header) + "\n")
          df_exact_match.to_csv(f, index=False, sep='\t', header=True,
                                mode='a')
          f.close()
      # Drop the records from the master
      df_master.drop(df_exact_match_index, inplace=True)
      # Append the data frame to df_merged
      df_merged = df_merged.append(df_exact_match)
      # Drop the data frame from memory and count records
      del df_exact_match
      total_records = (total_records - stat_exact_match)
      # DEBUG print(" \u2022 " + "Total variant records " +
      # "remaining:\t" + str(total_records))

  # #####################################################################
  # GET RECORDS WHERE REF AND ALT ALLELES ARE EXACTLY REVERSED
  # #####################################################################

  # Pull out REF and ALT reversed and record stats
  print(" \u2022 " + "Detecting variants where REF and ALT alleles are" +
        " reversed...")
  df_ref_alt_reversed = pd.DataFrame(df_master.loc[(df_master['CHROM'] ==
                                                    df_master['iCHROM']) &
                                                   (df_master['POS'] ==
                                                    df_master['iPOS']) &
                                                   (df_master['REF'] ==
                                                    df_master['iALT']) &
                                                   (df_master['ALT'] ==
                                                    df_master['iREF'])])
  stat_ref_alt_reversed = len(df_ref_alt_reversed)
  # If such records exist, write to file
  if not df_ref_alt_reversed.empty:
      # Create an index to easily drop these from the master
      df_ref_alt_reversed_index = df_ref_alt_reversed.index
      # Drop the superfluous columns
      df_ref_alt_reversed.drop(columns=['iCHROM', 'iPOS', 'iREF', 'iALT'],
                               inplace=True)
      # Swap the records to placeholder records in the sample columns
      for column in iScan_cols_samples:
          df_ref_alt_reversed[column].replace({'0/0': 'A/A', '0/1': 'A/B',
                                               '1/0': 'B/A', '1/1': 'B/B'},
                                              inplace=True)
      # Swap the placeholders for the new records in the sample columns
      for column in iScan_cols_samples:
          df_ref_alt_reversed[column].replace({'A/A': '1/1', 'A/B': '1/0',
                                               'B/A': '0/1', 'B/B': '0/0'},
                                              inplace=True)
      # Sort lexicographically and export to VCF with header
      df_ref_alt_reversed.sort_values(by=["CHROM", "POS"], inplace=True)
      df_ref_alt_reversed.rename(columns={'CHROM': '#CHROM'}, inplace=True)
      with open(path + "/exact_matches_rev_biallelic.vcf", 'w') as f:
          f.write("\n".join(vcf_header) + "\n")
          df_ref_alt_reversed.to_csv(f, index=False, sep='\t', header=True,
                                     mode='a')
          f.close()
      # Drop the records from the master
      df_master.drop(df_ref_alt_reversed_index, inplace=True)
      # Append the data frame to df_merged
      df_merged = df_merged.append(df_ref_alt_reversed)
      # Drop the data frame from memory and count records
      del df_ref_alt_reversed
      total_records = (total_records - stat_ref_alt_reversed)
      # DEBUG print(" \u2022 " + "Total variant records " +
      # "remaining:\t" + str(total_records))

  # #####################################################################
  # CHECK IF THE ALT FIELD IN THE REF VCF CONTAINS MULTIPLE ALLELES
  # #####################################################################

  # Check if the reference ALT field contains commas
  # This indicates alternative alleles for the ALT field
  print(" \u2022 " + "Detecting multi-allelic ALT sites in the " +
        "reference data...")
  df_alternate_alleles = df_master.loc[(df_master['ALT'].str.contains(','))]
  stat_alternate_alleles = len(df_alternate_alleles)

  # Set empty stats to avoid error in output if no multi-allelics found
  stat_multiallelic_regular = "0"
  stat_multiallelic_flipped = "0"

  # Only proceed if they exist
  if not df_alternate_alleles.empty:
      print(" \u2022 " + "Processing multi-allelic ALT sites:")
      df_alternate_alleles_index = df_alternate_alleles.index
      # Create a new data frame containing only those sites
      # Split the ALT column into multiple columns; one for each allele
      split_alts = df_alternate_alleles['ALT'].str.split(',', expand=True)
      split_alts.columns = ['ALT_{}'.format(int(x)+1) for x in split_alts.columns]
      # Add those columns to the end of the alternate_alleles data frame
      df_alternate_alleles = df_alternate_alleles.join(split_alts)
      # Delete the separate split_alts from memory
      del split_alts

      # Create empty data frames to contain matches
      df_multiallelic_regular = pd.DataFrame()
      df_multiallelic_flipped = pd.DataFrame()

  # #####################################################################
  # FUNCTION TO RESCUE MULTI-ALLELIC RECORDS
  # #####################################################################

      # Column will be either ALT_1, ALT_2, ALT_3 or ALT_4
      # Orientation will be either regular or flipped
      def check_for_multis(column_to_check, orientation):
          '''Checks for multi-allelic sites in either orientation'''
          # Check if the column e.g. ALT_2 actually exists in the data
          if column_to_check in df_alternate_alleles.columns:
              # Check if orientation is regular
              if orientation == "regular":
                  # Search for regular matches, i.e. iREF=REF and iALT=column
                  df_matches = pd.DataFrame(df_alternate_alleles.loc[
                                           (df_alternate_alleles['CHROM'] ==
                                            df_alternate_alleles['iCHROM']) &
                                           (df_alternate_alleles['POS'] ==
                                            df_alternate_alleles['iPOS']) &
                                           (df_alternate_alleles['REF'] ==
                                            df_alternate_alleles['iREF']) &
                                           (df_alternate_alleles[column] ==
                                            df_alternate_alleles['iALT'])])
                  # If matches were found, index to facilitating dropping
                  if not df_matches.empty:
                      df_matches_index = df_matches.index
                      print(" \u2022 " + "Re-coding " +
                            str(len(df_matches_index)) +
                            " iScan genotypes matching alternative ALT" +
                            " allele " + (column_to_check[4:5]) + "...")
                      # Update the variant call GTs for all iScan samples,
                      # depending on the column:
                      for each_sample in iScan_cols_samples:
                          # No manipulation of GT is needed for column one
                          # But we have to call it to ensure the
                          # data are appended
                          if column_to_check == 'ALT_2' and column_to_check in df_matches.columns:
                              df_matches[each_sample].replace({'0/1': '0/2',
                                                               '1/1': '1/2'},
                                                              inplace=True)
                          if column_to_check == 'ALT_3' and column_to_check in df_matches.columns:
                              df_matches[each_sample].replace({'0/1': '0/3',
                                                               '1/1': '1/3'},
                                                              inplace=True)
                          if column_to_check == 'ALT_4' and column_to_check in df_matches.columns:
                              df_matches[each_sample].replace({'0/1': '0/4',
                                                               '1/1': '1/4'},
                                                              inplace=True)
                      # Append results to the regular dataframe
                      global df_multiallelic_regular
                      df_multiallelic_regular = (df_multiallelic_regular.
                                                 append(df_matches))
                  # We have to drop at the end of ALT_4,
                  # i.e. before moving to 'flipped'
                  # otherwise flipped will find some
                  # regular records and duplicate those
                  # causing a failure later on
                      if column == 'ALT_4':
                          df_alternate_alleles.drop(df_matches_index,
                                                    inplace=True)
                      # Clear the df_matches dataframe
                      del df_matches

              # Check if orientation is flipped
              if orientation == "flipped":
                  # Search for flipped matches, i.e. iREF=column and iALT=REF
                  df_matches = pd.DataFrame(df_alternate_alleles.loc[
                                           (df_alternate_alleles['CHROM'] ==
                                            df_alternate_alleles['iCHROM']) &
                                           (df_alternate_alleles['POS'] ==
                                            df_alternate_alleles['iPOS']) &
                                           (df_alternate_alleles['REF'] ==
                                            df_alternate_alleles['iALT']) &
                                           (df_alternate_alleles[column] ==
                                            df_alternate_alleles['iREF'])])
                  # If matches were found, index to facilitating dropping
                  if not df_matches.empty:
                      df_matches_index = df_matches.index
                      print(" \u2022 " + "Re-coding " +
                            str(len(df_matches_index)) +
                            " iScan genotypes matching reversed ALT allele " +
                            (column[4:5]) + "...")
                      # Update the variant call GTs for all iScan samples,
                      # depending on the column:
                      # Note this throws local variable 'x' value is
                      # not used warning
                      for xyz in iScan_cols_samples:
                          if column == 'ALT_1' and column in df_matches.columns:
                              df_matches[column].replace({'0/1': 'X/X',
                                                          '1/0': 'Y/Y'},
                                                         inplace=True)
                              df_matches[column].replace({'X/X': '1/0',
                                                          'Y/Y': '0/1'},
                                                         inplace=True)
                          if column == 'ALT_2' and column in df_matches.columns:
                              df_matches[column].replace({'1/1': 'X/X',
                                                          '1/0': 'Y/Y',
                                                          '0/1': 'Z/Z'},
                                                         inplace=True)
                              df_matches[column].replace({'X/X': '1/2',
                                                          'Y/Y': '0/2',
                                                          'Z/Z': '1/0'},
                                                         inplace=True)
                          if column == 'ALT_3' and column in df_matches.columns:
                              df_matches[column].replace({'1/1': 'X/X',
                                                          '1/0': 'Y/Y',
                                                          '0/1': 'Z/Z'},
                                                         inplace=True)
                              df_matches[column].replace({'X/X': '1/3',
                                                          'Y/Y': '0/3',
                                                          'Z/Z': '1/0'},
                                                         inplace=True)
                          if column == 'ALT_4' and column in df_matches.columns:
                              df_matches[column].replace({'1/1': 'X/X',
                                                          '1/0': 'Y/Y',
                                                          '0/1': 'Z/Z'},
                                                         inplace=True)
                              df_matches[column].replace({'X/X': '1/4',
                                                          'Y/Y': '0/4',
                                                          'Z/Z': '1/0'},
                                                         inplace=True)
                      # Append results to the flipped dataframe
                      global df_multiallelic_flipped
                      df_multiallelic_flipped = (df_multiallelic_flipped
                                                 .append(df_matches))
                      # Clear the df_matches dataframe
                      del df_matches

      # #####################################################################
      # RUN THE FUNCTION TO RESCUE MULTI-ALLELIC RECORDS
      # #####################################################################

      # Run the function to check for multi-allelic alts
      check_for_multis('ALT_1', 'regular')
      check_for_multis('ALT_2', 'regular')
      check_for_multis('ALT_3', 'regular')
      check_for_multis('ALT_4', 'regular')
      check_for_multis('ALT_1', 'flipped')
      check_for_multis('ALT_2', 'flipped')
      check_for_multis('ALT_3', 'flipped')
      check_for_multis('ALT_4', 'flipped')

      if not df_multiallelic_regular.empty:
          # Drop columns that won't match to the master table, and index
          df_multiallelic_regular.drop(columns=['ALT_1', 'ALT_2',
                                                'ALT_3', 'ALT_4'],
                                       inplace=True, errors='ignore')
          df_multiallelic_regular_index = df_multiallelic_regular.index
          # Drop columns not needed in the VCF
          df_multiallelic_regular.drop(columns=['iCHROM', 'iPOS',
                                                'iREF', 'iALT'],
                                       inplace=True, errors='ignore')
          # Sort lexicographically and export to VCF with header
          df_multiallelic_regular.sort_values(by=["CHROM", "POS"],
                                              inplace=True)
          df_multiallelic_regular.rename(columns={'CHROM': '#CHROM'},
                                         inplace=True)
          with open(path + "/exact_matches_multiallelic.vcf", 'w') as f:
              f.write("\n".join(vcf_header) + "\n")
              df_multiallelic_regular.to_csv(f, index=False, sep='\t',
                                             header=True, mode='a')
              f.close()
          # Record statistic
          if len(df_multiallelic_regular_index) > 0:
              stat_multiallelic_regular = len(df_multiallelic_regular_index)
          # Drop the records from the master
          df_master.drop(df_multiallelic_regular_index, inplace=True)
          # Append the data frame to df_merged
          df_merged = df_merged.append(df_multiallelic_regular)
          # Drop the data frame from memory and count records
          del df_multiallelic_regular
          total_records = (total_records - stat_multiallelic_regular)
          # DEBUG print(" \u2022 " + "Total records rem:\t" + str(total_records))

      if not df_multiallelic_flipped.empty:
          # Drop columns that won't match to the master table, and index
          df_multiallelic_flipped.drop(columns=['ALT_1', 'ALT_2',
                                                'ALT_3', 'ALT_4'],
                                       inplace=True, errors='ignore')
          df_multiallelic_flipped_index = df_multiallelic_flipped.index
          # Drop columns not needed in the VCF
          df_multiallelic_flipped.drop(columns=['iCHROM', 'iPOS',
                                                'iREF', 'iALT'],
                                       inplace=True, errors='ignore')
          # Sort lexicographically and export to VCF with header
          df_multiallelic_flipped.sort_values(by=["CHROM", "POS"],
                                              inplace=True)
          df_multiallelic_flipped.rename(columns={'CHROM': '#CHROM'},
                                         inplace=True)
          with open(path + "/exact_matches_rev_multiallelic.vcf", 'w') as f:
              f.write("\n".join(vcf_header) + "\n")
              df_multiallelic_flipped.to_csv(f, index=False, sep='\t',
                                             header=True, mode='a')
              f.close()
          # Record statistic
          if len(df_multiallelic_flipped_index) > 0:
              stat_multiallelic_flipped = len(df_multiallelic_flipped_index)
          # Drop the records from the master
          df_master.drop(df_multiallelic_flipped_index, inplace=True)
          # Append the data frame to df_merged
          df_merged = df_merged.append(df_multiallelic_flipped)
          # Drop the data frame from memory and count records
          del df_multiallelic_flipped
          total_records = (total_records - stat_multiallelic_flipped)
          # DEBUG print(" \u2022 " + "Total recs rem:\t" + str(total_records))

      # Delete alternate alleles data frame from memory
      del df_alternate_alleles

  # #####################################################################
  # CONSTRUCT MERGED AND REJECTED FILES
  # #####################################################################

  stat_rejected = "0"
  stat_merged = "0"

  if not df_master.empty:
      # Sort lexicographically and export to VCF with header
      df_master.sort_values(by=["CHROM", "POS"], inplace=True)
      df_master.rename(columns={'CHROM': '#CHROM'}, inplace=True)
      with open(path + "/rejected.vcf", 'w') as f:
          f.write("\n".join(vcf_header) + "\n")
          df_master.to_csv(f, index=False, sep='\t', header=True, mode='a')
          f.close()
      # Record statistic
      stat_rejected = len(df_master.index)
      # Drop the data frame from memory and count records
      del df_master
      total_records = (total_records - stat_rejected)
      # DEBUG print(" \u2022 " + "Total recs rem:\t" + str(total_records))

  if not df_merged.empty:
      # Sort lexicographically and export to VCF with header
      df_merged.sort_values(by=["#CHROM", "POS"], inplace=True)
      with open(path + "/merged.vcf", 'w') as f:
          f.write("\n".join(vcf_header) + "\n")
          df_merged.to_csv(f, index=False, sep='\t', header=True, mode='a')
          f.close()
      # Record statistic
      stat_merged = len(df_merged.index)
      # Drop the data frame from memory and count records
      del df_merged

  # #####################################################################
  # OUTPUT SUMMARY STATISTICS
  # #####################################################################

  print("\n****************************************" +
        "******************************")
  print("\033[1m" +
        "iScanVCFMerge is complete! Summary statistics:" +
        "\033[0m")
  print("****************************************" +
        "******************************\n")

  print(" \u2022 " + "Original number of iScan records:" +
        "\t\t\t\t" + str(stat_iScan_total_before_sanitization))
  print(" \u2022 " + "Duplicate positions dropped:" + "\t\t\t\t\t" +
        str(stat_chrom_pos_dupes))
  print(" \u2022 " + "Positions dropped where REF contained an INDEL:" +
        "\t\t" + str(stat_ref_was_indel))
  print(" \u2022 " + "Positions dropped where ALT still contained an " +
        "INDEL:" + "\t" + str(stat_alt_was_indel))
  print(" \u2022 " + "Positions dropped where CHROM value was zero:" +
        "\t\t" + str(stat_CHROM_zero))
  print(" \u2022 " + "Positions dropped where POS value was zero:" +
        "\t\t\t" + str(stat_POS_zero))
  print(" \u2022 " + "Remaining iScan positions after clean-up:" +
        "\t\t\t" + str(stat_iScan_total_after_sanitization) + "\n")

  print(" \u2022 " + "Positions shared between reference and iScan" +
        "VCFs:" + "\t\t" + str(stat_loci_preserved_reference) + "\n")

  print(" \u2022 " + "Positions where REF and ALT alleles matched " +
        "exactly:" + "\t\t" + str(stat_exact_match))
  print(" \u2022 " + "Positions where REF and ALT alleles were" +
        "reversed:" + "\t\t" + str(stat_ref_alt_reversed) + "\n")
  print(" \u2022 " + "Number of multiallelic ALT positions:\t\t\t" +
        str(stat_alternate_alleles))
  print(" \u2022 " + "Number of iScan positions re-coded to use " +
        "alternate ALT:\t" + str(stat_multiallelic_regular))
  print(" \u2022 " + "Number of iScan positions reversed to use " +
        "alternate ALT:\t" + str(stat_multiallelic_flipped) + "\n")

  print(" \u2022 " + "Total number of positions re-coded and " +
        "recovered:" + "\t\t" + str(stat_merged))
  print(" \u2022 " + "Total number of positions that were discarded:" +
        "\t\t" + str(stat_rejected))

  if int(stat_loci_preserved_reference) == 0:
      success_rate = str(round(int(stat_merged), 2))
  else:
      success_rate = str(round(((int(stat_merged)/int(stat_loci_preserved_reference))*100), 2))

  print(" \u2022 " + "iScanVCFMerge conversion success rate:\t\t\t" +
        str(success_rate) + "%\n")

  executionTime = (time.time() - startTime)
  print(" \u2022 " + "iScanVCFMerge completed in " +
        str(round(executionTime, 2)) + " seconds\n")

  print("****************************************" +
        "******************************")
  print("\033[1m" +
        "Output files:" +
        "\033[0m")
  print("****************************************" +
        "******************************\n")
  print(r"        .' '.    " + "\t\033[1mexact_matches_biallelic.vcf (N=" +
        str(stat_exact_match) + ")\033[0m")
  print(r"    .-./ _=_ \.-.  " + "\tBiallelic positions where REF &" +
        " ALT matched.")
  print(r"   {  (,(oYo),) }} ")
  print(r"   {{ |  ' '  | }} " + "\t\033[1mexact_matches_rev_biallelic.vcf" +
        " (N=" + str(stat_ref_alt_reversed) + ")\033[0m")
  print(r"   { {  (---)   }} " + "\tBiallelic positions that matched" +
        "once reversed.")
  print(r"   {{  }'-=-'{ } } ")
  print(r"   { { }._:_.{  }} " + "\t\033[1mexact_matches_multiallelic.vcf" +
        " (N=" + str(stat_multiallelic_regular) + ")\033[0m")
  print(r"   {{  } -:- { } } " + "\tMultiallelic positions where" +
        " REF & ALT matched.")
  print(r"   {_{ }`===`{  _} ")
  print(r"  ((((\)     (/))))" + "\t\033[1mexact_matches_rev_" +
        "multiallelic.vcf (N=" + str(stat_multiallelic_flipped) + ")\033[0m")
  print("                    " + "\tMultiallelic positions that" +
        "matched once reversed.\n")
  print(r"        .=''=.         " + "\033[1m\tmerged.vcf (N=" +
        str(stat_merged) + ")\033[0m")
  print(r"      _/.-.-.\_     _ " + "\tAll of the above for downstream use.")
  print(r"     ( ( o o ) )    ))" + "\ti.e. " + str(stat_exact_match) +
        " + " + str(stat_ref_alt_reversed) + " + " +
        str(stat_multiallelic_regular) + " + " +
        str(stat_multiallelic_flipped) + " = " + str(stat_merged))
  print(r'      |/  "  \|    // ')
  print(r"       \\---//    //  " + "\033[1m\trejected.vcf (N=" +
        str(stat_rejected) + ")\033[0m")
  print(r'       /`"""`\\  ((   ' + "\tPositions that did not match.")
  print(r"      / /_,_\ \\  \\  ")
  print(r"      \_\\_'__/ \  )) " + "\t\tThank you for using iScanVCFMerge!")
  print(r"      /`  /`~\  |//   ")
  print(r"     /   /    \  /    ")
  print(r" ,--`,--'\/\    /     ")
  print(r"  '-- ''--'  '--'     ")
  print("\n")
