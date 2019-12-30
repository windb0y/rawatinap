
import requests
import psycopg2
import mysql.connector
from bs4 import BeautifulSoup

#SQL connection data to connect and save the data in
HOST = "localhost"
USERNAME = "postgres"
PASSWORD = "root"
DATABASE = "rawatinap"


#URL to be scraped
url_to_scrape = 'http://sirs.yankes.kemkes.go.id/fo/json/siranap.php'
#Load html's plain data into a variable
#plain_html_text = requests.get(url_to_scrape)
#parse the data
#soup = BeautifulSoup(plain_html_text.text, "html.parser")

# headers
headers = {
    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
# send request to download the data
response = requests.request("GET", url_to_scrape, headers=headers)
# parse the downloaded data
soup = BeautifulSoup(response.text, 'html.parser')

#print the whole html data to screen
#print(soup.prettify())


#Get the tables where the dates are written.

dates_tables = soup.children
#dates_tables = 'kode_prop\tnama_prop\tkode_rs\tnama_rs\tpemilik\ttotal\tterisi\tkosong\nID.AC\tACEH\t1101015\tRS Umum Daerah Simeulue\tRSUD\t150\t86\t64\nID.AC\tACEH\t1102016\tRS Umum Daerah Aceh Singkil\tRSUD\t97\t23\t74\nID.AC\tACEH\t1105056\tRS Umum Daerah dr. Zubir Mahmud\tRSUD\t155\t103\t52\nID.AC\tACEH\t1114011\tRS Umum Daerah Tamiang\tRSUD\t722\t676\t46'

#for row in dates_tables:
#    print(row)
#dataline = open(dates_tables)
if dates_tables:
    connection = psycopg2.connect(host=HOST, user=USERNAME, password=PASSWORD, dbname=DATABASE)
    kursor = connection.cursor()
    query = "TRUNCATE rumah_sakit"
    kursor.execute(query)
    connection.commit()
    connection.close()

    for row in dates_tables:
        cell = row.split('\n')
        #print(cell)
        for foo in cell:
            if (len(foo) > 0):
                line = foo.split('\t')    
                kode = line[0].strip()        
                provinsi = line[1].strip()
                kode_rs = line[2].strip()
                nama_rs = line[3].strip()
                kepemilikan = line[4].strip()
                tempat_tidur_total = line[5].strip()
                tempat_tidur_isi = line[6].strip()
                tempat_tidur_kosong = line[7].strip()
                

                #Save event data to database
                # Open database connection
                db = psycopg2.connect(host=HOST, user=USERNAME, password=PASSWORD, dbname=DATABASE)
                # prepare a cursor object using cursor() method
                cursor = db.cursor()
                # Prepare SQL query to INSERT a record into the database.
                sql = "INSERT INTO rumah_sakit(kode_rs, nama_rs, provinsi, kepemilikan, tempat_tidur_total, tempat_tidur_isi, tempat_tidur_kosong) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(kode_rs, nama_rs, provinsi, kepemilikan, tempat_tidur_total, tempat_tidur_isi, tempat_tidur_kosong)
                try:
                    # Execute the SQL command
                    cursor.execute(sql)
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()
                # disconnect from server
                db.close()

#connection = mysql.connector.connect(host=HOST, database=DATABASE, user=USERNAME, passwd=PASSWORD)
connection = psycopg2.connect(host=HOST, user=USERNAME, password=PASSWORD, dbname=DATABASE)
kursor = connection.cursor()
query = "DELETE FROM rumah_sakit WHERE id = 1"
kursor.execute(query)
connection.commit()
connection.close()
print("connection close")
    
    

"""
#Iterate through the tables
for table in dates_tables:
    #Iterate through the rows inside the table
    for row in table.select("tr"):
        #Get all cells inside the row
        cells = row.findAll("td")
        #check if there is at least one td cell inside this row
        if(len(cells) > 0):
            #get all the different data from the table's tds
            
            kode_rs = cells[0].text.strip()    
            nama_rs = cells[1].text.strip()            
            provinsi = cells[2].text.strip()            
            kepemilikan = cells[3].text.strip()
            tempat_tidur_total = cells[4].text.strip()
            tempat_tidur_isi = cells[5].text.strip()
            tempat_tidur_kosong = cells[6].text.strip()
            
            #Save event data to database
            # Open database connection
            db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE)
            # prepare a cursor object using cursor() method
            cursor = db.cursor()
            # Prepare SQL query to INSERT a record into the database.
            sql = "INSERT INTO rumah_sakit(kode_rs, nama_rs, provinsi, kepemilikan, tempat_tidur_total, tempat_tidur_isi, tempat_tidur_kosong) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(kode_rs, nama_rs, provinsi, kepemilikan, tempat_tidur_total, tempat_tidur_isi, tempat_tidur_kosong)
            try:
               # Execute the SQL command
               cursor.execute(sql)
               # Commit your changes in the database
               db.commit()
            except:
               # Rollback in case there is any error
               db.rollback()
            # disconnect from server
            db.close()
            
"""          