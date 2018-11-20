# First importing packages
import psycopg2

#Now connecting to the DB and enabling cursor
db = psycopg2.connect("dbname=news")
c = db.cursor()

# FIRST QUESTION

#Executing the first Query to fetch the data related to the most viewed articles
c.execute('''select path, count(status) as num 
          from log 
          group by path 
          order by num desc offset 1 limit 3;''')
most_viewed_articles = c.fetchall()

# Transforming the paths into the slugs and fetching the real Titles
articles_slugs = []
articles_titles = []

for i in range(0,len(most_viewed_articles)):
    
    articles_slugs.append((most_viewed_articles[i][0])[9:])

    c.execute('''select title from articles where slug like '{}';'''.format(articles_slugs[i]))
    articles_titles.append(c.fetchone())

    print("The # {} most viewed article was '{}' with {} views"
          .format(str(i+1),articles_titles[i][0],most_viewed_articles[i][1]))


# Now it creates a view inside the database with the Slugs and the count per slugs
'''create view slug_counts as 
          select substring(path,10), count(status) as num 
          from log 
          group by path 
          order by num desc offset 1 limit 10;'''
#Now it extracts a Table with The SUM OF views By author ID
'''create view authors_counts as 
          select articles.author as author, sum(slug_counts.num) as freq from
          slug_counts join articles on slug_counts.substring = articles.slug  
          group by author 
          order by author;'''

#This query create the Table that answer the 2nd question.
'''select authors.name, authors_count.freq from
    authors join authors_count on 
    authors_count.author = authors.id;'''