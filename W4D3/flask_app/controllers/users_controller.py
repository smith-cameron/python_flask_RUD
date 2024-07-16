from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User

@app.route('/')
def index():
  
  return render_template('index.html') 


@app.route('/users/create', methods=['POST'])
def users_create():
    print(f"request.form: {request.form}") 
    # Send the request.form to the model -> database
    # inserting that form data as a new row in the users table
    user_data ={
      'first_name': request.form['first_name'],
      'last_name': request.form['last_name'],
      'email': request.form['email'],
      'password': request.form['password'],
    }
    user_id = User.create(user_data)
    # redirect to '/dash'
    return redirect(f'/dash/{user_id}')  

@app.route('/dash/<int:user_id>')
def dashboard(user_id):
  print(f"dash user_id: {user_id}")
  
  return render_template('dashboard.html', current_user = User.get_one({'id' : user_id}))

@app.route('/show_all')
def show_all():
  query_results = User.get_all()
  return render_template('show_all.html', all_users = query_results)

@app.route('/logout')
def clear_session():
    session.clear()

    return redirect('/') 

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
  # delete the thing
  User.delete_one({'id' : user_id})
  # redirect to a get route
  return redirect('/show_all')

@app.route('/users/edit/<int:user_id>')
def edit_user(user_id):
  # render edit form
  return render_template('edit.html', 
    user = User.get_one({'id' : user_id})
  )

@app.route('/users/update/<int:user_id>', methods=['POST'])
def users_update(user_id):
    print(f"UPDATE request.form: {request.form}") 
    # Send the request.form to the model -> database
    # inserting that form data as a new row in the users table
    user_data ={
      'id' : user_id,
      'first_name': request.form['first_name'],
      'last_name': request.form['last_name'],
      'email': request.form['email'],
      'password': request.form['password'],
    }
    # Update row in db
    User.update_one(user_data)
    # redirect to '/dash'
    return redirect(f'/dash/{user_id}')  