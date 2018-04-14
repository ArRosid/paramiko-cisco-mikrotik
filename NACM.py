'''
Author  : Ahmad Rosid Komarudin (ArRosid)
Website : https://arrosid.com/ / http://coretanbocahit.blogspot.co.id/
Email   : rosid@idn.id
Fb      : https://www.facebook.com/ahmadrosidkomarudin
Github  : https://github.com/arrosid
Linkedin: https://www.linkedin.com/in/arrosid/
IG      : https://www.instagram.com/ahmadrosidkomarudin/
'''

import paramiko
import time
from getpass import getpass
import sys
import os

try:
    print "--------------------------------------------------------"
    print "Welcome to Network Automation on Cisco & Mikrotik (NACM)"
    print "--------------------------------------------------------\n\n"

    #Get ip file input from user
    while True:
        try:
            print "---IP File Format---"
            print "--------------------"
            print "----ipadd;vendor----"
            print "--------------------\n\n"
            input_file = raw_input("Input IP File: ")

            #read the file
            r_input_file = open(input_file, "r").readlines()
            break

        except IOError:
            print "IP File does not exsist!, Please Try Again!"
            continue

    #Separate the ip list & vendor list
    ip_list = []
    vendor_list = []

    for x in r_input_file:
        ip_list.append(x.split(";")[0])
        vendor_list.append(x.split(";")[1].strip())

    #Check the connection to the device
    ok_ip_list = []
    ok_vendor_list = []
    print "Checking the connection....."
    for index,ip in enumerate(ip_list):
        response = os.system("ping -c 3 {}".format(ip))

        if response == 0:
            print "\n\n{} is up!\n\n".format(ip)
            ok_ip_list.append(ip)
            ok_vendor_list.append(vendor_list[index])
        else:
            print "\n\n{} is down!\n\n".format(ip)



    #Get config file for cisco
    while True:
        try:
            input_cisco_config = raw_input("Input Cisco Config File: ")

            #read the file
            r_input_cisco_config = open(input_cisco_config, "r").readlines()
            break

        except IOError:
            print "Cisco Config File does not exsist!, Please Try Again!"
            continue


    #Get config file for mikrotik
    while True:
        try:
            input_mikrotik_config = raw_input("Input Mikrotik Config File: ")

            #read the file
            r_input_mikrotik_config = open(input_mikrotik_config, "r").readlines()
            break

        except IOError:
            print "Mikrotik Config File does not exsist!, Please Try Again!"
            continue


    #Get username & password from user
    username = raw_input("Username: ")
    password = getpass()

    print "Doing the configuration....."
    for index,ip in enumerate(ok_ip_list):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ip,username=username,password=password)
        print "Successfull Login to {}".format(ip)

        #if cisco device
        if ok_vendor_list[index].lower() == "cisco":
            conn = ssh_client.invoke_shell()

            for config in r_input_cisco_config:
                conn.send(config + "\n")
                time.sleep(1)
            print "Successfull Configuring {}\n".format(ip)

        #if mikrotik device
        else:
            for config in r_input_mikrotik_config:
                ssh_client.exec_command(config)
                time.sleep(1)
            print "Successfull Configuring {}\n".format(ip)

except KeyboardInterrupt:
    print "\n\nProgram Cancelled by user, Exiting...\n\n"
    sys.exit()
