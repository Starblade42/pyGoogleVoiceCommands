#!/usr/bin/python
#
#SMS test via Google Voice
#
#Jonathan Huff
#zarcos@gmail.com
#
#
from googlevoice import Voice
import sys
import BeautifulSoup
from time import sleep
import datetime
import random
import subprocess

smsCommands = {'on':'''Power on''', 'off':'''Shutdown''', 'off_force':'''Force shutdown'''}
adminNumber = '8018306325'
executibles = {'on':'''on_power.py''', 'off':'''on_power.py''', 'off_force':'''off_power_force.py'''}
confirmedText = "I will now execute command "
executibleLocation = "/home/jkh777/"



def isSMScommand(msg):
	text = msg['text']
	for i,key in enumerate(smsCommands):
		if text == smsCommands[key]:
			return True
	return False

def isConfirmPin(msg, pin):
	text = msg['text']
	if text == pin:
		return True
	else:
		return False

def sendVerifyText(msg):
	input = msg['text']
	key = getSmsCommandKey(input)
	pin = str(random.randint(0,99999)).zfill(5)
	verifyText = "Do you want to \n --> " + input + " <-- \nyour computer? Reply with \n--> " + pin + " <--\nwithin 5 minutes."
	sendSMS(adminNumber,verifyText)
	return pin

def verifyReceivedPin(waitTime,pin,msg):
	#Login so we can see if we got what we wanted
	voice.login()
	voice.sms()
	#Extract the SMS so we can look at it in a dictionary
	msgs = extractsms(voice.sms.html)
	#find the last message we received (not perfect. Based on order on the page. Multiple conversations messes this up. Thanks Google Voice!)
	myLastSms = findLastMsgISent(msgs)
	#retrive the command being sent and find the proper key for our dictionary, so we can execute the right command in our command dictionary
	commandKey = getSmsCommandKey(msg['text'])
	#Set up the loop we will use to poll for the text. Eventually I'll make it so this can be a script that runs in response to a script, but polling will do
	timeElapsed = 0
	while timeElapsed < waitTime:
		#log in to get all the most recent SMS messages.
		voice.login()
		voice.sms()
		msgs = extractsms(voice.sms.html)
		# Find the key and the number of the text message to make sure it matches the PIN we want.
		#If it's not a text that is newer than the one we just sent, then it's not valid.
		#This is important, because we might otherwise find the PIN we sent out and think we got a reply, even though we didn't!
		#Self fulfilling prophecies are not allowed
		for i,key in enumerate(msgs):
			if isConfirmPin(msgs[i],pin) & (i > myLastSms):
				executeCommand(commandKey)
				deleteReadSMS()
				return
		#Rather than poll constantly, we'll wait at least 30 seconds. Don't want Google to think we're trying to hack them!
		sleep(30)
		timeElapsed += 30

#-------------------------------------

def executeCommand(key):
	try:
		#Use the subprocess library to call the executible we'll be running in order to complete the SMS command we received.
		subprocess.check_call(executibleLocation + executibles[key])
		#Tell our user that we got their command and just finished doing it for them!
		sendSMS(adminNumber,confirmedText+executibles[key])
		print datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "I will now execute command " + executibles[key] + ".\n"
		#We're finished! Lets clean up our inbox so things will work consistently next time!
		deleteReadSMS()
	except subprocess.CalledProcessError:
		sendSMS(adminNumber, "Power operation >" + executibles[key] + "< failed.")
		print datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "Power operation>" + executibles[key] + "< failed due to CalledProcessError.\n"
	except OSError:
		sendSMS(adminNumber, "Power operation >" + executibles[key] + "< failed.")
		print datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p") + "Power operation>" + executibles[key] + "< failed due to OS error.\n"

def deleteReadSMS():
	#Delete the read SMS messages. Just what it says on the tin.
	for message in voice.sms().messages:
		if message.isRead:
			message.delete()

def sendSMS(number,message):
	#send a message to the NUMBER specified with the MESSAGE specified
	voice.send_sms(number, message)

def getSmsCommandKey(text):
	text
	for i,key in enumerate(smsCommands):
		if text == smsCommands[key]:
			return key

def findLastMsgISent(msgs):
	result = -1
	for msgNumber,message in enumerate(msgs):
		if message['from'] == 'Me:':
			result = msgNumber
	return result

def findLastMsgIReceived(msgs):
	result = -1
	for msgNumber,message in enumerate(msgs):
		if message['from'] != 'Me:':
			result = msgNumber
	return result

def extractsms(htmlsms) :
    """
    extractsms  --  extract SMS messages from BeautifulSoup tree of Google Voice SMS HTML.

    Output is a list of dictionaries, one per message.
    """
    msgitems = []										# accum message items here
    #	Extract all conversations by searching for a DIV with an ID at top level.
    tree = BeautifulSoup.BeautifulSoup(htmlsms)			# parse HTML into tree
    conversations = tree.findAll("div",attrs={"id" : True},recursive=False)
    for conversation in conversations :
        #	For each conversation, extract each row, which is one SMS message.
        rows = conversation.findAll(attrs={"class" : "gc-message-sms-row"})
        for row in rows :								# for all rows
            #	For each row, which is one message, extract all the fields.
            msgitem = {"id" : conversation["id"]}		# tag this message with conversation ID
            spans = row.findAll("span",attrs={"class" : True}, recursive=False)
            for span in spans :							# for all spans in row
                cl = span["class"].replace('gc-message-sms-', '')
                msgitem[cl] = (" ".join(span.findAll(text=True))).strip()	# put text in dict
            msgitems.append(msgitem)					# add msg dictionary to list
    return msgitems


#Main Event Loop
voice = Voice()

voice.login()
voice.sms()
msgs = extractsms(voice.sms.html)
msg = msgs[len(msgs)-1]
key = ""
if isSMScommand(msg):
	key = getSmsCommandKey(msg)
	pin = sendVerifyText(msg)
	verifyReceivedPin(2*60,pin,msg)


