# Preprocess Data
Download data provided by Kiana.

**Run Scripts:**
* python one_step.py <Memory_Usage(in GB)> <Input_file> <Output_File1>
* python assign_block.py <Output_file1> <Output_File2>

**Debugger Dataset:**

*input/debugger_origin.csv* file is small subset from origin dataset. It is used for testing the execution of our preprocessing programs.

*input/debugger.csv* file is a small dataset used to debug programs and test website interface. It should not be regarded as formally implemented data.

*input/debugger.csv* contains counts of records in each block.
* Time period is in: **10:00 to 14:45** *and* **April 25 to April 30th**.
* Cols: Level, latBlock, lngBlock, month, day, hour, quarter, count

*input/weather* contains weather data scraped from internet

**Overview:**

A quick overview of preprocessing program is in *Overview.ipynb* which runs on debugger dataset.

# Support
INF-560 (Data Informatics Professional Practicum) Project sponsored by Kiana Analytics, Inc.
