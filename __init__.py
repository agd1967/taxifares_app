# Import Flask and create an instance of flask
from flask import Flask, request, render_template, flash, url_for, redirect, session, make_response, jsonify

import gc

import datetime
from datetime import datetime, timedelta

from dbconnect import connection

from wfunctions import *

app = Flask(__name__)

app.config.update(
    DEBUG=True
    )

#************************************************
# set secret key
#************************************************
app.secret_key = 'taxifares-key'

#************************************************
# Sitemap.xml
#************************************************
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    try:
        """Generate sitemap.xml. Makes a list of urls and date modified."""
        pages = []
        ten_days_ago = (datetime.now() - timedelta(days=7)).date().isoformat()
        # static pages
        for rule in app.url_map.iter_rules():
            if "GET" in rule.methods and len(rule.arguments) == 0:
                pages.append(
                    ["http://global-note.com" + str(rule.rule), ten_days_ago]
                )

        sitemap_xml = render_template('sitemap_template.xml', pages=pages)
        response = make_response(sitemap_xml)
        response.headers["Content-Type"] = "application/xml"

        return response

    except Exception as e:
        return (str(e))

#**************************************************
# Define CONTEXT PROCESSOR for Jinja function call
#**************************************************
@app.context_processor
def my_utility_processor():

    def date_now(format="%d.m.%Y %H:%M:%S"):
        """ returns the formated datetime """
        now = datetime.now()
        return now.strftime(format)

    def date_short(mydate):
        """ returns the formated date """
        return mydate.strftime('%Y-%m-%d')

    def date_long(mydate):
        """ returns the formated date """
        return mydate.strftime('%B %d, %Y')



    return dict(date_now=date_now, date_short=date_short, date_long=date_long)

#************************************************
# Root Page
#************************************************
@app.route('/')
def homepage():

    # Get Client List
    csql = "SELECT client_id, concat(account_no, ' ', first_name, ' ', last_name, ' ', phone_no) as passenger "
    csql += "FROM client WHERE status ='A'"
    csql += " ORDER BY passenger"
    client = getListSQL(csql)

    return render_template("main.html", client=client)

# ************************************************
# Getting Search Client List
# ************************************************
@app.route('/background_client')
def background_client():

    #get parameters
    clientcode = request.args.get('clientcode', 0, type=str)

    #Selected Client
    csql = "SELECT * FROM client WHERE client_id =" + str(clientcode)
    client = getListSQL(csql)

    #Client Fares
    fsql = "SELECT fare_id, passenger_name, phone_no, pickup_address, "
    fsql += "Date_Format(pickup_datetime, '%a, %d %b %Y at %h:%i:%S %p') as pick_long, "
    fsql += "Case "
    fsql += "When DateDiff(Now(), pickup_datetime) < 0 Then Concat((DateDiff(Now(), pickup_datetime) * -1), ' days remaining') "
    fsql += "When (DateDiff(Now(), pickup_datetime) = 0 "
    fsql += " And (Time_To_Sec(TimeDiff(Now(), pickup_datetime)) / 3600 <= 0)) "
    fsql += "Then Concat(Time_Format(TimeDiff(Now(), pickup_datetime)*-1, '%H:%i'), ' hours remaining') "
    fsql += "When (DateDiff(Now(), pickup_datetime) = 0 "
    fsql += " And (Time_To_Sec(TimeDiff(Now(), pickup_datetime)) / 3600 > 0)) "
    fsql += "Then Concat(Time_Format(TimeDiff(Now(), pickup_datetime), '%H:%i'), ' hours ago') "
    fsql += "When DateDiff(Now(), pickup_datetime) = 1 Then Concat(DateDiff(Now(), pickup_datetime), ' day ago') "
    fsql += "Else Concat(DateDiff(Now(), pickup_datetime), ' days ago') "
    fsql += "End As delays "
    fsql += "FROM fares WHERE client_id =" + str(clientcode)
    fsql += " ORDER BY pickup_datetime DESC"
    fare = getListSQL(fsql)

    return jsonify(client=client, fare=fare)

