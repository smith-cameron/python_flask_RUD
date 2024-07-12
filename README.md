## Prepared statements
[Queries with Variable Data - Platform](https://login.codingdojo.com/m/506/12464/87420)
we will often want to provide variable data in the query that would be terrible to hard-code into the query
- where the actual value for condition will vary
- where the actual provided data will vary
Whenever we run a query that includes variables, we should use a prepared statement rather than string interpolation.
- %(variableKey)s
- % is a placeholder for mysql and ‘s’ is string
- () is how cursors package will accept the variable tuple/dictionary placeholder(key) string
what this means is that we'll need a string variable for the query and then a dictionary for the values to be used in the string
- we will pass both the query and the dictionary,
## Model - user.py
- [ ] Create user.py file
- [ ] `from mysqlDB import connect` To import connection class
- [ ] Define your schema name either globally or as a class variable
- [ ] model the class after the users table from our database
	- This reflects the dictionary keys will be structured upon query return
```python
from flask_app.config.mysqlDB import connect

class User:
	mydb = 'schemaName'
	def __init__(self, data):
		self.id = data['id']
		self.first_name = data['first_name']
		self.last_name = data['last_name']
		self.email = data['email']
		self.password = data['password']
		self.created_at = data['created_at']
		self.updated_at = data['updated_at']
```
This `__init__` method will take in self (of course) and a variable to carry a dictionary that is being returned from mysql connection file
### [[Model - @classmethod]]
use `@classmethod` to query our database, __WHY__?
*You can use class methods for any methods that are not bound to a specific instance but the class. In practice, you often use class methods for methods that create an instance of the class. When a method creates an instance of the class and returns it, the method is called a factory method.*
- [ ] Multi-line strings will help debug faster with more complicated queries that have more variables
- [ ] call the `connect()` function with arguments
	- [ ] the *schema* you are targeting
	- [ ] the *query* you wish to run
	`dbReturnList = connectToMySQL(schema variable).query_db(query)`
[Queries with Variable Data - Platform](https://login.codingdojo.com/m/506/12464/87420)
```python
@classmethod
  def getAll(cls):
    query = '''
      SELECT *
      FROM users;'''
    dbReturnList = connect(mydb).query_db(query)
    print(dbReturnList)
    output = []
    for each_dictionary in dbReturnList:
      output.append(cls(each_dictionary))
    pprint(output)
    return output
```
	If your query returns nothing you can return it directly
	Else: set it to a variable to make class objects
- [ ] Create an empty list to return - 
- [ ] Loop through results 
- [ ] use `cls` to append class objects into empty list 
- [ ] return something (if required)

---
## user_controller.py
[Retrieving and Displaying Data - Platform](https://login.codingdojo.com/m/506/12464/87419)
- [ ] `from user import User` to import the class from user.py
- [ ] Call the class method and push it up to Jinja in a variable
print() the variable - change the return of class method to just results to discuss the difference
Use `pprint()` - `from pprint import pprint`
Using `pprint()` (pretty print) to view results in your models can make lists of dictionaries easier to read
```python
from flask_app import app
from flask import request, render_template, redirect
from flask_app.models.user import User

@app.route('/')
def index():
    # all_users = User.get_all()
    # print(all_users)
    return render_template('index.html', all_users = all_users)


```


---
## VIEW(HTML & Jinja)
Display the info via Jinja
```html
<h1>Houston we have liftoff!!!!!!!!</h1>

    <table>
        <thead>
            <th>Name</th>
            <th>Email</th>
            <th>Added On</th>
        </thead>
        <tbody>
            {% for user in all_users %}
            <tr>
                <td>{{user.first_name}} {{user.last_name}}</td>
                <td>{{user.email}}</td>
                <td>{{user.created_at}}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

```
### UPDATE
__templates/showOne.html__
**Update form - grave rob create form and refactor on displayOne.html**
using value will preload form fields
```html
  <form action="/users/update/{{user.id}}" method="post">
    <label for="first_name">First Name:</label>
    <input type="text" name="first_name" value="{{user.first_name}}"/>
    <label for="last_name">Last Name:</label>
    <input type="text" name="last_name" value="{{user.last_name}}"/>
    <label for="email">Email:</label>
    <input type="email" name="email" value="{{user.email}}"/>
    <!-- <input type="submit" value="create user" /> -->
    <button>Submit Form</button>
  </form>
```
__controllers/user_controller.py__
==NOTE: How the user id comes from the rout not the form using `print(request.form)`==
```python
@app.route('/users/update/<int:user_id>', methods=['post'])
def update_user(user_id):
    print(request.form)
    data = {
		"id": user_id,
        "fname": request.form["first_name"],
        "lname": request.form["last_name"],
        "email": request.form["email"],
        "pw" : request.form["password"]
    }
    User.updateById(data)
    return redirect('/')
```
__models/user.py__

```python
  @classmethod
  def updateById(cls, data):
    print(data)
    query = '''
    UPDATE users
    SET first_name = %(fname)s,
        last_name = %(lname)s,
        email = %(email)s
    WHERE id = %(id)s;'''
    connect(cls.myDB).query_db(query, data)
```

### DELETE
__templates/form.html__
```html
<td><a href="/user/delete/{{user.id}}">DELETE</a></td>
```
__controllers/user_controller.py__
```python
@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    print(f"User id to delete: {user_id}")
    User.delete_by_id({'id': user_id})
    return redirect('/')
```
__models/user.py__
```python
  @classmethod
  def delete_by_id(cls, data):
    query = '''
    DELETE FROM users
    WHERE id = %(id)s;'''
    results = connect(cls.myDB).query_db(query, data)
    print(f"Results of Delete: {results}")
```

---
## SQL Injection
[SQL Injection - Platform](https://login.codingdojo.com/m/506/12464/87421)
- With string interpolation the variable would be interpreted as its literal value
- With injection the value passed for the variable will be a regular string and not be found in your sanitized(via validations) DB
- The way we run one query and close the connection allows us to run only one query at a time
---
