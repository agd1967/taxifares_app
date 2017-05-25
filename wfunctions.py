# **********************************
# Returns array multidimensional
# con el resultado de la consulta
# **********************************
def getListSQL(msql):

    from dbconnect import connection
    import gc
    b, bonn = connection()

    b.execute(msql)
    rawdata = list(b.fetchall())

    # close connection
    b.close()
    bonn.close()
    gc.collect()

    return (rawdata)

# **********************************
# Returns query for selected post
# **********************************
def getSelPost(pid):

    spost = "SELECT * FROM v_posts WHERE v_posts.post_id=" + str(pid)

    scomm = "SELECT comments.comm_id, comments.content, comments.cdate, "
    scomm += "comments.name, comments.email, comments.user_id, users.username, "
    scomm += "users.name As userdesc, users.email As useremail, users.country As usercountry, posts.post_id "
    scomm += "FROM posts Inner Join comments On comments.post_id = posts.post_id Left Join users "
    scomm += "On comments.user_id = users.user_id WHERE posts.post_id =" + str(pid)

    return(spost, scomm)

#***********************
# Update views and likes
#***********************
def updreads(ruser, postid, rtype):

    from datetime import datetime
    from dbconnect import connection
    import gc

    #check for view or like count
    rsql = "SELECT date_format(rdk_date, '%Y-%m-%d') as rdk_date "
    rsql += "FROM post_rdk WHERE post_id =" + str(postid)
    rsql += " AND ipadd = '" + ruser + "' AND rdk_type = '" + rtype + "'"
    #rsql += "' AND date_format(rdk_date, '%Y-%m-%d') = date_format(CURRENT_DATE, '%Y-%m-%d')"
    print(rsql)
    rlst = getListSQL("blog", rsql)
    if rlst:
        if (rlst[0][0] == datetime.now().strftime('%Y-%m-%d')):
            rdte = 'duplicate'
            print(rlst[0][0])
            print(datetime.now().strftime('%Y-%m-%d'))
        else:
            rdte = 'update'
    else:
        rdte = 'insert'

    print(rdte)

    #rsql += "' AND date_format(rdk_date, '%Y-%m-%d') = date_format(CURRENT_DATE, '%Y-%m-%d')"


    try:

        # check not duplicate
        if rdte != 'duplicate':

            # connect to db
            c, conn = connection("blog")

            # record reads and views
            if rdte == 'insert':
                upsql = "INSERT INTO post_rdk (rdk_id, post_id, ipadd, rdk_type) "
                upsql += "VALUES (0, " + str(postid) + ",'" + ruser + "', '" + rtype + "')"

            else:
                upsql = "UPDATE post_rdk SET rdk_date = date_format(current_date,'%Y-%m-%d') "
                upsql += "WHERE post_id =" + str(postid)
                upsql += " AND ipadd = '" + ruser + "' AND rdk_type = '" + rtype + "'"

            print(upsql)
            c.execute(upsql)
            conn.commit()

            # update reads and views
            if rtype == 'R':
                vrsql = "UPDATE posts SET views=views+1 WHERE post_id =" + str(postid)
            else:
                vrsql = "UPDATE posts SET likes=likes+1 WHERE post_id =" + str(postid)

            print(vrsql)
            c.execute(vrsql)
            conn.commit()

            c.close()
            conn.close()
            gc.collect()
            return ('okey')

        gc.collect()
        return ('dups')

    except Exception as e:
        return ('none')

#***********************
#Check valid Superuser
#***********************
def getsuperusr():

    from flask import session
    # get user, superuser
    username = session.get('username')
    if (username is None): username = ''
    superuser = session.get('superuser')
    if (superuser is None): superuser = ''

    # get user id
    usql = "SELECT * FROM users WHERE username='" + username + "' and status ='1'"
    usup = getListSQL("blog", usql)
    if usup:
        username = usup[0][1]
        superuser = usup[0][8]
    else:
        username = 'none'
        superuser = '0'

    return(username, superuser)

#***********************
#Check valid Email
#***********************
def validemail(email):

    #check notation
    sym_pos = email.find('@')
    dot_pos = email.find('.')
    if (sym_pos > 0) and ((sym_pos + 2 <= dot_pos) and (dot_pos + 2 <= len(email))):
        val_email = 1
    else:
        val_email = -1

    return(val_email)

#***********************
#Check valid Password
#***********************
def password_check(password):

    import re

    # calculating the length
    length_error = len(password) < 4

    # searching for digits
    digit_error = re.search(r"\d", password) is None

    # searching for uppercase
    uppercase_error = re.search(r"[A-Z]", password) is None

    # searching for lowercase
    lowercase_error = re.search(r"[a-z]", password) is None

    # searching for symbols
    symbol_error = re.search(r"\W", password) is None

    # overall result
    password_ok = not ( length_error or digit_error or uppercase_error or lowercase_error or symbol_error )

    return {
        'password_ok' : password_ok,
        'length_error' : length_error,
        'digit_error' : digit_error,
        'uppercase_error' : uppercase_error,
        'lowercase_error' : lowercase_error,
        'symbol_error' : symbol_error,
    }

