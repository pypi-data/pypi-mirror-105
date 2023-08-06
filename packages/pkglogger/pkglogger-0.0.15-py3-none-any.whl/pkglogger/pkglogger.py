# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:37:45 2021

@author: avik_
"""
import datetime,os

def logger(logger_no, function_name, task_status, error, path_output, url):
    try :
        if logger_no == '':
            logger_no = "Mention Logger Number"
        if function_name == '':
            function_name = "Mention Funtion Name"
        if task_status == '':
            task_status = "Mention Task Status"
        if error == '':
            error = "No Error"
        if path_output == '':
            path_output = "Mention Path Output"
        if url == '':
            url = "Mention URL Link"
        
        log_file = open(os.getcwd() + '/' + logger_no + '.txt', 'w+')
        print("1.var1 = directory where log file will be created || 2.var2 = Logger number ||\
              3.var3 = Function name || 4.var4 = Task status || 5.var5 = Error || 6.var6 = Output path || 7.var7 = URL Link")
        log_file.write("===============================================\n")
        log_file.write("===============================================\n")
        log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
        log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
        log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
        log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", error])
        log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
        log_file.writelines(["\n<<<<<<<<<<<< URL Link : >>>>>>>>>>>>>>>>> \n", url])
        log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        log_file.write("\n===============================================\n")
        log_file.write("===============================================\n")
        return "Logs Stored !!!" 
    except Exception as e:
        # pass
        exception_type, exception_object, exception_traceback = sys.exc_info()
        print('Input Data issues: ',  exception_type, exception_object, exception_traceback)
        # log_file = open(os.getcwd() +'/'+ 'Error' + '.txt', 'w+')
        # log_file.write("===============================================\n")
        # log_file.write("===============================================\n")
        # log_file.write("\n<<<<<<<<<<<<<<<<< Error >>>>>>>>>>>>>>>>>>>>>\n", e)
        # log_file.write("\n===============================================\n")
        # log_file.write("===============================================\n")
##############################################################################################################
def exceptionlogger(logger_no, function_name, task_status, error, path_output, url,exception_type, exception_object, exception_traceback):
    try :
        if logger_no == '':
            logger_no = "Mention Logger Number"
        if function_name == '':
            function_name = "Mention Funtion Name"
        if task_status == '':
            task_status = "Mention Task Status"
        if error == '':
            error = "No Error"
        if path_output == '':
            path_output = "Mention Path Output"
        if url == '':
            url = "Mention URL Link"
        
        log_file = open(os.getcwd() + '/' + logger_no + '.txt', 'w+')
        print("1.var1 = directory where log file will be created || 2.var2 = Logger number ||\
              3.var3 = Function name || 4.var4 = Task status || 5.var5 = Error || 6.var6 = Output path || 7.var7 = URL Link")
        log_file.write("===============================================\n")
        log_file.write("===============================================\n")
        log_file.writelines(["<<<<<<<<<<<<<Logger Number : >>>>>>>>>>>> \n", logger_no]) 
        log_file.writelines(["\n<<<<<<<<<<<<<Funtion Name : >>>>>>>>>>>>> \n", function_name])
        log_file.writelines(["\n<<<<<<<<<<<<Task Status : >>>>>>>>>>>>>>> \n", task_status])
        log_file.writelines(["\n<<<<<<<<<<<< Error : >>>>>>>>>>>>>>>>>>>> \n", error])
        log_file.writelines(["\n<<<<<<<<<<<< Output Path : >>>>>>>>>>>>>> \n", path_output])
        log_file.writelines(["\n<<<<<<<<<<<< URL Link : >>>>>>>>>>>>>>>>> \n", url])
        log_file.writelines(["\n<<<<<<<<< Exception Type : >>>>>>>>>>>>>> \n", exception_type])
        log_file.writelines(["\n<<<<<<<<< Exception Object : >>>>>>>>>>>> \n", exception_object])
        log_file.writelines(["\n<<<<<<< Exception Traceback : >>>>>>>>>>> \n", exception_traceback])
        log_file.writelines(["\n<<<<<<<<<<<< Logged Time : >>>>>>>>>>>>>> \n", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        log_file.write("\n===============================================\n")
        log_file.write("===============================================\n")
        return "Logs Stored !!!" 
    except Exception as e:
        # pass
        exception_type, exception_object, exception_traceback = sys.exc_info()
        print('Input Data issues: ',  exception_type, exception_object, exception_traceback)
##############################################################################################################         
def exceptiondetail(directory,logger_no, function_name, task_status, error, path_output, url):
    exception_type, exception_object, exception_traceback = sys.exc_info()
    return exceptionlogger(directory,logger_no, function_name, task_status, error, path_output, url,exception_type, exception_object, exception_traceback)


logger('log2','loggertest','','No Error','/test/dev','http://test.com123') #