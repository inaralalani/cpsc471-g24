from django.http import HttpResponse
from django.template import loader
import django.shortcuts as s
import duckdb
def landing(request):
    return s.render(request, 'landingpage.html')
def options(request):
    return s.render(request, 'options.html')
def rlogin(request):
    return s.render(request, 'researchers-login.html')
def llogin(request):
    return s.render(request, 'labelers-login.html')
def ldashboard(request):
    if(request.method == "POST"):
        db = duckdb.connect('m2kdashboard.db') #get the db
        id = request.POST.get('labeler-id')
        try:
            int(id) #check if it's actually an int, so as not to throw errors
        except:
            id = -1 #give -1 so it autofails the sql
        pas = request.POST.get('labeler-password')
        if(len(db.sql("SELECT * FROM Users WHERE user_id=" + str(id) + " AND user_password='" + pas + "' AND user_type!='researcher'").fetchnumpy().get('user_id')) != 0): #if username and password combo exist
            return s.render(request, 'labelers dashboard.html') #get the dashboard
        else: #otherwise go back to teh beginning for now
            return s.render(request, 'landingpage.html')
    else: #should be a get request, for submitting data
        #start getting all the form data
        id = request.GET.get('user-id')
        try:
            int(id) #check if it's actually an int, so as not to throw errors
        except:
            id = -1 #again, just an error value
        adid = request.GET.get('ad-id')
        food = request.GET.get('food-ad')
        tech1 = request.GET.get('technique1')
        prodname = request.GET.get('product-name')
        bradname = request.GET.get('brand-name')
        desc = request.GET.get('description1')
        if(food == "yes"):
            food = "true"
        else:
            food = "false"
        db = duckdb.connect('m2kdashboard.db')  # get the db
        num = db.sql("SELECT MAX(ad_id) FROM Labels").fetchnumpy().get('max(ad_id)')[0] #get the largest current ad id
        num = num+1 #increment it
        db.sql("INSERT INTO LABELS (user_upload,ad_id,video_id,labeller_id,ad_or_no,ad_brand,product,food_or_no) VALUES (true," + str(num) + ",'" + adid + "'," + id + ",true,'" + bradname + "','" + prodname + "'," + food + ")")
        return s.render(request, 'labelers dashboard.html')  # get the dashboard
def rdashboard(request):
    if(request.method == "POST"):
        db = duckdb.connect('m2kdashboard.db')  # get the db
        id = request.POST.get('researcher-id')

        try:
            int(id)  # check if it's actually an int, so as not to throw errors
        except:
            id = -1  # give -1 so it autofails the sql
        pas = request.POST.get('researcher-password')
        if (len(db.sql(
                "SELECT * FROM Users WHERE user_id=" + str(id) + " AND user_password='" + pas + "' AND user_type='researcher'").fetchnumpy().get(
                'user_id')) != 0):  # if username and password combo exist
            return s.render(request, 'researchers dashboard.html')  # get the dashboard
        else:  # otherwise go back to teh beginning for now
            return s.render(request, 'landingpage.html')
