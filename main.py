from flask import Flask, render_template, request

app = Flask(__name__)

#home page
@app.route('/')
def home():
  return render_template("index.html")

#get data from file as list
with open("Pokemon.csv") as p: # with method closes the file after it is accessed
    #read headers as a list, split by commas
    headers = p.readline().strip().split(',')
    #read all pokemons into a list
    pokemons = []
    for line in p:
        x = line.strip().split(",")
        #add record to pokemons list
        pokemons.append(x)
    # print(headers)
    # print(pokemons)

## imports records into database

import sqlite3

#create connection
connection = sqlite3.connect("pokedex.db")

#create table to store pokemon
connection.execute("""
    create table if not exists pokemons
    (
    no integer primary key,
    name text,
    type_1 text,
    type_2 text,
    total integer,
    hp integer,
    attack integer,
    defense integer,
    sp_atk integer,
    sp_def integer,
    speed integer,
    generation integer,
    legendary text
    )
    """)

#insert all pokemon records from list read from csv into database
for pokemon in pokemons:
    connection.execute(f"""
        insert or replace into pokemons(no, name, type_1, type_2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary)
        values(
        "{pokemon[0]}",
        "{pokemon[1]}",
        "{pokemon[2]}",
        "{pokemon[3]}",
        "{pokemon[4]}",
        "{pokemon[5]}",
        "{pokemon[6]}",
        "{pokemon[7]}",
        "{pokemon[8]}",
        "{pokemon[9]}",
        "{pokemon[10]}",
        "{pokemon[11]}",
        "{pokemon[12]}"
        )
        """)

connection.commit()

@app.route('/display', methods=['GET','POST'])
def display():
    """
    this function displays a selected number of pokemon with their types and statistics
    """
    if request.method == "GET":
        return render_template("display.html")
    else:
        num = int(request.form['num'])
        #create connection
        connection = sqlite3.connect("pokedex.db")
        #create cursor
        cursor = connection.cursor()
        #select all columns from table
        cursor.execute("select * from pokemons")
        #fetch selected number of pokemons
        display = cursor.fetchmany(num)
        #close connection
        connection.close()
        return render_template("display.html", headers = headers, display = display)

  
@app.route('/type', methods=['GET','POST'])
def type():
  """
  this function displays first pokemon of a type specified by the user
  """
  if request.method == "GET":
    return render_template("type.html")
  else:
    type = request.form['type']
    #create connection
    connection = sqlite3.connect("pokedex.db")
    #create cursor
    cursor = connection.cursor()
    #select all pokemons of specified type
    cursor.execute("select * from pokemons where type_1 = ?", (type.title(),))
    #fetch 1st pokemon
    display = cursor.fetchone()
    #close connection
    connection.close()
    #no pokemons of selected type
    if not display:
        no_such_pokemon = f"no pokemon of type '{type}' :("
    else:
        no_such_pokemon = ""
    return render_template("type.html", headers = headers, display = display, no_such_pokemon = no_such_pokemon)

@app.route('/total_base', methods=['GET','POST'])
def total_base():
  """
  this function displays all pokemon with a total base stat entered by user
  """
  if request.method == "GET":
    return render_template("total-base.html")
  else:
    total_base = request.form['total_base']
    #create connection
    connection = sqlite3.connect("pokedex.db")
    #create cursor
    cursor = connection.cursor()
    #select all pokemons with total base stat entered
    cursor.execute("select * from pokemons where total = ?", (total_base,))
    #fetch all selected pokemon
    display = cursor.fetchall()
    #close connection
    connection.close()
    #no pokemons of selected type
    if not display:
        no_such_pokemon = f"no pokemon with total base stat '{total_base}' :("
    else:
        no_such_pokemon = ""
    return render_template("total-base.html", headers = headers, display = display, no_such_pokemon = no_such_pokemon)

@app.route('/min_specific', methods=['GET','POST'])
def min_specific():
  """
  this function displays all pokemon with a minimum set of stats input by user
  """
  if request.method == "GET":
    return render_template("min-specific.html")
  else:
    attack = request.form['attack']
    defense = request.form['defense']
    speed = request.form['speed']
    #create connection
    connection = sqlite3.connect("pokedex.db")
    #create cursor
    cursor = connection.cursor()
    #select all pokemons that satisfy min stats input
    cursor.execute("""
        select * from pokemons
        where attack >= ?
        and defense >= ?
        and speed >= ?
        """,
        (attack, defense, speed))
    #fetch all selected pokemon
    display = cursor.fetchall()
    #close connection
    connection.close()
    #no pokemons satisfy min stats input
    if not display:
        no_such_pokemon = "no pokemon has such powerful stats :O *shocked pikachu face*"
    else:
        no_such_pokemon = ""
    return render_template("min-specific.html", headers = headers, display = display, no_such_pokemon = no_such_pokemon)
  
