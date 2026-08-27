<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
![Python][python-shield]

<!-- PROJECT HEADER -->
<br />
<div align="center">

<h3 align="center">Big Data — IBEX 35 quote pipeline</h3>

  <p align="center">
    Scrape the Madrid stock exchange every hour, aggregate it with MapReduce jobs,
    and push the results into HDFS. A deployment project for the Big Data course at
    the Polytechnic University of Valencia.
    <br />
    <br />
    <a href="https://github.com/GabinSMD/bigdata-project/issues">Report Bug</a>
    ·
    <a href="https://github.com/GabinSMD/bigdata-project/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#how-it-works">How it works</a></li>
        <li><a href="#contributors">Contributors</a></li>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#parameters">Parameters</a></li>
        <li><a href="#commands">Commands</a></li>
      </ul>
    </li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

The aim of this project is to retrieve shares from the stock exchange every hour, from Monday
(9:30 am) to Friday (6:30 pm), and to answer questions about them: biggest risers and fallers,
value ranges over a period, the changing composition of the top 5.

It was built during the Big Data course at the Polytechnic University of Valencia, on the
teaching cluster — which is why the paths below are absolute and start with `/home/alumno`.

> [!NOTE]
> **Archived, 2022.** The scraper uses the Selenium 3 API (`find_elements_by_xpath`), removed in
> Selenium 4, and the quote page it targets has changed since. Expect to fix selectors before this
> runs again.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### How it works

```
expansion.com (IBEX 35)
      │  scraper.py — headless Firefox via Selenium
      ▼
outputs/YYYY/WW/MM-DD/hourlyResult_…     one file per hour, CSV
      │  project_main.py — run by cron on the half hour
      ▼
dailyResult_… → weeklyResult_… → monthlyResult_…   aggregated as the day/week/month closes
      │  at 18:30 only
      ▼
HDFS  outputs/YYYY/WW/MM-DD/…
```

The ten `project_*.py` scripts are **mrjob** MapReduce jobs run over those files: a mapper splits
the CSV line, a reducer folds min, max and first/last quotes per stock. `outputs/` in this
repository still holds the April 2022 run, so the commands below work on real data.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Contributors