#***********************
#Get Lat and Lon
#***********************
def getgeoloc():

    import requests
    import json

    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)

    mlat, mlon = 0, 0
    mlat = j['latitude']
    mlon = j['longitude']

    return(mlat, mlon)

# ************************
# Get Country from Lat/Lon
# ************************
def getplace(lat, lon):

    import requests
    import json
    send_url = "http://maps.googleapis.com/maps/api/geocode/json?"
    send_url += "latlng=%s,%s&sensor=false" % (lat, lon)

    v = requests.get(send_url)
    j = json.loads(v.text)
    components = j['results'][0]['address_components']
    country = town = None
    for c in components:
        if "country" in c['types']:
            country = c['long_name']
        if "postal_town" in c['types']:
            town = c['long_name']

    return town, country

#***********************
#Get List of Countries
#***********************
def getWorldList():

    countries = [
        ('ca', 'Canada'),
        ('us', 'United States'),
        ('au', 'Australia'),
        ('NZ', 'New Zealand'),
        ('gb', 'United Kingdom'),
        ('ad', 'Andorra'),
        ('at', 'Austria'),
        ('by', 'Belarus'),
        ('be', 'Belgium'),
        ('ba', 'Bosnia And Herzegowina'),
        ('bg', 'Bulgaria'),
        ('hr', 'Croatia'),
        ('cy', 'Cyprus'),
        ('cz', 'Czech Republic'),
        ('dk', 'Denmark'),
        ('fi', 'Finland'),
        ('fr', 'France'),
        ('de', 'Germany'),
        ('ge', 'Georgia'),
        ('gr', 'Greece'),
        ('hu', 'Hungary'),
        ('is', 'Iceland'),
        ('ie', 'Ireland'),
        ('it', 'Italy'),
        ('kg', 'Kyrgyzstan'),
        ('lv', 'Latvia'),
        ('lt', 'Lithuania'),
        ('li', 'Liechtenstein'),
        ('lu', 'Luxembourg'),
        ('md', 'Moldova'),
        ('mc', 'Monaco'),
        ('nl', 'Netherlands'),
        ('no', 'Norway'),
        ('pl', 'Poland'),
        ('pt', 'Portugal'),
        ('ro', 'Romania'),
        ('ru', 'Russian Federation'),
        ('sm', 'San Marino'),
        ('sk', 'Slovakia'),
        ('si', 'Slovenia'),
        ('es', 'Spain'),
        ('se', 'Sweden'),
        ('ch', 'Switzerland'),
        ('tj', 'Tajikistan'),
        ('tr', 'Turkey'),
        ('uz', 'Uzbekistan'),
        ('ua', 'Ukraine'),
        ('va', 'Vatican City State'),

        ('ag', 'Antigua And Barbuda'),
        ('ar', 'Argentina'),
        ('bs', 'Bahamas'),
        ('bb', 'Barbados'),
        ('bz', 'Belize'),
        ('bo', 'Bolivia'),
        ('br', 'Brazil'),
        ('cl', 'Chile'),
        ('co', 'Colombia'),
        ('cr', 'Costa Rica'),
        ('cu', 'Cuba'),
        ('dm', 'Dominica'),
        ('do', 'Dominican Republic'),
        ('ec', 'Ecuador'),
        ('sv', 'El Salvador'),
        ('gd', 'Grenada'),
        ('gt', 'Guatemala'),
        ('gy', 'Guyana'),
        ('ht', 'Haiti'),
        ('hn', 'Honduras'),
        ('jm', 'Jamaica'),
        ('mx', 'Mexico'),
        ('ni', 'Nicaragua'),
        ('pa', 'Panama'),
        ('py', 'Paraguay'),
        ('pe', 'Peru'),
        ('kn', 'Saint Kitts And Nevis'),
        ('lc', 'Saint Lucia'),
        ('vc', 'St Vincent/Grenadines'),
        ('sr', 'Suriname'),
        ('tt', 'Trinidad And Tobago'),
        ('uy', 'Uruguay'),
        ('ve', 'Venezuela'),

        ('cn', 'China'),
        ('hk', 'Hong Kong'),
        ('jp', 'Japan'),
        ('kr', 'Korea'),
        ('id', 'Indonesia'),
        ('ph', 'Philippines'),
        ('sg', 'Singapore'),
        ('tw', 'Taiwan'),
        ('vn', 'Vietnam'),

        ('ds', 'American Samoa'),
        ('aw', 'Aruba'),
        ('cw', 'Curacao'),
        ('gp', 'Guadeloupe'),
        ('mq', 'Martinique'),
        ('vi', 'Virgin Islands (U.S.)'),
        ('vg', 'Virgin Islands (British)'),
        ('gl', 'Greenland'),
        ('gu', 'Guam'),

        ('af', 'Afghanistan'),
        ('sa', 'Saudi Arabia'),
        ('al', 'Albania'),
        ('dz', 'Algeria'),
        ('ao', 'Angola'),
        ('ai', 'Anguilla'),
        ('aq', 'Antarctica'),
        ('az', 'Azerbaijan'),
        ('bh', 'Bahrain'),
        ('bd', 'Bangladesh'),
        ('bj', 'Benin'),
        ('bm', 'Bermuda'),
        ('bt', 'Bhutan'),
        ('bw', 'Botswana'),
        ('bv', 'Bouvet Island'),
        ('bn', 'Brunei Darussalam'),
        ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'),
        ('KH', 'Cambodia'),
        ('CM', 'Cameroon'),
        ('CV', 'Cape Verde'),
        ('KY', 'Cayman Islands'),
        ('CF', 'Central African Rep'),
        ('TD', 'Chad'),
        ('CX', 'Christmas Island'),
        ('CC', 'Cocos Islands'),
        ('KM', 'Comoros'),
        ('CG', 'Congo'),
        ('CK', 'Cook Islands'),
        ('CI', 'Cote D`ivoire'),
        ('DJ', 'Djibouti'),
        ('TP', 'East Timor'),
        ('EG', 'Egypt'),
        ('GQ', 'Equatorial Guinea'),
        ('ER', 'Eritrea'),
        ('EE', 'Estonia'),
        ('ET', 'Ethiopia'),
        ('FK', 'Falkland Islands (Malvinas)'),
        ('FO', 'Faroe Islands'),
        ('FJ', 'Fiji'),
        ('GF', 'French Guiana'),
        ('PF', 'French Polynesia'),
        ('TF', 'French S. Territories'),
        ('GA', 'Gabon'),
        ('GM', 'Gambia'),
        ('GH', 'Ghana'),
        ('GI', 'Gibraltar'),
        ('GN', 'Guinea'),
        ('GW', 'Guinea-bissau'),
        ('IN', 'India'),
        ('IR', 'Iran'),
        ('IQ', 'Iraq'),
        ('IL', 'Israel'),
        ('JO', 'Jordan'),
        ('KZ', 'Kazakhstan'),
        ('KE', 'Kenya'),
        ('KI', 'Kiribati'),
        ('KP', 'Korea, Democratic People''s Republic of'),
        ('KW', 'Kuwait'),
        ('LA', 'Laos'),
        ('LB', 'Lebanon'),
        ('LS', 'Lesotho'),
        ('LR', 'Liberia'),
        ('LY', 'Libya'),
        ('MO', 'Macau'),
        ('MK', 'Macedonia'),
        ('MG', 'Madagascar'),
        ('MW', 'Malawi'),
        ('MY', 'Malaysia'),
        ('MV', 'Maldives'),
        ('ML', 'Mali'),
        ('MT', 'Malta'),
        ('MH', 'Marshall Islands'),
        ('MR', 'Mauritania'),
        ('MU', 'Mauritius'),
        ('YT', 'Mayotte'),
        ('FM', 'Micronesia'),
        ('MN', 'Mongolia'),
        ('MS', 'Montserrat'),
        ('MA', 'Morocco'),
        ('MZ', 'Mozambique'),
        ('MM', 'Myanmar'),
        ('NA', 'Namibia'),
        ('NR', 'Nauru'),
        ('NP', 'Nepal'),
        ('NC', 'New Caledonia'),
        ('NE', 'Niger'),
        ('NG', 'Nigeria'),
        ('NU', 'Niue'),
        ('NF', 'Norfolk Island'),
        ('MP', 'Northern Mariana Islands'),
        ('OM', 'Oman'),
        ('PK', 'Pakistan'),
        ('PW', 'Palau'),
        ('PG', 'Papua New Guinea'),
        ('PN', 'Pitcairn'),
        ('QA', 'Qatar'),
        ('RE', 'Reunion'),
        ('RW', 'Rwanda'),
        ('WS', 'Samoa'),
        ('ST', 'Sao Tome'),
        ('SN', 'Senegal'),
        ('SC', 'Seychelles'),
        ('SL', 'Sierra Leone'),
        ('SB', 'Solomon Islands'),
        ('SO', 'Somalia'),
        ('ZA', 'South Africa'),
        ('LK', 'Sri Lanka'),
        ('SH', 'St. Helena'),
        ('PM', 'St.Pierre'),
        ('SD', 'Sudan'),
        ('SR', 'Suriname'),
        ('SZ', 'Swaziland'),
        ('SY', 'Syrian Arab Republic'),
        ('TZ', 'Tanzania'),
        ('TH', 'Thailand'),
        ('TG', 'Togo'),
        ('TK', 'Tokelau'),
        ('TO', 'Tonga'),
        ('TN', 'Tunisia'),
        ('TM', 'Turkmenistan'),
        ('TV', 'Tuvalu'),
        ('UG', 'Uganda'),
        ('AE', 'United Arab Emirates'),
        ('VU', 'Vanuatu'),
        ('EH', 'Western Sahara'),
        ('YE', 'Yemen'),
        ('ZR', 'Zaire'),
        ('ZM', 'Zambia'),
        ('ZW', 'Zimbabwe')
    ]

    return(countries)

