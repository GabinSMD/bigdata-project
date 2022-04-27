<div id="top"></div>
<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the repo and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email
-->





<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">

  <h3 align="center">Big Data</h3>

  <p align="center">
    Deployement Project    
    <br />
    <br />
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Report Bug</a>
    ·
    <a href="https://github.com/othneildrew/Best-README-Template/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Contributors](#contributors)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Roadmap](#roadmap)
* [Usage](#usage)
  * [Parameters](#parameters)
  * [Commands](#commands)
    * [Stock scripts](#stock-scripts)
    * [Top script](#top-scripts)
* [Contributing](#contributing)
* [License](#license)


<!-- ABOUT THE PROJECT -->
## About The Project

The aim of this project is to retrieve shares from the stock exchange every hour from Monday (9:30 am) to Friday (6:30 pm).

The collected data will then be processed according to the [Roadmap](#roadmap)

This project was realized during the BigData course at the Polytechnic University of Valencia


### Contributors 

<a href="https://github.com/GabinSMD/bigdata-project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=GabinSMD/bigdata-project" />
</a>

### Built With

* [Python](https://www.python.org)
* [Hadoop](https://hadoop.apache.org/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* selenium
```sh
sudo pip install selenium
```
* geckodriver
```sh
sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
sudo tar -xzvf geckodriver-v0.31.0-linux64.tar.gz
sudo rm geckodriver-v0.31.0-linux64.tar.gz
sudo mv geckodriver /usr/bin
```
### Installation

1. Go to Alumno Home in Big Data Practicas folder
```sh
cd /home/alumno/bigdatapracticas/
```
2. Get Project Package
```sh
sudo git clone https://github.com/GabinSMD/bigdata-project.git
cd bigdata-project
sudo mv proyecto/ ../
sudo mv README.md ../
cd ../
sudo rm -rf bigdata-project
sudo chown -R alumno proyecto/
```
2. Add the cron execution line
```sh
crontab -e
```
then add
```
30 9-18 * * 1-5 /home/alumno/environments/bigdata/bin/python3.6 /home/alumno/bigdatapracticas/proyecto/scripts/project_main.py > /home/alumno/foo.log 2>&1
```

<!-- ROADMAP -->
## Roadmap

 
- [x] [Generate a weekly list (for the current week) showing, for each stock, its initial, final, minimum and maximum value for each share.](https://github.com/GabinSMD/bigdata-project/main/project_main.py)

- [x] [Generate a monthly list (for the current month) indicating, for each share, its initial, final, minimum and maximum value for each share](https://github.com/GabinSMD/bigdata-project/main/project_stock_list.py)

- [x] [Given the name of a stock and a range of dates, obtain its minimum and maximum value of quotation, as well as the percentage decrease and increase from the initial quote value to the minimum and maximum, respectively.](https://github.com/GabinSMD/bigdata-project/main/project_stock_infos.py)

- [x] [Given the name of a stock, retrieve its lowest and highest quoted value for the last hour, week and month.](https://github.com/GabinSMD/bigdata-project/main/project_stock_history.py)

- [x] [Display the 5 stocks that have risen the most in the last week and month.](https://github.com/GabinSMD/bigdata-project/main/project_stock_increase.py)

- [x] [Display the 5 stocks that have fallen the most in the last week and month.](https://github.com/GabinSMD/bigdata-project/main/project_stock_decrease.py)
- [x] Add the optional feature:
 
   - [x] [Given a percentage and a range of dates, show the stocks that have had an increase of this percentage during this period.](https://github.com/GabinSMD/bigdata-project/main/project_stock_evolution.py)
- [x] Add advanced features:

   - [x] [Given a time period, show the variation of the Top 5 stocks over this period.](https://github.com/GabinSMD/bigdata-project/main/project_top_history.py)

   - [x] [Given a precise date, show the value of the top 5 stocks at that time.](https://github.com/GabinSMD/bigdata-project/main/project_top_date.py)

   - [x] [Given a percentage and a range of dates, show the stock list’s corresponding who have already been in the top 5.](https://github.com/GabinSMD/bigdata-project/main/project_top_evolution.py)

See the [open issues](https://github.com/github_username/repo_name/issues) for a list of proposed features (and known issues).

<!-- USAGE EXAMPLES -->
## Usage

### Parameters

* For `project_stock_[SCRIPTNAME].py` scripts:
  
  `YEAR` : enter the year wanted, can be `*` for all folders

  `WEEK` :  enter the week wanted, can be `*` for all folders

  `MONTH-DAY` :  enter the month-day wanted, can be `*` for all folders
  
  `DATE` :  enter the date wanted in format : "2022-4-26 16:45" 

  `FILENAME` : enter the name of the file in the following format:
  - For the hourly files: `hourlyResult`_`YEAR`-`WEEK`-`DAY`-`HOUR`h but any part or all part can be replace by `*`
  - For the daily files: `dailyResult`_`YEAR`-`WEEK`-`DAY` but any part or all part can be replace by `*`
  
* For `project_top_[SCRIPTNAME].py` scripts:

These scripts use the parameters of the `project_stock_[SCRIPTNAME].py` scripts with the following new parameter:
  
  `TOPFILENAME` : Enter the name to the previously generated Top file, can be `*` for all top files

### Commands
#### Stock scripts:
* project_main.py
```sh
python project_main.py
```
This allows to launch the scrapper, the creation of the daily, weekly and monthly files and to send them in the HDFS if it is 18:30
* project_stock_list.py
  - Command:
    ```sh
    python project_stock_list.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME]
    ```
   - E.G :
     - Create a Weekly file of daily values:
       ```sh
       python project_stock_list.py ../outputs/2022/17/*/dailyResult_*
       ```
     - Create a Month file of weekly values:
        ```sh
        python project_stock_list.py ../outputs/2022/*/4-*/dailyResult_*
        ```
* project_stock_infos.py
  - Command:
    ```sh
    python project_stock_infos.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME]  --minDate=[DATE] --maxDate=[DATE] --stockName=[NAME]
    ```
   - E.G :
     - Give informations about acciona between 9:30 and 19:40 on 21/04/2022:
       ```sh
       python project_stock_infos.py ../outputs/*/*/*/dailyResult_*  --minDate="2022-04-21 09:30" --maxDate="2022-04-21 19:40" --stockName="acciona"
       ```

* project_stock_history.py
  - Command:
    ```sh
    python project_stock_history.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME]
    ```
   - E.G :
     - Give the minimal and the maximal value of SOLARIA of the last hour, last week and the last month:
       ```sh
       python project_stock_history.py ../outputs/*/*/*/dailyResult_* --stockName="SOLARIA"
       ```

* project_stock_increase.py
  - Command:
    ```sh
    python project_stock_increase.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME]
    ```
   - E.G :
     - Display the 5 stocks that have risen the most in the last week and month :
       ```sh
       python project_stock_increase.py ../outputs/*/*/*/dailyResult_* 
       ```
       
* project_stock_decrease.py
  - Command:
    ```sh
    python project_stock_decrease.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/hourlyResult_[FILENAME]
    ```
   - E.G :
     - Display the 5 stocks that have declined the most in the last week and month:
       ```sh
       python project_stock_decrease.py ../outputs/2022/17/*/dailyResult_*
       ```
        
* project_stock_evolution.py
  - Command:
    ```sh
    python project_stock_evolution.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME] --pourcentage=[PORCENTAGE] --minDate=[DATE] --maxDate=[DATE]
    ```
   - E.G :
     - Takes all files from 2022 and displays the stocks that have increased by that percentage between 21/04/2022 9:30 and 28/04/2022 17:00   :
       ```sh
       python project_stock_evolution.py ../outputs/2022/*/*/dailyResult_* --pourcentage=1 --minDate="2022-04-21 9:30" --maxDate="2022-04-28 17:00"
       ```
       
#### Top scripts:

* project_top_history.py
  - Command:
    ```sh
    python project_top_history.py ../outputs/[TOP5] ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME] --minDate=[DATE] --maxDate=[DATE]
    ```
   - E.G :
     - Take the names of the stock in todayTOP5 and display informations of these stock between 16/04/2022 9:00 and 26/04/2022 15:00
       ```sh
       python project_top_history.py ../outputs/todayTOP5 ../outputs/*/*/*/dailyResult_* --minDate="2022-4-16 9:00" --maxDate="2022-4-26 15:00"
       ```
       
* project_top_date.py
  - Command:
    ```sh
    python project_top_date.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/hourlyResult_[FILENAME]
    ```
   - E.G :
     - Create a Weekly file of daily values:
       ```sh
       python project_top_date.py ../outputs/2022/17/*/dailyResult_*
       ```
     - Create a Month file of weekly values:
        ```sh
        python project_top_date.py ../outputs/2022/*/4-*/dailyResult_*
        ```  
* project_top_evolution.py
  - Command:
    ```sh
    python project_top_evolution.py ../outputs/top/[TOP5] ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_* --minDate="[DATE]" --maxDate="[DATE]" --pourcentage=[PERCENTAGE]
    ```
   - E.G :
     - Get the stock list’s corresponding who have already been in the top 5 :
       ```sh
       python project_top_evolution.py  ../outputs/top/* ../outputs/2022/*/*/dailyResult_* --minDate="2022-04-16 9:00" --maxDate="2022-04-26 17:00" --pourcentage=1

  
<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/GabinSMD/bigdata-project.svg?style=flat-square
[contributors-url]: https://github.com/GabinSMD/bigdata-project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GabinSMD/bigdata-project.svg?style=flat-square
[forks-url]: https://github.com/GabinSMD/bigdata-project/network/members
[stars-shield]: https://img.shields.io/github/stars/GabinSMD/bigdata-project.svg?style=flat-square
[stars-url]: https://github.com/GabinSMD/bigdata-project/stargazers
[issues-shield]: https://img.shields.io/github/issues/GabinSMD/bigdata-project.svg?style=flat-square
[issues-url]: https://github.com/GabinSMD/bigdata-project/issues