@app.route('/legendary', methods=['GET','POST'])
def legendary():
  """
  this function displays all lengedary pokemon that have the specified type1 and type2
  """
  if request.method == "GET":
    return render_template("legendary.html")
  else:
    type1 = request.form['type1']
    type2 = request.form['type2']
    #create connection
    connection = sqlite3.connect("pokedex.db")
    #create cursor
    cursor = connection.cursor()
    #select all legendary pokemon with specified types
    cursor.execute("""
        select * from pokemons
        where legendary = "TRUE"
        and type_1 = ?
        and type_2 = ?
        """,
        (type1.title(), type2.title()))
    #fetch all selected pokemon
    display = cursor.fetchall()
    #close connection
    connection.close()
    #no pokemons of selected type
    if not display:
        no_such_pokemon = f"there exists no legendary pokemon with types '{type1}' and '{type2}' :("
    else:
        no_such_pokemon = ""
    return render_template("legendary.html", headers = headers, display = display, no_such_pokemon = no_such_pokemon)

@app.route('/new', methods=['GET','POST'])
def new():
    """
    this function allows the under to insert new pokemon data to be stored in the database
    """
    #create connection
    connection = sqlite3.connect("pokedex.db")
    #create cursor
    cursor = connection.cursor()
    if request.method == "GET":
        #counts current total n of pokemon in table
        cursor.execute("select count(no) from pokemons")
        total = cursor.fetchone()[0]
        #close connection
        connection.close()
        return render_template("new.html", next = total+1)
    else:
        # print("hi")
        data = []
        # print(data)
        no = int(request.form["no"])
        data.append(no)
        # print(data)
        name = request.form["name"]
        data.append(name)
        # print(data)
        type_1 = request.form["type1"]
        data.append(type_1)
        # print(data)
        type_2 = request.form["type2"]
        data.append(type_2)
        # print(data)
        total = int(request.form["total"])
        data.append(total)
        # print(data)
        hp = int(request.form["hp"])
        data.append(hp)
        # print(data)
        attack = int(request.form["attack"])
        data.append(attack)
        # print(data)
        defense = int(request.form["defense"])
        data.append(defense)
        # print(data)
        sp_atk = int(request.form["sp_atk"])
        data.append(sp_atk)
        # print(data)
        sp_def = int(request.form["sp_def"])
        data.append(sp_def)
        # print(data)
        speed = int(request.form["speed"])
        data.append(speed)
        # print(data)
        generation = int(request.form["generation"])
        data.append(generation)
        # print(data)
        legendary = request.form["legendary"].upper()
        data.append(legendary)
        # print(data)
        #convert data to tuple for insertion
        data = tuple(data)
        # print(data)
        #insert data into database
        cursor.execute("""
            insert or replace into pokemons(no, name, type_1, type_2, total, hp, attack, defense, sp_atk, sp_def, speed, generation, legendary)
            values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            data)
        connection.commit()
        #close connection
        connection.close()
        added = f"new pokemon '{name}' added successfully to database! :)"
        return render_template("new.html", added = added)
       

@app.route('/display_by_hp', methods=['GET','POST'])
def display_by_hp():
  """
  this function displays, in descending order of HP, the count of each Type1 Pokemon type based on a minimum HP entered by the user
  """
  if request.method == "GET":
    return render_template("display-by-hp.html")
  else:
    min = request.form['min']
    #create connection
    connection = sqlite3.connect("pokedex.db")
    #create cursor
    cursor = connection.cursor()
    #read the docstring
    cursor.execute("""
        select type_1, count(type_1) from pokemons
        where hp >= ?
        group by type_1
        order by hp desc
        """, (min,))
    #fetch all selected pokemon
    display = cursor.fetchall()
    #close connection
    connection.close()
    #no pokemons of selected type
    if not display:
        no_such_pokemon = f"no pokemon with minimum hp {min} :("
    else:
        no_such_pokemon = ""
    return render_template("display-by-hp.html", headers = ["type", "count"], display = display, no_such_pokemon = no_such_pokemon)

@app.route('/surprise_me')
def surprise_me():
    """
    this is a very surprising function
    """
    return render_template("surprise-me.html")

@app.route('/such_surprise')
def such_surprise():
   """
   this function actually surprises
   """
   return render_template("surprise-me.html", surprise = True)

#flask runs -- 1m
if __name__ == '__main__':
    app.run()