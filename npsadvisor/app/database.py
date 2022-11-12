from app import db
def test_fetch() -> dict:
    parks = [
        {"name": "yellowstone", "description": "maybe exists idk", "stateAbbr": "HI"}
    ]
    return parks

def get_parks() -> dict:
    conn = db.connect()
    query_res = conn.execute("SELECT name, description, stateAbbr, directionsUrl FROM Parks LIMIT 10;").fetchall() # Use Python's .format() for user input
    conn.close()
    parks = []
    for res in query_res:
        item = {
            "name": res[0],
            "description": res[1],
            "states": res[2],
            "directions": res[3]
        }
        parks.append(item)
    return parks

def search_parks(search_query) -> dict:
    search_query = "%" + search_query + "%"
    conn = db.connect()
    query = "SELECT name, description, stateAbbr, directionsUrl FROM Parks WHERE name LIKE %s LIMIT 2;"
    query_res = conn.execute(query, (search_query)).fetchall()
    conn.close()
    parks = []
    for res in query_res:
        item = {
            "name": res[0],
            "description": res[1],
            "states": res[2],
            "directions": res[3]
        }
        parks.append(item)
    return parks

def get_events() -> dict:
    conn = db.connect()
    query = """SELECT title, e1.description, name, stateAbbr, datestart, dateend
               FROM Parks p1 JOIN Events e1 ON (p1.name = e1.parkfullname)
               ORDER BY title
               LIMIT 15;"""
    query_res = conn.execute(query).fetchall()
    conn.close()
    events = []
    for res in query_res:
        item = {
            "event_title": res[0],
            "event_description": res[1],
            "park_name": res[2],
            "states": res[3],
            "start_date": res[4],
            "end_date": res[5]
        }
        events.append(item)
    return events

def get_events_free_parking() -> dict:
    conn = db.connect()
    query = """SELECT title, e1.description, name, stateAbbr, datestart, dateend
                FROM Parks p1 JOIN Events e1 ON (p1.name = e1.parkfullname)
                WHERE name NOT IN (SELECT p.name
                                   FROM Parks p JOIN ParkingLots l ON(p.parkCode = l.parkCode)
                                   WHERE hasFee=True)
                ORDER BY datestart
                LIMIT 15;"""
    query_res = conn.execute(query).fetchall()
    free_parking_events = []
    conn.close()
    for res in query_res:
        free_parking_events.append(res[0])
    return free_parking_events

def get_parknames() -> dict:
    conn = db.connect()
    query_res = conn.execute("SELECT name FROM Parks LIMIT 2;").fetchall()
    park_name = []
    conn.close()
    for res in query_res:
        item = {
            "name": res[0]
        }
        park_name.append(item)
    return park_name

def insert_new_event(title, description, start_date, end_date, park_name):
    conn = db.connect()
    query = "INSERT INTO Events (title, description, datestart, dateend, parkfullname) VALUES({}, {}, {}, {}, {});".format(
        title, description, start_date, end_date, park_name)
    query_res = conn.execute(query)
    conn.close()

def search_events(search_query) -> dict:
    search_query = "%" + search_query + "%"
    conn = db.connect()
    query = query = """SELECT title, e1.description, name, stateAbbr, datestart, dateend
               FROM Parks as p1 JOIN Events e1 ON (p1.name = e1.parkfullname)
               WHERE p1.name LIKE %s
               ORDER BY title
               LIMIT 15;"""
    query_res = conn.execute(query, (search_query)).fetchall()
    conn.close()
    events = []
    for res in query_res:
        item = {
            "event_title": res[0],
            "event_description": res[1],
            "park_name": res[2],
            "states": res[3],
            "start_date": res[4],
            "end_date": res[5]
        }
        events.append(item)
    return events