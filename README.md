# Consumer Reports Rankings ETL - OnPrem ver.
Consumer Reports Data (Overall Scores for Ranking) ETL tool to keep track of product rankings in each of the 43 product categories (~1600 products)
![cr_rankings_etl](https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/e14b243c-48ef-47f2-8c54-8612eed9ee6e)



## Project Overview

The implementation of the ETL process streamlined the daily spending time of about 10 engineers from a combined 5+ hours to merely 10 minutes for a single person (who only needs to click a macro button in Excel VBA). Every step of this end-to-end pipeline has been initiated and developed by me.

<!-- Engineers have daily responsibilities to check the Consumer Reports 
website for any changes within the home appliance product categories they are in charge of. 
There are 43 product categories to be checked by about 10 engineers everyday. 
An engineer spends at least half an hour to review their products and update the table if any changes are observed and report to the 
senior manager.-->

### Technologies and Functions 
- ```Python/Selenium```: Data extraction.
- ```Python/Pandas```: Data transformation.
- ```Windows Task Scheduler```: Scheduled task (cron) to run the python script everyday at a scheduled time.
- ```Postgres```: Data warehouse on premise.
- ```Shared Cloud Disk```: Store transformed data in excel format for clleagues and dashboards.
- ```Excel VBA Macros & Functions```: Dashboard with ranking tables, update status, and search tool.


**Extraction** 
-------------
 - A custom web scraper was built using Selenium and Python to extract 43 home appliance product categories' data.
  <img width="316" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/64848b19-3333-4092-967c-343e84205694">
  <img width="358" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/efaefbd2-42a5-4a48-980f-f2aa5fe89071">







  
 - Scheduled to run the script on weekdays using Windows Task Scheduler.
  <img width="375" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/ff56625d-a80c-47a4-b3de-c1970a7f61bf">

<img width="365" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/31a29c8c-724c-45d1-99ca-cb34d9e0aff3">



**Transformation**
-------------
- Data cleaning
- Creating new columns: **ranking**, **key**, **concat**, and **ranking_change**
- **Key** and **concat** are needed for generating dynamic tables in the Excel VBA file

<img width="420" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/a2445266-3082-40cb-8b7a-61ead2d312ca">

<img width="333" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/7228e238-c9df-4f04-a4f1-81ca3d586967">

- **How rankings are given:**

![image](https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/62a143a3-8900-4b4c-9202-141d40d7c82b)

**Postgres Datatable:**
![image](https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/c84c0194-6d8e-4ec4-8892-cad54b39d60a)




**Dashboards**
--------------
- Excel VBA macros and functions were used to create the dashboard

<img width="220" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/064b55f4-d4df-4948-9236-7b1378f67dd4">
<img width="334" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/dc1e4b9d-06ab-4a4f-9454-405c858fcb5a">





-------------

- **Ranking Tables**

<img width="475" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/3ded91ac-5a67-4328-9c12-5c0cefb2bd26">

<img width="365" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/e385831f-765a-418e-a767-db585099d61d">






------------
- **Changes Detecting Screen**

<img width="550" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/427d2d52-0997-444c-bb2b-3bbf6cd7a55b">


- **Dynamic Lookup Table**

<img width="550" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/f6a86c0d-e6ad-4914-af09-f86c8220495e">

-------------

- **Dynamic Lookup Table Nested Functions** 
<img width="900" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/4295a1ef-c871-4641-9b02-1bf6cded9e37">










