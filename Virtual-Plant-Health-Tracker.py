import mysql.connector
from datetime import datetime, timedelta
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="plant_health")
cur = con.cursor()
def add_plant():
    name = input("Enter plant name: ")
    species = input("Enter species: ")
    water_gap = int(input("Ideal watering gap (days): "))
    sunlight = input("Ideal sunlight (low/medium/high): ")

    query = ("INSERT INTO plants(name, species, ideal_water_gap, ideal_sunlight) "
             "VALUES (%s, %s, %s, %s)")
    cur.execute(query, (name, species, water_gap, sunlight))
    con.commit()
    print("Plant added successfully!\n")
def log_entry():
    plant_id = int(input("Enter plant ID: "))
    watered = int(input("Watered? (1=yes,0=no): "))
    sunlight_hrs = int(input("Sunlight hours today: "))
    soil_moist = int(input("Soil moisture (1–10): "))
    
    query = ("INSERT INTO plant_logs(plant_id, date, watered, sunlight_hrs, soil_moisture) "
             "VALUES (%s, %s, %s, %s, %s)")
    cur.execute(query, (plant_id, datetime.now().date(), watered, sunlight_hrs, soil_moist))
    con.commit()
    print("Log recorded!\n")
def health_report():
    plant_id = int(input("Enter plant ID: "))

    cur.execute("SELECT name, ideal_water_gap, ideal_sunlight FROM plants WHERE plant_id=%s",
                (plant_id,))
    plant = cur.fetchone()
    if not plant:
        print("Plant not found.\n")
        return
    name, ideal_gap, ideal_sun = plant
    print(f"\n--- Health Report for {name} ---")
    cur.execute("SELECT date, watered, sunlight_hrs, soil_moisture "
                "FROM plant_logs WHERE plant_id=%s ORDER BY date DESC LIMIT 5",
                (plant_id,))
    logs = cur.fetchall()
    if not logs:
        print("No logs available.\n")
        return
    last_watered = None
    for log in logs:
        if log[1] == 1:
            last_watered = log[0]
            break
    alerts = []
    if last_watered:
        days_since = (datetime.now().date() - last_watered).days
        if days_since > ideal_gap:
            alerts.append("Needs Watering")
    else:
        alerts.append("Never watered recently")
    if logs[0][3] < 4:
        alerts.append("Low Soil Moisture")
    sun = logs[0][2]
    sun_req = {"low": 2, "medium": 4, "high": 6}
    if sun < sun_req.get(ideal_sun, 4):
        alerts.append("Insufficient Sunlight")
    if not alerts:
        print("Plant is healthy!\n")
    else:
        print("Warnings:")
        for a in alerts:
            print(" -", a)
    print()

while True:
    print("=== Virtual Plant Health Tracker ===")
    print("1. Add Plant")
    print("2. Log Daily Entry")
    print("3. View Health Report")
    print("4. Exit")

    ch = input("Enter choice: ")

    if ch == '1':
        add_plant()
    elif ch == '2':
        log_entry()
    elif ch == '3':
        health_report()
    elif ch == '4':
        print("Goodbye!")
        break
    else:
        print("Invalid choice!\n")
