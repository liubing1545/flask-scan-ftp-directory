#from flask_apscheduler import APScheduler
import look
a = 1

def cron_scan():

    look.send_email()
    # global  a 
    # a = a+1
    # print("kkk:" +  str(a) )

# if __name__ == '__main__':
#     scheduler = APScheduler()