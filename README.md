# Weather Data System

This repository is consist of code to fetch data from OpenWeather API and add it to postgresSQL database. This project was creating, using Python, PostgreSQL and for storing the data constantly, Cron job in Linux OS.

## Entity-Relationship Diagram

![alt text](https://i.postimg.cc/KvfwK8kg/weather-ERD.png)

## Prerequisites

Before you begin, ensure you have the following installed:

- PostgreSQL (Version 12.0 or newer recommended)
- pgAdmin 4 (or another PostgreSQL client)
- Python 3.8 or newer
- pip (Python package installer)
- Linux OS or WSL (Windows subsystem for Linux)

## Installation Guide

### 1. Clone the Repository

Start by cloning this repository to your local machine using:

```bash
git clone https://github.com/TuringCollegeSubmissions/martstelm-DE2v2.2.5.git
cd martstelm-DE2.v2.2.5
```

### 2. Set Up Python Environment

Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
```

### 3. Create database

Then, create a new database in PostgreSQL:

```sql
CREATE DATABASE Weather;
```

### 4. Configure Environment Variables

Create a .env file in the src directory of your project and add the following environment variables to configure your database connection:

```env
DB_NAME=Weather
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
APP_ID=<Open Weather API token>
```

### 5. Run application

#### Manual
If you want run files manually:

```bash
python3 hourly_info.py
python3 statistic.py
python3 weekly_info.py
```
#### Automatic
To run script automatically, you can use Cron job. `hourly_info.py` script created to run every hour, `statistic.py` - every day and `weekly_info.py` - every Sunday. To create cron job you need to:

##### Open crontab

```bash
crontab -e
```

#### Edit the crontab file

```nano
0 * * * * /path/to/your/python/executor /path/to/project/folder/hourly_info.py
1 23 * * * /path/to/your/python/executor /path/to/project/folder/statistic.py
59 23 * * 0 /path/to/your/python/executor /path/to/project/folder/weekly_info.py
```

### 6. Backup
 Also, in this repository you will find shell script, where you could generate backup.There was issue with cron, so I did not put it automatically, so if you want to run manually:

```bash
chmod +x ./backup_weather_script.py
./backup_weather_script.py
```

### 7. Verify the Import

To verify that the data has been imported successfully, you can run the following SQL query:

```sql
SELECT *
FROM public.hourly_weather
LIMIT 10;
```

## Usage

You can now use pgAdmin or any other PostgreSQL client to connect to the `Weather` database and run queries, generate reports, or perform analysis.
