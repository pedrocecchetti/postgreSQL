# Log Analysis

This is a project of the Udacity FUllStack Web Developer Nanodegree.
This project sets up a PostgreSQL database for a news website and proposes us to answer 3 questions using SQL syntax.
The provided Python script pythondb.py uses the psycopg2 library to query the database
and produce a report that answers the following questions:
- *What are the most popular three articles of all time?*
- *Who are the most popular article authors of all time?*
- *On which days did more than 1% of requests lead to errors?* 

## Instructions
### Requirements
In order to run the program you'll need to have installed in your machine:
- Python
- PostgreSQL
- Psycopg2
- News website DB. You can Download it [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

You could also create a virtual machine with all the specs required for this project:
*These instructions refer to Ubuntu*
- Install VirtualBox from the Ubuntu Software Center.
- Download and Install vagrant from [here](https://www.vagrantup.com/downloads.html)
- Download the configuration file from [here](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
- Unzip the file and cd into the vagrant folder via Terminal:```cd FSND-Virtual-Machine/vagrant```
- Run the following commands on Terminal:
```vagrant up ```
```vagrant ssh```

- After your VM is configured  and you're in the terminal of your VM, it is time to Link your Database to de newsdata.sql
- You will need to have the SQL file inside the project folder and you'll need to run:
``` psql -d news -f newsdata.sql```

*Congratulations, you now have everything configured to execute the program created.

### Before Running the Script
In order to the program to work You will have to have the SQL file in the same folder as the python program.
You are also gonna need to create some `VIEWS` in the database.
- To create the views log into the database in your VM with:
```psql news```
- After that run the queries below in the order that they appear here:
```
    create view path_access as
        select substring(path,10) as slug, count(status) as num
        from log
        group by path
        order by num desc offset 1 limit 3;
``` 

These instructions will be 
You can Download it [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

- First clone this repository:
```git clone https://github.com/pedrocecchetti/postgreSQL.git```
- Then move the sql file into the same directory
- Then change your directory to the one with both files (The python code and the SQL file)
- You'll hav to install **pyscopg2**:
```sudo pip install psycopg2```
- Then run the program:
```python pythondb.py```