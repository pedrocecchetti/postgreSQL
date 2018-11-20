# First importing packages
import psycopg2

#Now connecting to the DB and enabling cursor
db = psycopg2.connect("dbname=news")
c = db.cursor()

#Cleaning views from DB
c.execute('drop view if exists authors_counts;')
c.execute('drop view if exists slug_counts;')

# FIRST QUESTION
print("###############################")
print("Solving First question....")
print("###############################")

#Executing the first Query to fetch the data related to the most viewed articles
c.execute('''select path, count(status) as num 
          from log 
          group by path 
          order by num desc offset 1 limit 3;''')
most_viewed_articles = c.fetchall()

# Transforming the paths into the slugs and fetching the real Titles
articles_slugs = []
articles_titles = []

# Printing the most viewed articles and the number of views
for i in range(0,len(most_viewed_articles)):
    
    articles_slugs.append((most_viewed_articles[i][0])[9:])

    c.execute('''select title from articles where slug like '{}';'''.format(articles_slugs[i]))
    articles_titles.append(c.fetchone())

    print("The # {} most viewed article was '{}' with {} views"
          .format(str(i+1),articles_titles[i][0],most_viewed_articles[i][1]))

# SECOND QUESTION

# Now it creates a view inside the database with the Slugs and the count per slugs
c.execute('''create view slug_counts as 
          select substring(path,10), count(status) as num 
          from log 
          group by path 
          order by num desc offset 1 limit 10;''')
db.commit()

#Now it creates another view with The SUM OF views By author ID
c.execute('''create view authors_counts as 
          select articles.author as author, sum(slug_counts.num) as freq from
          slug_counts join articles on slug_counts.substring = articles.slug  
          group by author 
          order by author;''')
db.commit()

#This query create the Table that answer the 2nd question.
c.execute('''select authors.name, authors_count.freq from
    authors join authors_count on 
    authors_count.author = authors.id;''')

#Extracting the data from DB
authors_views = c.fetchall()

#Creating lists for each info
best_authors = []
best_authors_count = []

for i in range(0,len(most_viewed_articles)):
    # Populating lists
    best_authors.append(authors_views[i][0])
    best_authors_count.append(authors_views[i][1])
    #Printing info
    print("The # {} most viewed author was '{}' with {} views\n"
          .format(str(i+1),best_authors[i],int(best_authors_count[i])))

# THIRD QUESTION
print("###############################")
print("Solving Third question....")
print("###############################")

#First selecting the number of requests per day
c.execute('select cast(time as date) as data ,count(status) as number_of_requests from log group by data order by number_of_requests desc;')
all_requests = c.fetchall()

#Then selecting only BAD requests
c.execute('''select cast(time as date) as data ,count(status) as number_of_requests from log where status like '404 NOT FOUND' group by data order by number_of_requests desc;''')
bad_requests = c.fetchall()


#Creating list for percentages 
requests_percentages = []

for i in range(0,len(all_requests)):
    day_percentage = round((float(bad_requests[i][1])/float(all_requests[i][1])),3)*100
    newitem = [bad_requests[i][0],day_percentage]
    requests_percentages.append(newitem)
    requests_percentages