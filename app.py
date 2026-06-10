from flask import Flask, render_template, request, redirect, session, flash
import json
import datetime


app = Flask(__name__)
app.secret_key = "my_name"

def load_data():
     with open('expense.json','r') as f:
          data = json.load(f)
          return data

def dump_data(data):
     with open('expense.json','w') as f:
          json.dump(data,f,indent=4)

@app.route('/')
def index():
     return render_template('index.html')

@app.route('/log_in',methods=['POST','GET'])
def log_in():
     try:

          if request.method == "GET":
               return render_template('log_in.html')
          username = request.form.get('username')
          password = request.form.get('password')
          users = load_data()
          
          if username in users:
               user = users[username]  # Stores the dict of pas and expenses
               pas = user['password']   # stores real password
               if pas == password: 
                    session['username'] = username 
                    flash("Logged in successfully ")
                    return redirect('/main')
               else:
                    flash("Incorrect password please retry")
                    return redirect('/log_in')
          else:
               flash("No such User Found! Please Retry")
               return redirect('/log_in')

          return render_template('log_in.html')
     except ValueError:
          return "Error Occured"
     
@app.route('/sign_in',methods=['POST','GET'])
def sign_in():
     try:

          if request.method == "GET":
               return render_template('sign_in.html')
          username = request.form.get('username')
          password = request.form.get('password')
          users = load_data()
          
          

          if username in users:
               user = users[username]   # This stores dictionary of that user with pass and expenses
               pas = user['password']   # Stores real pass

               flash("This user already exists. Please retry")
                
               return redirect('/sign_in')

          else:       
               session['username'] = username 
               users[username] = {'password':password, 'expenses':[]}      # creating new key of user name 
               dump_data(users)


               flash('signed in successfully.')
               return redirect('/main')

               

          return render_template('sign_in.html')
     except ValueError:
          return "Error Occured"
     
def welcome_kit():
     if 'username' in session:
          name = session['username']
     now = datetime.datetime.now()
     c_hour = now.hour
     if c_hour <12 :
          return f"Good Morning {name.upper()} 🌞!"
     elif 12 <= c_hour <= 17:
          return f"Good Afternoon {name.upper()} ☀️!"
     elif 17 <= c_hour <= 20:
          return f"Good Evening {name.upper()} 🌻!"
     else:
          return f"Hii {name.upper()} 🌝!"
     
@app.route('/main')
def main():
     welcome = welcome_kit()
     return render_template('main.html',welcome=welcome)

@app.route('/add_expense', methods=['GET','POST'])
def add_expense():
     if request.method == "GET":
          return render_template("add_expense.html")
     
     item = request.form.get('item')
     amount = request.form.get('amount')
     category = request.form.get('category')
     date = request.form.get('date')
     if 'username' in session:
          user = session['username']
     users=load_data()
     details = users[user]
     expenses = details['expenses']
     
     new_expense = {
        "Item": item,
        "Amount": amount,
        "Category": category,
        "Date": date
      }

     expenses.append(new_expense)

     dump_data(users)
     flash("Expense added successfully")
     
     return redirect('/view_expense')

@app.route('/view_expense')
def view_expense():
     users = load_data()      # Loading all data
     if 'username' in session:     # Checking user in session
          user = session['username']
     details = users[user]    # all details of user (pass, expenses)

     expenses = details['expenses']
     if not expenses:
          flash("Ypu have no expenses yet. please add expense first")
          return redirect('/add_expense')
          

     return render_template('view_expense.html', expenses=expenses)

@app.route("/delete_expense", methods=['POST','GET'])
def delete_expense():

     index = request.form.get('index')
     if not index:
          index = -1
     new_index = int(index)

     users = load_data()      # Loading all data
     if 'username' in session:     # Checking user in session
          user = session['username']
     details = users[user]    # all details of user (pass, expenses)

     expenses = details['expenses']
     if not expenses:
          flash("You have no expenses yet. please add first")
          return redirect("/add_expense")

     if 0 <= new_index <= len(expenses):
          expenses.pop(new_index)
          dump_data(users)    # re-inserting the data to database
          flash("Expense deleted successfully")
          return redirect('/delete_expense')
     

     return render_template('delete_expense.html',expenses=expenses)

@app.route('/exit')
def exit():
     if 'username' in session:
          session.pop('username')
     flash("Logged out succesfully 👍")
     return redirect('/')
if __name__ == "__main__":
     app.run(debug=True)