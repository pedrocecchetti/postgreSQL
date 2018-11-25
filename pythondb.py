#!/usr/bin/env python
# First importing packages
import psycopg2

# Now connecting to the DB and enabling cursor
db = psycopg2.connect("dbname=news")
c = db.cursor()


def First_question():
    # FIRST QUESTION
    print("###############################")
    print("Solving First question....")
    print("###############################")

    # Executing the first Query to fetch the data with most viewed articles
    # and creating a view
    c.execute('''select articles.title, path_access.num from
           articles join path_access
           on path_access.slug = articles.slug;''')
    articles = c.fetchall()

    # Printing the most viewed articles and the number of views
    for i in range(0, len(articles)):
            print("The # {} most viewed article was '{}' with {} views\n "
                  .format(str(i+1), articles[i][0], articles[i][1]))


def Second_question():

    # SECOND QUESTION
    print("###############################")
    print("Solving Second question....")
    print("###############################")

    # This query create the Table that answer the 2nd question.
    c.execute('''select authors.name, authors_counts.freq from
    authors join authors_counts on
    authors_counts.author = authors.id;''')

    # Extracting the data from DB
    authors_views = c.fetchall()

    # Creating lists for each info

    for i in range(0, len(authors_views)):
        # Printing info
        print("The # {} most viewed author was '{}' with {} views\n"
              .format(str(i+1), authors_views[i][0], authors_views[i][1]))


def Third_question():

    # THIRD QUESTION
    print("###############################")
    print("Solving Third question....")
    print("###############################")
    c.execute('''select all_requests.data,all_requests.number_of_requests
    as all_requests,
    bad_requests.number_of_requests as bad_requests
    from all_requests join bad_requests
    on all_requests.data = bad_requests.data order by bad_requests desc;''')
    requests = c.fetchall()
    # Creating list for percentages
    requests_percentages = []
    for i in range(0, len(requests)):
        day_percentage = (float(requests[i][2])/float(requests[i][1]))
        day_percentage = round(day_percentage, 4)
        day_percentage = day_percentage*100
        newitem = [requests[i][0], day_percentage]
        requests_percentages.append(newitem)
    # Prints the results for the Day with the most Bad requests
    print("\n The day with the most bad requests was {} with {} % \n"
          .format(requests_percentages[0][0], requests_percentages[0][1]))


def Solve_problem():
    First_question()
    Second_question()
    Third_question()


if __name__ == '__main__':
    Solve_problem()
