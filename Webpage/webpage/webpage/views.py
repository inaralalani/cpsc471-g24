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
        desc = request.GET.get('description1')
        if(food == "yes"):
            food = "true"
        else:
            food = "false"
        db = duckdb.connect('m2kdashboard.db')  # get the db
        num = db.sql("SELECT MAX(ad_id) FROM Labels").fetchnumpy().get('max(ad_id)')[0] #get the largest current ad id
        num = num+1 #increment it
        db.sql("INSERT INTO LABELS (user_upload,ad_id,video_id,labeller_id,ad_or_no,product,food_or_no) VALUES (true," + str(num) + ",'" + adid + "'," + id + ",true,'" + prodname + "'," + food + ")")
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
    return s.render(request, 'researchers data.html')