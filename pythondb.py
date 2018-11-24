#!/usr/bin/env python
# First importing packages
import psycopg2

# Now connecting to the DB and enabling cursor
db = psycopg2.connect("dbname=news")
c = db.cursor()

# Cleaning views from DB
c.execute('drop view if exists authors_counts;')
c.execute('drop view if exists slug_counts;')
c.execute('drop view if exists path_access;')

# FIRST QUESTION
print("###############################")
print("Solving First question....")
print("###############################")

# Executing the first Query to fetch the data related to most viewed articles
# and creating a view
c.execute('''create view path_access as
          select substring(path,10) as slug, count(status) as num
          from log
          group by path
          order by num desc offset 1 limit 3;''')
db.commit()

c.execute('''select articles.title, path_access.num from
           articles join path_access
           on path_access.slug = articles.slug;''' )
articles = c.fetchall()

# Printing the most viewed articles and the number of views
for i in range(0, len(articles)):

    print("The # {} most viewed article was '{}' with {} views\n "
          .format(str(i+1), articles[i][0], articles[i][1]))

# SECOND QUESTION
print("###############################")
print("Solving Second question....")
print("###############################")

# Now it creates a view inside the database with Slugs and the count per slugs
c.execute('''create view slug_counts as
          select substring(path,10), count(status) as num
          from log
          group by path
          order by num desc offset 1 limi   t 10;''')
db.commit()

# Now it creates another view with The SUM OF views By author ID
c.execute('''create view authors_counts as
          select articles.author as author, sum(slug_counts.num) as freq from
          slug_counts join articles on slug_counts.substring = articles.slug
          group by author
          order by author;''')
db.commit()

# This query create the Table that answer the 2nd question.
c.execute('''select authors.name, authors_counts.freq from
    authors join authors_counts on
    authors_counts.author = authors.id;''')

# Extracting the data from DB
authors_views = c.fetchall()

# Creating lists for each info
best_authors = []
best_authors_count = []

for i in range(0, len(most_viewed_articles)):
    # Populating lists
    best_authors.append(authors_views[i][0])
    best_authors_count.append(authors_views[i][1])
    # Printing info
    print("The # {} most viewed author was '{}' with {} views\n"
          .format(str(i+1), best_authors[i], int(best_authors_count[i])))

# THIRD QUESTION
print("###############################")
print("Solving Third question....")
print("###############################")

# First selecting the number of requests per day
c.execute('''select cast(time as date) as data ,
                    count(status) as number_of_requests
             from log group by data
             order by number_of_requests desc;''')
all_requests = c.fetchall()

# Then selecting only BAD requests
c.execute('''select cast(time as date) as data ,
            count(status) as number_of_requests
            from log
            where status like '404 NOT FOUND'
            group by data
            order by number_of_requests desc;''')

bad_requests = c.fetchall()


# Creating list for percentages
requests_percentages = []

for i in range(0, len(all_requests)):
    day_percentage = (float(bad_requests[i][1])/float(all_requests[i][1]))
    day_percentage = round(day_percentage, 4)
    day_percentage = day_percentage*100
    newitem = [bad_requests[i][0], day_percentage]
    requests_percentages.append(newitem)
    requests_percentages

# Prints the results for the Day with the most Bad requests

print("\n The day with the most bad requests was {} with {} % \n"
      .format(requests_percentages[0][0], requests_percentages[0][1]))
