## Usage
On disk:
 * Origin: 21.0GB
 * Formatted: 15.2GB

Memory:
  * Origin: >16GB
  * Formatted: 8.0GB

Details:
   - **260 million** entries
   - ClientMacAddr - **int64** *(~2.0GB)*
   - Level - **int8** *(~0.260GB)*
   - lat - **float64** *(~2.0GB)*
   - lng - **float64** *(~2.0GB)*
   - localtime - **datetime64[ns]** *(~2.0GB)*

## Details of features
* *Building*: Dropped since its contains only one value
* *ClientMacAddr*:
  * Formatted to *int64*
  * ~ 9 million distinct Ids, which means on average each Id has 27 records
  * ~ 5% of Ids have more than 27 records
  * Std of numbers of records for Ids is ~1200
* *localtime*:
  * Range from 2018-04-01 to 2018-07-31
  * Around June and July, there is a period that only hundreds of records exist
    * May be because of some special cases about the mall
    * The records may from staffs
