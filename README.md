# cr-rankings-etl-onprem
Consumer Reports Data (Overall Scores for Ranking) ETL tool to keep track of product rankings.
![cr_rankings_etl](https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/4e199367-6c67-48b8-90fb-a99aa3b46eb2)


## Project Overview

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
- ```Excel VBA Macros & Functions```: Update dashboard that shows changes between sessions.


**Extraction** 
-------------
 - A custom web scraper was built using Selenium and Python to extract 43 home appliance product categories' data.
  <img width="316" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/dc1cddf1-24db-4d92-bf74-5a8723fe615e">
  <img width="358" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/efaefbd2-42a5-4a48-980f-f2aa5fe89071">








  
 - Scheduled to run the script on weekdays using Windows Task Scheduler.
  <img width="375" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/ff56625d-a80c-47a4-b3de-c1970a7f61bf">



**Transformation**
-------------
<img width="427" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/19fdc003-5bcb-42f8-b7d2-fec766f74731">

<img width="340" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/d261fbbb-9c0f-4913-8567-b1a39d5c8295">




**Dashboards**
--------------
- Excel VBA macros and functions based dashboard

<img width="220" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/064b55f4-d4df-4948-9236-7b1378f67dd4">
<img width="334" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/dc1e4b9d-06ab-4a4f-9454-405c858fcb5a">

-------------

<img width="475" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/3ded91ac-5a67-4328-9c12-5c0cefb2bd26">
<img width="365" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/e385831f-765a-418e-a767-db585099d61d">

------------
<img width="425" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/427d2d52-0997-444c-bb2b-3bbf6cd7a55b">
<img width="468" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/f6a86c0d-e6ad-4914-af09-f86c8220495e">

-------------
<img width="900" alt="image" src="https://github.com/kwoolaid725/cr-rankings-etl-onprem/assets/107806433/4295a1ef-c871-4641-9b02-1bf6cded9e37">