def rdata(request):
    db = duckdb.connect('m2kdashboard.db')  # get the db
    if request.method == "POST":
        food = formatfood(request)
        label = formatlabel(request)
        market = formatmarket(request)

    else:
        food = db.sql("SELECT * FROM Foods").fetchnumpy()  # assume get the food data
        label = db.sql("SELECT * FROM Labels").fetchnumpy() # same as the first
    technique = db.sql("SELECT * FROM Techniques").fetchnumpy()
    foodtable = [[None] * 6 for i in range(len(food.get('food_id')))] #list of lists to make a table, initialized with enough size
    for i in range(len(food.get('food_id'))): #create a row-by-row table
        foodtable[i][0] = food.get('food_id')[i]
        foodtable[i][1] = food.get('ad_id')[i]
        foodtable[i][2] = food.get('one_many')[i]
        foodtable[i][3] = food.get('name')[i]
        foodtable[i][4] = food.get('eval_method')[i]
        foodtable[i][5] = food.get('health')[i]
    labeltable = [[None] * 8 for i in range(len(label.get('user_upload')))] #now for labels
    for i in range(len(label.get('user_upload'))):
        labeltable[i][0] = label.get('user_upload')[i]
        labeltable[i][1] = label.get('ad_id')[i]
        labeltable[i][2] = label.get('video_id')[i]
        labeltable[i][3] = label.get('labeller_id')[i]
        labeltable[i][4] = label.get('ad_or_no')[i]
        labeltable[i][5] = label.get('ad_brand')[i]
        labeltable[i][6] = label.get('product')[i]
        labeltable[i][7] = label.get('food_or_no')[i]
    markettable = [[None] * 5 for i in range(len(market.get('review_id')))]
    for i in range(len(market.get('review_id'))):
        markettable[i][0] = market.get('review_id')[i]
        markettable[i][1] = market.get('ad_id')[i]
        markettable[i][2] = market.get('technique_id')[i]
        markettable[i][3] = market.get('feature')[i]
        markettable[i][4] = market.get('character')[i]
    techtable = [[None] * 2 for i in range(len(technique.get('technique_id')))]
    for i in range(len(technique.get('technique_id'))):
        techtable[i][0] = technique.get('technique_id')[i]
        techtable[i][1] = technique.get('technique_name')[i]
    context = {}
    context['food'] = foodtable
    context['label'] = labeltable
    context['market'] = markettable
    context['technique'] = techtable
    return s.render(request, 'researchers data.html', context=context)

def formatfood(request): # helper function to format the food sql request, you'll see more of these
    db = duckdb.connect('m2kdashboard.db')  # get the db
    foodfilter = request.POST.get('food-filter', None)
    foodeval = request.POST.get('food-eval', None)
    foodname = request.POST.get('food-name')
    if foodfilter == "all" and foodeval == "all" and (foodname == None or foodname==""):  # show all data
        foodreq = "SELECT * FROM Foods"
        food = db.sql(foodreq).fetchnumpy()
    else:
        foodreq = "SELECT * FROM Foods WHERE "
        if foodfilter == "healthy":
            foodreq += "health='healthy'"
            if foodeval == "healthcan" or foodeval == "uoft" or foodeval == "limited":
                foodreq += " AND "
        elif request.POST.get('food-filter') == "unhealthy":
            foodreq += "health='unhealthy'"
            if foodeval == "healthcan" or foodeval == "uoft" or foodeval == "limited":
                foodreq += " AND "

        if foodeval == "healthcan":
            foodreq += "eval_method='health-can'"
            if (foodname != None and foodname!=""):
                foodreq += " AND "
        elif foodeval == "uoft":
            foodreq += "eval_method='uoft'"
            if (foodname != None and foodname!=""):
                foodreq += " AND "
        elif foodeval == "limited":
            foodreq += "eval_method='limited'"
            if (foodname != None and foodname!=""):
                foodreq += " AND "
        if (foodname != None and foodname!=""):
            foodreq += "name='" + foodname + "'"
        food = db.sql(foodreq).fetchnumpy()
    return food

def formatlabel(request): #stuff for formatting labels
    db = duckdb.connect('m2kdashboard.db')  # get the db
    labelfood = request.POST.get('label-filter', None)
    prodname = request.POST.get('product-name')
    if labelfood == "all" and (prodname =='' or prodname == None):
        labelreq = "SELECT * FROM Labels"
        label = db.sql(labelreq).fetchnumpy()
    else:
        labelreq = "SELECT * FROM Labels WHERE "
        if labelfood == "yes":
            labelreq += "food_or_no=true"
            if prodname !='' and prodname != None:
                labelreq += " AND "
        if labelfood == "no":
            labelreq += "food_or_no=false"
            if prodname != '' and prodname != None:
                labelreq += " AND "
        if (prodname != None and prodname!=""):
            labelreq += "product='" + prodname + "'"
        label = db.sql(labelreq).fetchnumpy()
    return label
def formatmarket(request):
    db = duckdb.connect('m2kdashboard.db')  # get the db
    featurename = request.POST.get('marketing-feature')
    if (featurename != None and featurename != ""):
        print("SELECT * FROM Marketing WHERE feature='" + featurename + "'")
        return db.sql("SELECT * FROM Marketing WHERE feature='" + featurename + "'").fetchnumpy()
    elif (featurename == None or featurename == ""):
        return db.sql("SELECT * FROM Marketing").fetchnumpy()