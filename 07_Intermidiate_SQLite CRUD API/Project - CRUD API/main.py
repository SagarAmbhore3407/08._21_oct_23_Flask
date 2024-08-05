
#7. Integrate a SQLite database with Flask to perform CRUD operations on a list of items.

from flask import Flask, render_template,request
import sqlite3


app = Flask(__name__)

def create_database():
    conn = sqlite3.connect("items.db")
    curr = conn.cursor()
    conn.execute('''CREATE TABLE IF NOT EXISTS items 
                (item_id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT NOT NULL, item_price INTEGER)''')
    conn.commit()
    curr.close()
    conn.close()

create_database()

def getall():
    conn = sqlite3.connect("items.db")
    curr = conn.cursor()
    curr.execute('''SELECT * FROM items''')
    record = curr.fetchall()
    conn.commit()
    conn.close()
    return record   
    

#page Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add")
def add_page():
    return render_template("add_item.html")

@app.route("/fetch")
def fetch_page():
    return render_template("fetch_items.html")

@app.route("/update")
def update_page():
    return render_template("update_item.html")

@app.route("/delete")
def delete_page():
    return render_template("delete_item.html")


#Action Route
@app.route('/allfetch',methods = ['POST'])
def allfetch():
    if request.method == 'POST':
        record = getall()
        if record:
            message1 = f'Successfully fetched complete Itemrecord...'
            message2 = f"To check See the following list of Items..."
        else:
            if not record:
                record = [f'No records Found in Database.. Its Empty..']
            message1 = f'No record found in database...'
            message2 = f"To check See the following list of Items..."   
        return render_template('showdata.html',record=record, message1 = message1, message2 = message2)


@app.route("/createitem",methods=['POST'])
def create_Item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        item_price = request.form['item_price']
        
        conn = sqlite3.connect('items.db')
        curr = conn.cursor()
        
        curr.execute('''INSERT INTO items (item_name,item_price) values(?,?)''',(item_name,item_price))
        conn.commit()
        conn.close()
        
        record = getall()
        
        message1 = f'The Item "{item_name} with price {item_price}" successfully Added to database...'
        message2 = f"To check See the following list of Items..."
        return render_template('showdata.html',record=record, message1 = message1, message2 = message2)
 
 
    
@app.route("/fetchitem",methods =['POST'] )
def fetch_Item():
    if request.method == 'POST':
        item_name = request.form['item_name']
        
        conn = sqlite3.connect('items.db')
        curr = conn.cursor()
        sql_query = "SELECT * FROM items WHERE item_name = ?"
        curr.execute(sql_query, (item_name,))
        itemdata = curr.fetchall()
        conn.commit()
        conn.close()
        
        
        

        if itemdata:
            message1 = f"Successfully fetched Matched  {len(itemdata)} items from  Record..."
            message2 = f"The Item record list '{itemdata}' is Matched to given Attribute '{item_name}'..."
            record = getall()
        else:
            record = getall()
            if not record:
                record = [f'No records Found with Item name : {item_name}..']
            message1 = f"No Matched record found in Database.." 
            message2 = f"The Item '{item_name}' does not exists in database..." 
            
        return render_template('showdata.html',message1 = message1,message2 = message2,record=record)    
              
@app.route('/updateitem', methods=['POST'])
def update_Item():
    if request.method == 'POST':
        item_id = request.form['item_id']  
        newname = request.form['newitem_name']
        setprice = request.form['item_price'] 
        
        conn = sqlite3.connect('items.db')
        curr = conn.cursor()
        
        query = 'SELECT * FROM items WHERE item_id = ?'
        curr.execute(query, (item_id,))
        existdata = curr.fetchall()
        
        
        if existdata:
            curr.execute("UPDATE items SET item_name = ?, item_price = ? WHERE item_id = ?", (newname, setprice, item_id))
            conn.commit()  # Commit the changes to the database
            
            message1 = f"Successfully updated Item associated with Item id '{item_id}'"
            message2 = f"The Item record '{existdata}' updated to name = {newname} and price = {setprice}... To check see the following record.."
            record = getall()
        else:
            record = getall()
            if not record:
                record = [f'No records Found associated with id = {item_id} ']
            message1 = f"Updation is Unsuccessful.. "
            message2 = f"No record found associated with itemid = {item_id}..." 
        conn.close()   
             
        return render_template('showdata.html', message1=message1, message2=message2, record=record)


@app.route('/deleteone',methods = ['POST'])
def deleteone():
    if request.method == 'POST':
        item_id = request.form['item_id']
        
        conn = sqlite3.connect('items.db')
        curr = conn.cursor()
        
        query = 'SELECT * FROM items WHERE item_id = ?'
        curr.execute(query, (item_id,))
        existdata = curr.fetchall()
        
        
        if existdata:
            curr.execute("DELETE FROM items WHERE item_id = ?",(item_id,))
            conn.commit()  
            record = getall()
            message1 = f"Successfully Deleted Item associated with Item id '{item_id}'"
            message2 = f"The Item record '{existdata[0]}' Has been Deleted from the record .. To check see the following record.."
        else:
            record = getall()
            if not record:
                record = [f'No records Found in Database.. Its Empty..']
            message1 = f"Deletion is Unsuccessful.. "
            message2 = f"No record found associated with itemid = {item_id}..." 
        conn.close()  
        
        return render_template('showdata.html', message1=message1, message2=message2, record=record)
          
@app.route('/deletemultiple',methods = ['POST'])
def deletemultiple():
    if request.method == 'POST':
        item_price = request.form['price']
        
        conn = sqlite3.connect('items.db')
        curr = conn.cursor()
        query = 'SELECT * FROM items WHERE item_price = ?'
        curr.execute(query, (item_price,))
        existdata = curr.fetchall()
        
        if existdata:
            curr.execute("DELETE FROM items WHERE item_price = ?",(item_price,))
            conn.commit()  
            
            message1 = f"Successfully Deleted {len(existdata)} Items associated with Item id '{item_price}'"
            message2 = f"The Item records Has been Deleted from the database .. To check see the following record.."
            record = getall()
        else:
            record = getall() 
            if not record:
                record = [f'No records Found in Database.. Its Empty..']
            message1 = f"Deletion is Unsuccessful.. "
            message2 = f"No record found associated with item_price = {item_price}..." 
        conn.close()
          
             
        return render_template('showdata.html', message1=message1, message2=message2, record=record)    

@app.route('/formattable',methods = ['POST'])
def formattable():
    if request.method == 'POST':
        database = getall()
        record = getall()
        if database:
            conn = sqlite3.connect('items.db')
            curr = conn.cursor()
            curr.execute('DELETE FROM items')
            conn.commit()
            conn.close
            message1 = f'Successfully formatted the the items data...'
            message2 = f"Total {len(database)} items has been deleted from database..."
            record = ["Records has been Deleted..."]
        else:
            if not record:
                record = ["No records Found..."]
            message1 = f'The table is already  empty...'
            message2 = f"Total {len(database)} items has been deleted from database..."
            
        return render_template('showdata.html', message1=message1, message2=message2, record=record)
        

if __name__ == "__main__":
    app.run(debug=True)