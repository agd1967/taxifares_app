#**********************************************
#Functions to get json file to write mlb codes
#getJason function
#**********************************************
def getjason():

    import json
    from pprint import pprint


    myjason = 'C:/Users/Antonio/Documents/BigData/BigProjects/worldball/master.json'
    print(myjason)

    with open(myjason) as json_data:
        d = json.load(json_data)
        pprint('Total Players...')
        pprint(len(d['player']))
        for i in range(0, len(d['player'])):
        #for i in range(0, 4):
            #pprint (d['player'][i]['KEY_MLBAM'])
            #pprint(d['player'][i]['KEY_RETRO'])
            #pprint(d['player'][i]['KEY_MLBAM'])
            #pprint(d['player'][i]['KEY_BBREF'])
            #pprint(d['player'][i]['KEY_FANGRAPHS'])
            #pprint(d['player'][i]['THROWS'])
            #pprint(d['player'][i]['BATS'])
            #pprint(d['player'][i]['NAMEFIRST'])
            #pprint(d['player'][i]['NAMELAST'])
            #pprint(d['player'][i]['KEY_LAHMAN'])
            #pprint(d['player'][i]['BIRTHYEAR'])
            #pprint(d['player'][i]['BIRTHMONTH'])
            #pprint(d['player'][i]['BIRTHDAY'])
            #pprint(d)

            myPlayer = []
            myPlayer = [
                d['player'][i]['KEY_RETRO'],
                d['player'][i]['KEY_MLBAM'],
                d['player'][i]['KEY_BBREF'],
                d['player'][i]['KEY_FANGRAPHS'],
                d['player'][i]['THROWS'],
                d['player'][i]['BATS'],
                d['player'][i]['NAMEFIRST'],
                d['player'][i]['NAMELAST'],
                d['player'][i]['KEY_LAHMAN'],
                d['player'][i]['BIRTHYEAR'],
                d['player'][i]['BIRTHMONTH'],
                d['player'][i]['BIRTHDAY']
            ]

            #Write Player into DB
            #writePlayer(myPlayer)

    return

#**********************************************
#Function to write PLAYER into mlbjason DB
#writePlayer function
#**********************************************
def writePlayer(myPlayer):

    # Open database connection and truncate news table to star process
    import mysql.connector

    try:
        cnx = mysql.connector.connect(user='root',
                                    password='mypass',
                                    host='localhost',
                                    database='stats')
        #getting cursos for inserts
        mycursor = cnx.cursor()

        insql = "INSERT INTO MLBJASON VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(insql, myPlayer)
        cnx.commit()
        print('    Inserting player... ' + myPlayer[7])

        # finished, close cursor and database
        mycursor.close()
        cnx.close()

    except mysql.connector.Error as err:
        print("Error {}".format(err))