# ************************************************
# Manage Fares
# ************************************************
@app.route('/fares/<int:clientcode>/', methods=["GET", "POST"])
def fares(clientcode):

    # Selected Client
    csql = "SELECT * FROM client WHERE client_id =" + str(clientcode)
    client = getListSQL(csql)

    # Client Fares
    fsql = "SELECT fare_id, passenger_name, phone_no, pickup_address, "
    fsql += "Date_Format(pickup_datetime, '%a, %d %b %Y at %h:%i:%S %p') as pick_long, "
    fsql += "Case "
    fsql += "When DateDiff(Now(), pickup_datetime) < 0 Then Concat((DateDiff(Now(), pickup_datetime) * -1), ' days remaining') "
    fsql += "When (DateDiff(Now(), pickup_datetime) = 0 "
    fsql += " And (Time_To_Sec(TimeDiff(Now(), pickup_datetime)) / 3600 <= 0)) "
    fsql += "Then Concat(Time_Format(TimeDiff(Now(), pickup_datetime)*-1, '%H:%i'), ' hours remaining') "
    fsql += "When (DateDiff(Now(), pickup_datetime) = 0 "
    fsql += " And (Time_To_Sec(TimeDiff(Now(), pickup_datetime)) / 3600 > 0)) "
    fsql += "Then Concat(Time_Format(TimeDiff(Now(), pickup_datetime), '%H:%i'), ' hours ago') "
    fsql += "When DateDiff(Now(), pickup_datetime) = 1 Then Concat(DateDiff(Now(), pickup_datetime), ' day ago') "
    fsql += "Else Concat(DateDiff(Now(), pickup_datetime), ' days ago') "
    fsql += "End As delays "
    fsql += "FROM fares WHERE client_id =" + str(clientcode)
    fsql += " ORDER BY pickup_datetime DESC"
    fare = getListSQL(fsql)

    try:
        if request.method == "POST":

            account = request.form['account']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            phone = request.form['phone']
            pick_address = request.form['pick_address']
            pick_date = request.form['pick_date']
            pick_time = request.form['pick_time']
            drop_address = request.form['drop_address']
            pick_datetime =  pick_date + ' ' +  pick_time

            if account == '' or account.find(' ') > -1:
                flash("Account No. is incomplete, please choose another.")
                return render_template("fares.html", client=client, fare=fare)

            if first_name == '' or first_name.find(' ') > -1 or last_name == '' or last_name.find(' ') > -1:
                flash("Name is incomplete, please choose another.")
                return render_template("fares.html", client=client, fare=fare)

            if phone == '' or phone.find(' ') > -1:
                flash("Phone No. is incomplete, please choose another.")
                return render_template("fares.html", client=client, fare=fare)

            if pick_address == '':
                flash("Pickup Address is incomplete, please choose another.")
                return render_template("fares.html", client=client, fare=fare)

            if pick_date == '' or pick_date.find(' ') > -1 or pick_time == '' or pick_time.find(' ') > -1:
                flash("Date/Time is incomplete, please choose another.")
                return render_template("fares.html", client=client, fare=fare)

            # connect to database
            c, conn = connection()

            # insert client if not found
            if clientcode == 0:

                #check for duplicate account
                dsql = "SELECT count(*) FROM client WHERE account_no='" + account + "'"
                dacc = getListSQL(dsql)
                dcnt, = dacc[0]
                if dcnt > 0:
                    c.close()
                    conn.close()
                    gc.collect()
                    flash("Account No. is already taken, please choose another.")
                    return render_template("fares.html", client=client, fare=fare)

                # insert client
                newClient = [0, account, first_name, last_name, phone, pick_address, drop_address, 'A']
                insql = "INSERT INTO client ( client_id, account_no, first_name, last_name, phone_no, "
                insql += "pickup_address, dropoff_address, status) "
                insql += "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                c.execute(insql, newClient)
                conn.commit()

                #lastrow id
                clientcode = c.lastrowid

            # Insert new fare
            long_name = first_name + ' ' + last_name
            newFare = [0, clientcode, long_name, phone, pick_address, pick_datetime, drop_address, 'D' ]
            insql = "INSERT INTO fares (  fare_id, client_id, passenger_name, phone_no, "
            insql += " pickup_address, pickup_datetime, dropoff_address, status) "
            insql += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            c.execute(insql, newFare)
            conn.commit()

            c.close()
            conn.close()
            gc.collect()

            return redirect(url_for('homepage'))

        gc.collect()
        return render_template("fares.html", client=client, fares=fare)

    except Exception as e:
        print(e)
        error = " Invalid selection. Please, try again."
        return render_template("fares.html", client=client, fares=fare)

#************************************************
# Page Not Found Error 404
#************************************************
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

#************************************************
# Methode not valid Error 404
#************************************************
@app.errorhandler(504)
def methode_not_found(e):
    print(e)
    return render_template("405.html")

#************************************************
# Page/system down Error 500
#************************************************
@app.errorhandler(500)
def page_not_found(e):
    return("Server is momentarily down. Please wait few minutes and return to page."), 500

#************************************************
# Run Website Engine
#************************************************
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5558'))
    except ValueError:
        PORT = 5558
    app.run(HOST, PORT)