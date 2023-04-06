import mysql.connector
from bs4 import BeautifulSoup
import re
# # connect to SQL database
mydb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "root",
    database = "bincom_database"
)

# create cursor object
mycursor = mydb.cursor()

# Execute sql query for polling unit
mycursor.execute("SELECT * FROM announced_pu_results")
data = mycursor.fetchall()

mycursor.close()

# open and write in file
with open('index.html', 'w') as f:
    f.write('<html>\n')
    f.write('  <head>\n')
    f.write('    <title>MySQL data in Python</title>\n')
    f.write('  </head>\n')
    f.write('  <body>\n')
    f.write('  <P>Result of individual polling unit\n ')
    f.write('    <table>\n')
    f.write('      <tr>\n')
    f.write('        <th>polling unit id</th>\n')
    f.write('        <th>Column party</th>\n')
    f.write('        <th>Column score</th>\n')
    f.write('      </tr>\n')
    
    for row in data:
        f.write('      <tr>\n')
        f.write(f'        <td>{row[1]}</td>\n')
        f.write(f'        <td>{row[2]}</td>\n')
        f.write(f'        <td>{row[3]}</td>\n')
        f.write('      </tr>\n')
    
    f.write('    </table>\n')
    f.write('  </P>\n')
    f.write('</html>')
    
# 
# 
#   question 2
# Result of polling unit in an LGA

# create cursor
lga_cursor = mydb.cursor()
lga_cursor.execute("SELECT * FROM lga")
lga_data = lga_cursor.fetchall()



i = 0
while i< 2: 
    with open('lga.html', 'w') as f:
        f.write('<html>\n')
        f.write('  <head>\n')
        f.write('    <title>MySQL data in Python</title>\n')
        f.write('  </head>\n')
        f.write('  <body>\n')
        f.write('  <P>Result of lga\n ')
        f.write( "<label for='lga'> Choose your lga:  </label>")
        f.write("<select name='lga' id='lga_id'>")
        
        for row in lga_data:
            f.write(f"<option value='{row[1]}'> {row[2]}({row[1]}) </option>\n")
        

        f.write("</select>")
  
        f.write('    <table>\n')
        f.write('      <tr>\n')
        f.write('        <th>lga name</th>\n')
        f.write('        <th>party name</th>\n')
        f.write('        <th>party score</th>\n')
        f.write('      </tr>\n')
        

        f.write('  </body>\n')
        f.write('</html>')
        
    lga_id = None
    with open('lga.html',"r") as fp:
        # use beautiful soup to parse html document
        soup = BeautifulSoup(fp,'html.parser')
        selection_tag = soup.select_one('#lga_id')
        selection_option = selection_tag.select_one('option')
        selected_option_value = selection_option['value']
        lga_id = int(selected_option_value)

    #  if statement runs if you have beautiful soup can get the value of the option tag  
    if lga_id :
        lga_result_cursor = mydb.cursor()
        lga_result_cursor.execute("SELECT * FROM announced_lga_results WHERE lga_name = %s",(lga_id,))
        lga_result_data = lga_result_cursor.fetchall() 
        # print ( lga_result_data)
        lga_result_cursor.close()

        with open('lga.html', 'w') as f:
            f.write('<html>\n')
            f.write('  <head>\n')
            f.write('    <title>MySQL data in Python</title>\n')
            f.write('  </head>\n')
            f.write('  <body>\n')
            f.write('  <P>Result of lga</p>\n ')
            f.write( "<label for='lga'> Choose your lga:  </label>")
            f.write("<select name='lga' id='lga_id'>\n")
            
            for row in lga_data:
                f.write(f"<option value ='{row[1]}' > ({row[1]}) {row[2]} </option>\n")
            
        
            f.write("</select>")
            
            # queries the data base with the value gotten
            if lga_id :
                lga_result_cursor = mydb.cursor()
                lga_result_cursor.execute("SELECT * FROM announced_lga_results WHERE lga_name = %s",(lga_id,))
                lga_result_data = lga_result_cursor.fetchall() 
                # print ( lga_result_data)
                lga_cursor.close()
                lga_result_cursor.close()
                
            
            f.write('    <table>\n')
            f.write('      <tr>\n')
            f.write('        <th>lga name</th>\n')
            f.write('        <th>party name</th>\n')
            f.write('        <th>party score</th>\n')
            f.write('      </tr>\n')
            
            for row in lga_result_data:
                f.write('      <tr>\n')
                f.write(f'        <td>{row[1]}</td>\n')
                f.write(f'        <td>{row[2]}</td>\n')
                f.write(f'        <td>{row[3]}</td>\n')
                f.write('      </tr>\n')
            
            f.write('    </table>\n')
            f.write('  </P>\n')
            f.write('  </body>\n')
            f.write('</html>')

        
    i+=1
# 
# 
#   Question 3   
# Result of LGA
lga_pu_cursor = mydb.cursor()

# Execute sql query for total score of each party in a polling unit
lga_pu_cursor.execute("SELECT party_abbreviation, SUM(party_score) as total FROM announced_pu_results GROUP BY party_abbreviation")
lga_pu_data = lga_pu_cursor.fetchall()
# print(lga_pu_data)
lga_pu_cursor.close()

# Open and write to new_polling_unit.html file
with open('new_polling_unit.html', 'w') as f:
            f.write('<html>\n')
            f.write('  <head>\n')
            f.write('    <title>MySQL data in Python</title>\n')
            f.write('  </head>\n')
            f.write('  <body>\n')
            f.write('  <P>Total result for parties in announced polling unit</p> \n ')
            f.write('    <table>\n')
            f.write('      <tr>\n')
            f.write('        <th>party name</th>\n')
            f.write('        <th>party collated result</th>\n')
            f.write('      </tr>\n')
            
            for row in lga_pu_data:
                f.write('      <tr>\n')
                f.write(f'        <td>{row[0]}</td>\n')
                f.write(f'        <td>{row[1]}</td>\n')
                f.write('      </tr>\n')
            
            f.write('    </table>\n')
            f.write('  </P>\n')
            f.write('  </body>\n')
            f.write('</html>')