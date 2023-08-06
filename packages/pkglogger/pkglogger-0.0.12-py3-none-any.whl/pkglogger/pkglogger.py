# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:37:45 2021

@author: avik_
"""
import datetime,os

def logger(directory,logger_no, function_name, task_status, error, path_output, url):
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
        
        log_file = open(directory + '/' + logger_no + '.txt', 'w+')
        
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
        pprint('Failed to upload to ftp: '+ str(e))
        # log_file = open(os.getcwd() +'/'+ 'Error' + '.txt', 'w+')
        # log_file.write("===============================================\n")
        # log_file.write("===============================================\n")
        # log_file.write("\n<<<<<<<<<<<<<<<<< Error >>>>>>>>>>>>>>>>>>>>>\n", e)
        # log_file.write("\n===============================================\n")
        # log_file.write("===============================================\n")
   

logger('D:\Cogino\Cognino_Project\pkglogger','log1','loggertest','','No Error','/test/dev','http://test.com123') #