<a href="https://github.com/GabinSMD/bigdata-project/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=GabinSMD/bigdata-project" alt="Contributors" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [Python 3.6](https://www.python.org)
* [mrjob](https://mrjob.readthedocs.io/) — MapReduce jobs in Python
* [Hadoop / HDFS](https://hadoop.apache.org/)
* [Selenium](https://www.selenium.dev/) + geckodriver — headless Firefox scraping

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* **selenium** and **mrjob**
  ```sh
  sudo pip install selenium mrjob
  ```
* **geckodriver**
  ```sh
  sudo wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
  sudo tar -xzvf geckodriver-v0.31.0-linux64.tar.gz
  sudo rm geckodriver-v0.31.0-linux64.tar.gz
  sudo mv geckodriver /usr/bin
  ```
* A working **HDFS** client, for the 18:30 upload step

### Installation

1. Go to the Big Data practicas folder in the student's home
   ```sh
   cd /home/alumno/bigdatapracticas/
   ```
2. Get the project, keeping only `proyecto/` where the scripts expect it
   ```sh
   sudo git clone https://github.com/GabinSMD/bigdata-project.git
   cd bigdata-project
   sudo mv proyecto/ ../
   sudo mv README.md ../
   cd ../
   sudo rm -rf bigdata-project
   sudo chown -R alumno proyecto/
   ```
3. Add the cron line
   ```sh
   crontab -e
   ```
   then
   ```
   30 9-18 * * 1-5 /home/alumno/environments/bigdata/bin/python3.6 /home/alumno/bigdatapracticas/proyecto/scripts/project_main.py > /home/alumno/foo.log 2>&1
   ```

The paths are hardcoded in `project_main.py`: moving `proyecto/` elsewhere means editing that file.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

Everything the assignment asked for is done — the list below is kept as the record of it.

- [x] [Main program](proyecto/scripts/project_main.py)
- [x] [Weekly list: initial, final, minimum and maximum value per share](proyecto/scripts/project_stock_list.py)
- [x] [Monthly list: same, for the current month](proyecto/scripts/project_stock_list.py)
- [x] [Given a stock and a date range: min and max quote, plus the percentage fall and rise from the initial value](proyecto/scripts/project_stock_infos.py)
- [x] [Given a stock: lowest and highest quote over the last hour, week and month](proyecto/scripts/project_stock_history.py)
- [x] [The 5 stocks that rose the most over the last week and month](proyecto/scripts/project_stock_increase.py)
- [x] [The 5 stocks that fell the most over the last week and month](proyecto/scripts/project_stock_decrease.py)
- [x] Optional feature:
  - [x] [Given a percentage and a date range: the stocks that rose by that much over the period](proyecto/scripts/project_stock_evolution.py)
- [x] Advanced features:
  - [x] [Given a period: how the top 5 varied over it](proyecto/scripts/project_top_history.py)
  - [x] [Given a precise date: the value of the top 5 at that moment](proyecto/scripts/project_top_date.py)
  - [x] [Given a percentage and a date range: which stocks have already been in the top 5](proyecto/scripts/project_top_evolution.py)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
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
  
  `PERCENTAGE` : enter the percentage wanted, can be negatif or positif
  
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
       python project_stock_infos.py ../outputs/2022/*/*/dailyResult_*  --minDate="2022-04-21 09:30" --maxDate="2022-04-21 19:40" --stockName="acciona"
       ```

* project_stock_history.py
  - Command:
    ```sh
    python project_stock_history.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME]
    ```
   - E.G :
     - Give the minimal and the maximal value of SOLARIA of the last hour, last week and the last month:
       ```sh
       python project_stock_history.py ../outputs/2022/*/*/dailyResult_* --stockName="SOLARIA"
       ```

* project_stock_increase.py
  - Command:
    ```sh
    python project_stock_increase.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME]
    ```
   - E.G :
     - Display the 5 stocks that have risen the most in the last week and month :
       ```sh
       python project_stock_increase.py ../outputs/2022/*/*/dailyResult_* 
       ```
       
* project_stock_decrease.py
  - Command:
    ```sh
    python project_stock_decrease.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/hourlyResult_[FILENAME]
    ```
   - E.G :
     - Display the 5 stocks that have declined the most in the last week and month:
       ```sh
       python project_stock_decrease.py ../outputs/2022/*/*/dailyResult_*
       ```
        
* project_stock_evolution.py
  - Command:
    ```sh
    python project_stock_evolution.py ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME] --pourcentage=[PERCENTAGE] --minDate=[DATE] --maxDate=[DATE]
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
    python project_top_history.py ../outputs/[TOPFILENAME] ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME] --minDate=[DATE] --maxDate=[DATE]
    ```
   - E.G :
     - Take the names of the stock in todayTOP5 and display informations of these stock between 16/04/2022 9:00 and 26/04/2022 15:00
       ```sh
       python project_top_history.py ../outputs/todayTOP5 ../outputs/2022/*/*/dailyResult_* --minDate="2022-4-16 9:00" --maxDate="2022-4-26 15:00"
       ```
       
* project_top_date.py
  - Command:
    ```sh
    python project_top_date.py ../outputs/[TOPFILENAME] ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_[FILENAME] --searchDate="[DATE]"
    ```
   - E.G :
     - Get the value of the Top 5 at a precise date:
       ```sh
       python project_top_date.py ../outputs/todayTOP5 ../outputs/2022/*/*/dailyResult_* --searchDate="2022-4-26 9:00"
       ```
      
* project_top_evolution.py
  - Command:
    ```sh
    python project_top_evolution.py ../outputs/top/[TOPFILENAME] ../outputs/[YEAR]/[WEEK]/[MONTH]-[DAY]/dailyResult_* --minDate="[DATE]" --maxDate="[DATE]" --pourcentage=[PERCENTAGE]
    ```
   - E.G :
     - Get the stock list’s corresponding who have already been in the top 5 :
       ```sh
       python project_top_evolution.py  ../outputs/top/* ../outputs/2022/*/*/dailyResult_* --minDate="2022-04-16 9:00" --maxDate="2022-04-26 17:00" --pourcentage=1       ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

A finished course project, archived as-is. If you want to bring it back to life, the two useful
moves are porting the scraper to the Selenium 4 API and making the paths configurable instead of
hardcoded.

1. Fork the project
2. Create your branch (`git checkout -b feature/selenium-4`)
3. Commit your changes (`git commit -m 'Port scraper to Selenium 4'`)
4. Push to the branch and open a pull request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

No license file: **all rights reserved**. The work is shared between three authors, so it is not
relicensed unilaterally — ask if you want to reuse it.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Gabin Simond — gabin.simond@simondancebros.org

Project link: [https://github.com/GabinSMD/bigdata-project](https://github.com/GabinSMD/bigdata-project)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Universitat Politècnica de València](https://www.upv.es/) — the Big Data course and its cluster
* [expansion.com](https://www.expansion.com/mercados/cotizaciones/indices/ibex35_I.IB.html) — the quote source
* [mrjob](https://mrjob.readthedocs.io/) — MapReduce without the Java
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template) — the shape of this file

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/GabinSMD/bigdata-project.svg?style=for-the-badge
[contributors-url]: https://github.com/GabinSMD/bigdata-project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GabinSMD/bigdata-project.svg?style=for-the-badge
[forks-url]: https://github.com/GabinSMD/bigdata-project/network/members
[stars-shield]: https://img.shields.io/github/stars/GabinSMD/bigdata-project.svg?style=for-the-badge
[stars-url]: https://github.com/GabinSMD/bigdata-project/stargazers
[issues-shield]: https://img.shields.io/github/issues/GabinSMD/bigdata-project.svg?style=for-the-badge
[issues-url]: https://github.com/GabinSMD/bigdata-project/issues
[python-shield]: https://img.shields.io/badge/Python-3.6-3776AB?style=for-the-badge&logo=python&logoColor=white
