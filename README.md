# Preprocess
Download data provided by Kiana.

**Run Scripts:**
* python one_step.py <Memory_Usage(in GB)> <Input_file> <Output_File1>
* python assign_block.py <Output_file1> <Output_File2>

**Debugger Dataset:**

*input/debugger_origin.csv* file is small subset from origin dataset (random sampling). It is used for testing the execution of our preprocessing programs.

*input/debugger.csv* file is a small dataset used to debug programs and test website interface. It should not be regarded as formally implemented data. It contains counts of records in each block.
* Time period is in: **10:00 to 14:45** *and* **April 25 to April 30th**.
* Cols: Level, latBlock, lngBlock, month, day, hour, quarter, count

*input/weather* contains weather data scraped from internet

**Overview of Functions:**

A quick overview of preprocessing program is in *[Quick_Overview.ipynb](./Quick_Overview.ipynb)* which runs on debugger dataset.

# Support
INF-560 (Data Informatics Professional Practicum) Project sponsored by Kiana Analytics, Inc.

# Run Demo
## Step 1
Use command below to setup environment:
$npm install -g browser-sync
## Step 2
Enter the dictionary "web"(Kiana->web)
## Step 3
Use command below to run the demo on your web browsers:
$browser-sync start -s -f "*.html,*.css,*.js" -i index.html
