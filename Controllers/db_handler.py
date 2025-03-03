import mysql.connector
import os
from Controllers.email_handler import send_contact_email
from config import load_config

params = load_config()

def get_db_connection():
    if params['local_server']:
        db_password = os.getenv("MYSQL_PASSWORD")
        connection = mysql.connector.connect(
            host=params['mysql']['host'],
            user=params['mysql']['user'],
            password=db_password,
            database=params['mysql']['database']
        )
    else:
        connection = mysql.connector.connect(
            host=params['mysql']['prod_host'],
            user=params['mysql']['prod_user'],
            password=params['mysql']['prod_password'],
            database=params['mysql']['database']
        )
    return connection
def feedback(Name,Email_address,Phone_number,Message,Date):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        feedbackquery = "INSERT INTO feedback (Name, `Email address`, `Phone number`, Message, Date) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(feedbackquery,(Name,Email_address,Phone_number,Message,Date))
        connection.commit()
        cursor.close()
        connection.close()
        return True

    except Exception as e:
        print(f"An error occured: {e}")
        connection.rollback()
        return False

    finally:
        cursor.close()
        connection.close()

def save_blog_post(title, content, date, author, email):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        check_author_query = "SELECT id, blog_count FROM author WHERE email = %s"
        cursor.execute(check_author_query, (email,))
        author_data = cursor.fetchone()

        if author_data:
            author_id , blog_count = author_data
            update_author_query = "UPDATE author SET blog_count = blog_count + 1 WHERE id = %s"
            cursor.execute(update_author_query,(author_id,))
        else:
            insert_author_query = "INSERT INTO author (name,email,blog_count) VALUES (%s,%s,%s)"
            cursor.execute(insert_author_query,(author,email,1))
            author_id = cursor.lastrowid

        insert_blog_query = """
        INSERT INTO upload_blog (title,content,author_id,created_at) VALUES (%s,%s,%s,%s)
        """
        cursor.execute(insert_blog_query,(title, content, author_id, date))
        connection.commit()
        return " Blog Uploaded Successfully! "

    except Exception as e:
        print(f"An error occured: {e}")
        connection.rollback()
        return "Failed to submit data."
    finally:
        cursor.close()
        connection.close()












def get_posts(page=1, per_page=5):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        offset = (page - 1) * per_page
        query = ("""
                 SELECT
                ub.id,
                ub.title,
                ub.content,
                a.name AS author,
                ub.created_at
            FROM upload_blog ub
            JOIN author a ON ub.author_id = a.id
            LIMIT %s OFFSET %s
                 """)
        cursor.execute(query,(per_page, offset))
        posts = cursor.fetchall()
        return posts
        #print(posts)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    finally:
        cursor.close()
        connection.close()
get_posts()