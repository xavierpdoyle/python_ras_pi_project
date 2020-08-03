import os
import RPi.GPIO as GPIO
import time
# bare minimum terminal commands
import random

import urllib.request 

import subprocess
#lcdglo: lines=0, charPerLine=1, timeUnit=2, textDisplaySpeed=3, lledPin = 4
lcdGlo = [(2),(16),(0.14),(0.35),(21)]
#lcdGlo[0]=int(lcdGlo[0])
#numCharLcdSet=int(lcdGlo[1])
print("num of lines: ", lcdGlo[0])
print("num of char per line: ", lcdGlo[1])

ButtonPin=16
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(lcdGlo[4], GPIO.OUT)
GPIO.output(lcdGlo[4], GPIO.LOW)

GPIO.setup(ButtonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

createdFileName=""

lcdGlo[2]=0.14

lcdGlo[3]=0.35

print("time unit value: ", lcdGlo[2])

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                                        
GPIO.setup(lcdGlo[4], GPIO.OUT)#set LED pin's mode as output
GPIO.output(lcdGlo[4], GPIO.LOW)#sets LED pin to be OFF at start

GPIO.setup(ButtonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)#this sets our ButtonPin's mode as input with the internal pullup

#bare minimum LCD screen:
#LCD pins assigned are VERY simple-- just follow this:
# vcc goes to 5 volts
# GND goes to some ground (either the long blue line marked with the negative sign or any pin marked with "GND")
# SDA goes to SDA (or SDA1 if you've got it)
# SCL goes to SCL (or SCL1 if that's what you see)

import datetime

# Modified 2018-09-30 to use Matt Hawkins' LCD library for I2C available
# from https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/lcd_i2c.py
import RPi.GPIO as GPIO
import time

# Additional stuff for LCD
import smbus

xGlo= [(0x27),(0x80),(0xC0),(0x94),(0xD4)]
print("I2C device address: ", xGlo[0])
print("ram address line 1: ", xGlo[1])
print("ram address line 2: ", xGlo[2])
print("ram address line 3: ", xGlo[3])
print("ram address line 4: ", xGlo[4])


#LCD pin assignments, constants, etc
I2C_ADDR  = 0x27 # I2C device address
#int(lcdGlo[1]) = lcdGlo[1]   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

LCD_BACKLIGHT  = 0x08  # On
#LCD_BACKLIGHT = 0x00  # Off

ENABLE = 0b00000100 # Enable it

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


# Ultrasonic pin assignments
SR04_trigger_pin = 20
SR04_echo_pin = 21

# LCD commands
LCD_CMD_4BIT_MODE = 0x28   # 4 bit mode, 2 lines, 5x8 font
LCD_CMD_CLEAR = 0x01
LCD_CMD_HOME = 0x02   # goes to position 0 in line 0
LCD_CMD_POSITION = 0x80  # Add this to DDRAM address

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by standard marking

# Set up the SR04 pins
GPIO.setup(SR04_trigger_pin, GPIO.OUT)
GPIO.setup(SR04_echo_pin, GPIO.IN)
GPIO.output(SR04_trigger_pin, GPIO.LOW)

#Open I2C interface
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1


def lcd_init():
  try:
    lcd_byte(0x33,LCD_CMD) # 110011 Initialise
    lcd_byte(0x32,LCD_CMD) # 110010 Initialise
    lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
    lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off 
    lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
    lcd_byte(0x01,LCD_CMD) # 000001 Clear display
    time.sleep(E_DELAY)
  except:
    print("LCD screen not currently plugged in")

def lcd_byte(bits, mode):
  bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
  bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

  # High bits
  bus.write_byte(I2C_ADDR, bits_high)
  lcd_toggle_enable(bits_high)

  # Low bits
  bus.write_byte(I2C_ADDR, bits_low)
  lcd_toggle_enable(bits_low)

def lcd_toggle_enable(bits):
  # Toggle enable
  time.sleep(E_DELAY)
  bus.write_byte(I2C_ADDR, (bits | ENABLE))
  time.sleep(E_PULSE)
  bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
  time.sleep(E_DELAY)

def lcd_string(message,line):
  # Send string to display
  try:
    message = message.ljust(int(lcdGlo[1])," ")

    lcd_byte(line, LCD_CMD)

    for i in range(int(lcdGlo[1])):
      lcd_byte(ord(message[i]),LCD_CHR)
  except:
    print(message)

# functions not in the original library
def lcd_xy(col, row):
        lcd_byte(LCD_CMD_POSITION+col+(64*row), LCD_CMD)

def lcd_msg(msg_string):
        for i in range(0, len(msg_string)):
                lcd_byte(ord(msg_string[i]), LCD_CHR)


def readFromFile(file_in):
    """
    Counts the number of lines in a file_in
    file_in: string - file name
    Returns: integer - number of lines in file_in
    """
    
    # create file object fin for reading

    fin = open(file_in,'r')

    # create and initialize local variable to store result
    numLines = 0


    # iterate through fin with line loop variable
    for line in fin:
        numLines = numLines + 1
        #print(line)


    # close fin object
    fin.close()

    # return result
    return line

#////////////////////////////////////////////////////////////////////////

def readFromFileArr(file_in):
    """
    Counts the number of lines in a file_in
    file_in: string - file name
    Returns: integer - number of lines in file_in
    """
    
    # create file object fin for reading

    fin = open(file_in,'r')

    # create and initialize local variable to store result
    numLines = 0

    arrSongs=[""]
    arrSongs
    # iterate through fin with line loop variable
    for line in fin:

        numLines = numLines + 1
        print("line is", line)
        arrSongs.append(line)        
        print("Array Song number",numLines,"is", arrSongs[numLines])

    # close fin object
    fin.close()

    # return result
    return arrSongs

#////////////////////////////////////////////////////////////////////////

def quickGrabAll(inputUrl,outputText):
    grabBytes= urllib.request.urlopen(inputUrl)
    bText = grabBytes.read()
    outputText = bText.decode("utf8")
    grabBytes.close()
    return outputText


                                  
#  `O+:+XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX///:  
#  /+.`./XXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO-.`.X  
#  /X/:+XXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOO++XO  
# `-```/OOOOOOOOXXXOOOOOOOOOOOOOOOOOOOOOO(@)(@)Z---->[3V3][5V]
# `-```/OOOOOOOOOOOOOOOOO+:+-XOXO+OOOOOOO(@)(@)Z---->[SDA1][5V]
# `-```/OOOOOOOOOOOOOOO-O/+OX::XX/OOOOOOO(@)(@)Z---->[SCL1][Ground]
#  /OOOOOOOOOOOOOOOOOO+/OX/O++:-OOOOOOOOO(@)(@)Z---->[GPIO4][GPIO14]
#  /OOOOOOOOOOOOOOOOOOO/XO:X///XX/OOOOOOO(@)(@)Z---->[Ground][GPIO15]
#  /OOOOOOOOOOOOOOOOOOOOOOOOXXOXXXOOOOOOO(@)(@)Z---->[GPIO17][GPIO18]
# .+XXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOO(@)(@)Z---->[GPIO27][Ground]
# :````````:OOOOOOOOOOO+++++++++XOOOOOOOO(@)(@)Z---->[GPIO22][GPIO23]
# :````````:OOOOOOOOOOO+++++++++XOOOOOOOO(@)(@)Z---->[
# :````````:OOOOOOOOOOO+++++++++XOOOOOOOO(@)(@)Z---->[
# :````````:OOOOOOOOOOO+++++++++XOOOOOOOO(@)(@)Z---->[
# :````````:OOOOOOOOOOOOOOXXXXXXOOOOOOOOO(@)(@)Z---->[
# ./XXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOO(@)(@)Z---->[
#  /OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO(@)(@)Z---->[
#  /OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO(@)(@)Z---->[GPIO5][Ground]
#  /OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO(@)(@)Z---->[GPIO6][GPIO12]
#  /XXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOO(@)(@)Z---->[GPIO13][Ground]<
#`OO.````````/OOOOOOOOOOOOOOOOOOOOOOOOOOO(@)(@)Z---->[GPIO19][GPIOlcdGlo[1]]<
#`OO.````````/OOOOOOOOOOOOOO++++++OOOOOOO(@)(@)Z---->[GPIO26][GPIO20]
# .+OOOOOOOOOOOOOOOOOOOOOOOO++++++OOOOOOO(@)(@)Z---->[GPIO21][Ground]
#  /X:-:XOOOOOOOOOOOOOOOOOOO++++++OOOOOOOOOO:-/X  
#  /O.`.OOOOOOOOOOOOOOOOOOOOOOOXXXOOOOOOOOO:.`.X  
#  /OXXXXXXXXXXXXXXOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  
#  /OO-```````````OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  
#  /OO-```````````OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO  
#  /OO-```````````OOOO`````````-OOOO``````````OO  
#  /OO-```````````OOOO`````````-OOOO``````````OO  
#  /OO-```````````OOOO`````````-OOOO``````````OO  
#  /OO-```````````OOOO`````````-OOOO``````````OO  
#  /OO-```````````OOOO`````````-OOOO``````````OO  
#   :/-```````````////`````````-+//+`````````.O-  
#     .```````````` #```````````   #``````````    

#now we define the morse code function:
#This conversion would be about converting dots/dashes to letters)
def dd_to_let(convertedLetter):
        if(convertedLetter=='.-'):
                convertedLetter='a'
        elif(convertedLetter=='-...'):
                convertedLetter='b'
        elif(convertedLetter=='-.-.'):
                convertedLetter='c'
        elif(convertedLetter=='-..'):
                convertedLetter='d'
        elif(convertedLetter=='.'):
                convertedLetter='e'
        elif(convertedLetter=='..-.'):
                convertedLetter='f'
        elif(convertedLetter=='--.'):
                convertedLetter='g'
        elif(convertedLetter=='....'):
                convertedLetter='h'
        elif(convertedLetter=='..'):
                convertedLetter='i'
        elif(convertedLetter=='.---'):
                convertedLetter='j'
        elif(convertedLetter=='-.-'):
                convertedLetter='k'
        elif(convertedLetter=='.-..'):
                convertedLetter='l'
        elif(convertedLetter=='--'):
                convertedLetter='m'
        elif(convertedLetter=='-.'):
                convertedLetter='n'
        elif(convertedLetter=='---'):
                convertedLetter='o'
        elif(convertedLetter=='.--.'):
                convertedLetter='p'
        elif(convertedLetter=='--.-'):
                convertedLetter='q'
        elif(convertedLetter=='.-.'):
                convertedLetter='r'
        elif(convertedLetter=='...'):
                convertedLetter='s'
        elif(convertedLetter=='-'):
                convertedLetter='t'
        elif(convertedLetter=='..-'):
                convertedLetter='u'
        elif(convertedLetter=='...-'):
                convertedLetter='v'
        elif(convertedLetter=='.--'):
                convertedLetter='w'
        elif(convertedLetter=='-..-'):
                convertedLetter='x'
        elif(convertedLetter=='-.--'):
                convertedLetter='y'
        elif(convertedLetter=='--..'):
                convertedLetter='z'
        elif(convertedLetter=='.----'):
                convertedLetter='1'
        elif(convertedLetter=='..---'):
                convertedLetter='2'
        elif(convertedLetter=='...--'):
                convertedLetter='3'
        elif(convertedLetter=='....-'):
                convertedLetter='4'
        elif(convertedLetter=='.....'):
                convertedLetter='5'
        elif(convertedLetter=='-....'):
                convertedLetter='6'
        elif(convertedLetter=='--...'):
                convertedLetter='7'
        elif(convertedLetter=='---..'):
                convertedLetter='8'
        elif(convertedLetter=='----.'):
                convertedLetter='9'
        elif(convertedLetter=='-----'):
                convertedLetter='0'

        else:
                convertedLetter='?'
        return convertedLetter

#----------------------------------------------------------
def end_message(convertedMessage):
        convertedMessage=(str(convertedMessage)+'. ---OUT---')
        print('COMPLETE MESSAGE: ', str(convertedMessage))
        return convertedMessage
#----------------------------------------------------------


def run_new_letter_funcs(ddCombo, convertedLetter):
        convertedLetter=ddCombo
        #print('Debug: our midconversion letter is ', str(convertedLetter))
        convertedLetter=dd_to_let(convertedLetter)
        print('our new letter is ', str(convertedLetter))
        return convertedLetter


#----------------------------------------------------------
def add_word_to_message(convertedWord,convertedMessage):
        convertedMessage=(str(convertedMessage)+' '+str(convertedWord))
        print('our current message so far is ', str(convertedMessage))
        return convertedMessage
#----------------------------------------------------------
def add_letter_to_word(convertedLetter,convertedWord):
        convertedWord=(str(convertedWord)+str(convertedLetter))
        print('our current word so far is ', str(convertedWord))
        return convertedWord

#----------------------------------------------------------



def specifictionary(filterToApply, messageToFilter):
    filteredMessage=""
    if (filterToApply == "Display Settings"):
        filteredMessage=messageToFilter
        filteredMessageU=filteredMessage.upper()
        if (filteredMessageU.count("INCH")==0 and filteredMessageU.count("3.5")==0 and filteredMessage[0].upper() != "3"):
            if (filteredMessageU.count("LCD")>=1 or filteredMessageU.count("4")>=1 or filteredMessageU.count("LINE")>=1 or filteredMessageU.count("CHAR")>=1 or filteredMessageU.count("I2C")>=1):
                filteredMessage
                if (filteredMessage.upper() == "4" or filteredMessage.upper() == "I2C LCD DISPLAY"):
                    print("You selected:")
                    print("4- Change number of lines and characters per line displayed by I2C LCD display")
                    filteredMessage="I2C LCD Display"
                else:
                    filteredMessage="I2C LCD Display"
                    print("We think you meant: "+str(filteredMessage))
            return filteredMessage



def writeToFile(createdFileName,userSays1,inputModeW):
    if(userSays1==""):
        if (inputModeW=="Keyboard"):
            userSays1=input("What text would you like to enter into the file?")
        else:
            userSays1=morseCode(userSays1,"")
    with open('/home/pi/Desktop/finalProject/'+str(createdFileName), 'w') as f:
            f.write(""+userSays1)
        
def writeSettingsToFile(createdFileName,userSays1,inputModeW):
    if(userSays1==""):
        if (inputModeW=="Keyboard"):
            userSays1=input("What text would you like to enter into the file?")
        else:
            userSays1=morseCode(userSays1,"")
    with open('/home/pi/pyAtStartBman/'+str(createdFileName), 'w') as f:
            f.write(""+userSays1)
    

def lcdSays(lcdTextIn):

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lcdGlo[4], GPIO.OUT)
    GPIO.output(lcdGlo[4], GPIO.LOW)
        


    global xGlo
    global lcdGlo
    

    
    line1Arr=0*lcdGlo[1]
    line2Arr=1*lcdGlo[1]
    line3Arr=3*lcdGlo[1]
    line4Arr=4*lcdGlo[1]
    
    line1S=""
    line2S=""
    countLcdArr=0
    totalLinesToPrint=len(lcdTextIn)

    print(lcdTextIn)



    while(line2Arr<(totalLinesToPrint)):
        
        time.sleep(lcdGlo[3])
        line1S= lcdTextIn[line1Arr:(line1Arr+lcdGlo[1])]
        #print(line1S)
        lcd_string(""+str(line1S)+"           ", xGlo[1])

        line2S= lcdTextIn[line2Arr:(line2Arr+lcdGlo[1])]
        #print(line2S)
        lcd_string(""+str(line2S)+"           ", xGlo[2])
        time.sleep(lcdGlo[3])
        print(""+str(line1S)+str(line2S))

        if(0 == GPIO.input(ButtonPin)):
            print(lcdTextIn)
            return

        if(lcdGlo[0]>=4):
            time.sleep(lcdGlo[3])
            line1S= lcdTextIn[line1Arr:(line1Arr+lcdGlo[1])]
            #print(line1S)
            lcd_string(""+str(line1S)+"           ", xGlo[3])

            line2S= lcdTextIn[line2Arr:(line2Arr+lcdGlo[1])]
            #print(line2S)
            lcd_string(""+str(line2S)+"           ", xGlo[4])
            time.sleep(lcdGlo[3])

            line1Arr=line1Arr+lcdGlo[1]
            line2Arr=line2Arr+lcdGlo[1]



        if(0 == GPIO.input(ButtonPin)):
            print(lcdTextIn)
            return

        blinkOutputAi=0
        if(blinkOutputAi==1):
          d2=[]
          l=(""+str(line1S)+str(line2S))
          #l = input("Now how about super profound?  ")
          for i in range(0, len(l)):
              #print(l[i]," in Morse is ",MorseConvert(l[i]), \
                  #" which looked up again is ",MorseConvert(MorseConvert(l[i])))
              d2.append(MorseConvert(l[i]))
              if(0 == GPIO.input(ButtonPin)):
                  print(l)
                  print(d2)
                  print(lcdTextIn)                
                  return              
          AiLedBlinkTimes=[]
          for i in range(0, len(d2)):
                for j in range(0, len(d2[i])):
                      #print("debug print out our dots and dashes: ", d2[i][j])
                      if(d2[i][j] == "."):
                            AiLedBlinkTimes.append(1)
                      if(d2[i][j] == "-"):
                            AiLedBlinkTimes.append(3)
                      if(d2[i][j] == " "):
                            AiLedBlinkTimes.append(-2)
                      if(d2[i][j] == "&"):
                            AiLedBlinkTimes.append(-7)
                      if(d2[i][j] == "?"):
                            AiLedBlinkTimes.append(-7)
                                                    
                      if(0 == GPIO.input(ButtonPin)):
                          print(l)
                          print(d2)
                          print(lcdTextIn)                
                          return                           
                                              
                                  
          for i in range(0, len(AiLedBlinkTimes)):
                #print(AiLedBlinkTimes[i])
                if(AiLedBlinkTimes[i]>0):
                      #print("Led ON")
                      GPIO.output(lcdGlo[4], GPIO.HIGH) 
                      #print((AiLedBlinkTimes[i])*lcdGlo[2])
                      
                      time.sleep((AiLedBlinkTimes[i])*lcdGlo[2])
                      #print("Led OFF")
                      GPIO.output(lcdGlo[4], GPIO.LOW) 
                      time.sleep(1*lcdGlo[2])
                      #print(str(1*lcdGlo[2]))
                else:
                      #print("Led OFF")
                      GPIO.output(lcdGlo[4], GPIO.LOW) 
                      time.sleep(-1*lcdGlo[2]*(AiLedBlinkTimes[i]))
                      #print(-1*lcdGlo[2]*(AiLedBlinkTimes[i]))

                      if(0 == GPIO.input(ButtonPin)):
                          print(l)
                          print(d2)
                          print(lcdTextIn)                
                          return                           
        line1Arr=line1Arr+lcdGlo[1]
        line2Arr=line2Arr+lcdGlo[1]






    if (0 == GPIO.input(ButtonPin)):

        GPIO.output(lcdGlo[4], GPIO.HIGH)
        print("Message  WITHOUT LED blinks in Morse Code")
        time.sleep(1)
        
        GPIO.output(lcdGlo[4], GPIO.LOW) 



    while(line2Arr<(totalLinesToPrint) and 0 == GPIO.input(ButtonPin)):
        
        time.sleep(lcdGlo[3])
        line1S= lcdTextIn[line1Arr:(line1Arr+lcdGlo[1])]
        #print(line1S)
        lcd_string(""+str(line1S)+"           ", xGlo[1])

        line2S= lcdTextIn[line2Arr:(line2Arr+lcdGlo[1])]
        #print(line2S)
        lcd_string(""+str(line2S)+"           ", xGlo[2])
        time.sleep(lcdGlo[3])
        print(""+str(line1S)+str(line2S))

        line1Arr=line1Arr+lcdGlo[1]
        line2Arr=line2Arr+lcdGlo[1]

        if(lcdGlo[0]>=4):
            time.sleep(lcdGlo[3])
            line1S= lcdTextIn[line1Arr:(line1Arr+lcdGlo[1])]
            #print(line1S)
            lcd_string(""+str(line1S)+"           ", xGlo[3])

            line2S= lcdTextIn[line2Arr:(line2Arr+lcdGlo[1])]
            #print(line2S)
            lcd_string(""+str(line2S)+"           ", xGlo[4])
            time.sleep(lcdGlo[3])

            line1Arr=line1Arr+lcdGlo[1]
            line2Arr=line2Arr+lcdGlo[1]







        
#======================================================================================================
Morse2 = ['a','.- ','b','-... ','c','-.-. ','d','-.. ','e','. ','f','..-. ','g','--. ', \
      'h','.... ','i','.. ','j','.--- ','k','-.- ','l','.-.. ','m','-- ','n','-. ','o','--- ', \
      'p','.--. ','q','--.- ','r','.-. ','s','... ','t','- ','u','..- ','v','...- ', \
      'w','.-- ','x','-..- ','y','-.-- ','z','--.. ','1','.---- ','2','..--- ','3','...-- ', \
      '4','....- ','5','..... ','6','-.... ','7','--... ','8','---.. ','9','----. ','0','----- ',' ','&']


#======================================================================================================
#======================================================================================================
def MorseConvert(s):
      global Morse2
      try:
            if s[0] < '0':
                  retval = Morse2[Morse2.index(s)-1]
            else:
                  retval = Morse2[Morse2.index(s[0].lower())+1]
      except:
                  retval = '?'
      return retval
#======================================================================================================  

def email_sending(receiver,content):


	import smtplib



	mail = smtplib.SMTP('smtp.gmail.com',587)

	mail.ehlo()


	mail.starttls()

	Address = ''

	Address = '###########@gmail.com'

	emailSite=''



	#brentxavierproject	
	mail.login('######@gmail.com','###########')

	mail.sendmail('########@gmail.com',receiver,content)

	mail.close()


def checkEmail():
  
  import poplib

  from email import parser

  pop_conn = poplib.POP3_SSL('###.gmail.com')

  pop_conn.user('###@gmail.com')

  pop_conn.pass_('########')

  #pulls the content from the server
  messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]

  # puts back together messages for printing
  messages = ["\n".join(mssg[1]) for mssg in messages]

  #parses through messages
  messages = [parser.Parser().parsestr(mssg) for mssg in messages]
  for message in messages:
      print(message)
  pop_conn.quit()




def morseCode(textInOut, specFilter):

    
    
    lcdGlo[2]=0.14
        
    lcdGlo[4] = 21
    ButtonPin=lcdGlo[1]
    print("Light blinking starting now")

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(lcdGlo[4], GPIO.OUT)
    GPIO.output(lcdGlo[4], GPIO.LOW)
            
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)                                        
    GPIO.setup(lcdGlo[4], GPIO.OUT)#set LED pin's mode as output
    GPIO.output(lcdGlo[4], GPIO.LOW)#sets LED pin to be OFF at start

    GPIO.setup(ButtonPin, GPIO.IN, pull_up_down = GPIO.PUD_UP)#this sets our ButtonPin's mode as input with the internal pullup


    OFFtimer=0 #this is the amount of time that the LED was OFF for
    ONtimer=0 #this is the amount of time that the LED was ON for

    ONtimerStarted=0 #this checks if our ONtimer has started ticking yet-- if is HAS,
    # then we we set ONtimerStarted=1... when our timer turns off, ONtimerStarted is
    # reset back to ZERO.  OFFtimerStarted follows the same basic principle.
    OFFtimerStarted=0

    startTimeOn=1.111 #records exact time at the moment the LED is turned ON
    startTimeOff=1.111 #records exact time at the moment the LED is turned OFF

    onList = []
    offList = []

    numButtonPushes = 0
    numButtonReleases = 0

    waitTime=0

    input_state = GPIO.input(ButtonPin)
    
    
    #==============SECTION 2: DEFINING FUNCTIONS (AND DECLARING VARIABLES THAT USE THEM)========
    #===========================================================================================

    convertedLetter='c'
    convertedWord=''
    convertedMessage='Message: '
        
    try:
      lcd_string("Enter Morse Code:                     ", LCD_LINE_2)
    except:
      print("Enter Morse Code:")

    while(0 != GPIO.input(ButtonPin)):
        if (waitTime==0):
            startWaiting=time.time()
        waitTime=time.time()-startWaiting
        print("waiting for user to push button... current wait time is",waitTime)
        if(waitTime>0.5):
                sadString="@@@@@"
                return sadString
        
    waitTime=0


    lcdButtonDisplay=""
    #lcd_string("Input detected:            ", LCD_LINE_1)
    lcd_string(lcdButtonDisplay+"                                 ", LCD_LINE_2)

    #SECTION 4: "SIMON SAYS" WHILE LOOP RECORDS BUTTON PUSHES UNTIL 14 TU PASS WITHOUT A PRESS================================================================
    #===========================================================================================

    dotDashMess='Message: '#these are the first 9 characters.  dot/dashes start on

    currentLineNum=0

    while(OFFtimer<(lcdGlo[1]*lcdGlo[2])):#if user fails to blink light for 10 or more time units, our code
    #assumes he is done recording and ends the while loop, thereby proceeding on to the
    #next part where our code will plug the ON/OFF timer arrays into a PARROT array,
    #where the LED will parrot our own button pushes exactly.

    #===========================================================================================   
        if ((0 == GPIO.input(ButtonPin))):#When button is pushed this if loop runs           
            GPIO.output(lcdGlo[4], GPIO.HIGH) #turns LED on

            if (OFFtimerStarted != 0):#all info gathered from the previously run elseloop goes here
                offList.append(OFFtimer)
                numButtonReleases=numButtonReleases+1
                if (OFFtimer>(3*lcdGlo[2])):
                    print (dotDashMess + '-')
                    lcdButtonDisplay=lcdButtonDisplay+" "
                    currentLineNum=int((len(lcdButtonDisplay))/lcdGlo[1])
                    #lcd_string("Input detected:            ", LCD_LINE_1)
                    lcd_string(lcdButtonDisplay[(currentLineNum*lcdGlo[1]):((currentLineNum*lcdGlo[1])+lcdGlo[1])]+"", LCD_LINE_2)               

            OFFtimer=0
            OFFtimerStarted=0#the off timer values are all reset to 0
            
            
            if (ONtimerStarted==0):#recording the time at the moment of the button push
                startTimeOn=time.time()
                ONtimerStarted=1
            
            ONtimer= time.time() - startTimeOn
            print("current time elapsed on button push ",numButtonPushes+1," is ",(ONtimer/lcdGlo[2]),"time units")
            
    #===========================================================================================
        else:#when button is NOT pushed
            GPIO.output(lcdGlo[4], GPIO.LOW) #turns LED off        
            if (ONtimerStarted != 0):
                onList.append(ONtimer)#add our latest ONtimer recorded to our on array
                currentTimeOff=0
                #I want to print out dash every time I get a dash and add that to the messageSoFar
                if (ONtimer>(3*lcdGlo[2])):
                    print (dotDashMess + '-')
                    lcdButtonDisplay=lcdButtonDisplay+"-"
                    currentLineNum=int((len(lcdButtonDisplay))/lcdGlo[1])
                    #lcd_string("Input detected:            ", LCD_LINE_1)
                    lcd_string(lcdButtonDisplay[(currentLineNum*lcdGlo[1]):((currentLineNum*lcdGlo[1])+lcdGlo[1])]+"", LCD_LINE_2)                                 
                else:
                    print (dotDashMess+ '.')
                    lcdButtonDisplay=lcdButtonDisplay+"."
                    currentLineNum=int((len(lcdButtonDisplay))/lcdGlo[1])
                    #lcd_string("Input detected:            ", LCD_LINE_1)
                    lcd_string(lcdButtonDisplay[(currentLineNum*lcdGlo[1]):((currentLineNum*lcdGlo[1])+lcdGlo[1])]+"", LCD_LINE_2)                          
                numButtonPushes = numButtonPushes +1
                print("final time duration recorded for button push",numButtonPushes," is ",(ONtimer/lcdGlo[2])," time units")            
            ONtimer=0
            ONtimerStarted=0#the on timer values are all reset to 0
            
            if (OFFtimerStarted==0):#recording the time at the moment of the button RELEASE
                startTimeOff=time.time()
                OFFtimerStarted=1
            
            OFFtimer= time.time() - startTimeOff
            print("current time elapsed SINCE button press number ",numButtonPushes+1," is ",OFFtimer/lcdGlo[2]," time units")

    #===============================================================================================
    #===============================================================================================
    #===============================================================================================
    #SECTION 5: FOR LOOP USED TO PARROT USER BUTTON INPUT (AND TRANSFER VALUES FROM ARRAYS INTO=====
    # STRINGS)-- it also performs 2 successive conversions with the aid of functions: first,========
    #	1) from button input times into dots/dashes, and then ======================================
    #	2) from dots/dashes into letters============================================================
    if (OFFtimerStarted != 0):
        offList.append(OFFtimer)#add one last recorded Off time (since we can't go back the other
    #loop to record it once its completed)
        numButtonReleases=numButtonReleases+1

    #We now have TWO arrays (lists): onList and offList

    count=0
    dd1=''#this is where our dots and dashes are stored-- it is illegal to have more than 5 in an english morse code char
    dd2=''
    dd3=''
    dd4=''
    dd5=''
    dd6=''
    ddCombo=''

    #print("debug check for index fixing: ")
    if((len(offList)) != (len(onList))):
      if((len(offList)) > (len(onList))):
        del offList[0]
      if((len(onList)) > (len(offList))):
        del onList[0]


    #writeToFile("",userSays1,"Morse Code"):

    for q in range(0, len(offList)):

        #print("onList value",q," is ", onList[q])               
        #GPIO.output(lcdGlo[4], GPIO.HIGH) #turns LED on
        #time.sleep(onList[q])

        
        os.system('echo '+str(offList[q])+' >> bleepBloopTimes')
        os.system('echo '+str(onList[q])+' >> bleepBloopTimes')
                    
        
        count=count+1

            

        if(onList[q]>=(3*lcdGlo[2])):#this means you've got a dash
            if (dd1 != '.' and dd1 != '-'):
                dd1='-'
            elif (dd2 != '.' and dd2 != '-'):
                dd2='-'
            elif (dd3 != '.' and dd3 != '-'):
                dd3='-'        
            elif (dd4 != '.' and dd4 != '-'):
                dd4='-'        
            elif (dd5 != '.' and dd5 != '-'):
                dd5='-'
            elif (dd6 != '.' and dd6 != '-'):
                dd6='-'         
        else:
            if (dd1 != '.' and dd1 != '-'):
                dd1='.'
            elif (dd2 != '.' and dd2 != '-'):
                dd2='.'
            elif (dd3 != '.' and dd3 != '-'):
                dd3='.'        
            elif (dd4 != '.' and dd4 != '-'):
                dd4='.'        
            elif (dd5 != '.' and dd5 != '-'):
                dd5='.'
            elif (dd6 != '.' and dd6 != '-'):
                dd6='.'         


        ddCombo=dd1+dd2+dd3+dd4+dd5+dd6
        print (ddCombo+' is our letter so far in dashes and dots')


        #print("offList value",q," is ", offList[q])
        #GPIO.output(lcdGlo[4], GPIO.LOW)#turns LED off
        #time.sleep(offList[q])

        if (count>6):
            someText = ddCombo+ ' is not a valid character in morse code.'
            dd1=''
            d=''
            dd3=''
            dd4=''
            dd5=''
            dd6=''
            ddCombo=''
            count=0
        if (offList[q]>=(3*lcdGlo[2])):
            convertedLetter=run_new_letter_funcs(ddCombo, convertedLetter)
            convertedWord=add_letter_to_word(convertedLetter,convertedWord)
            dd1=''
            dd2=''
            dd3=''
            dd4=''
            dd5=''
            dd6=''
            ddCombo=''
            count=0
            if (offList[q]>=(7*lcdGlo[2])):
                    convertedMessage=add_word_to_message(convertedWord,convertedMessage)
                    convertedWord=''
                    if (offList[q]>=(14*lcdGlo[2])):
                            convertedMessage=end_message(convertedMessage)
                            convertedWord=''
                            convertedMessage=convertedMessage[9:]
                            convertedMessage=convertedMessage[:-11]
                            
                            if(specFilter != ""):
                                convertedMessage= specifictionary(specFilter, convertedMessage)
                            return convertedMessage



lcdGlo[0]=2
numCharLcdSet=lcdGlo[1]




def playModernJazz(genre,subgenre):

    subgenre=str(subgenre).lower()
    subgenre1=subgenre[0].upper()
    subgenre1=(subgenre1+subgenre[1:])
    subgenre=subgenre1
    print('Our current subgenre is: ', subgenre)
    playerReplySub=input("Check subgenre to see if correct")#human player selection process: 
    

    genre=str(genre).lower()
    genre1=genre[0].upper()
    genre1=(genre1+genre[1:])
    genre=genre1
    print('Our current genre is: ', genre)
    playerReplySub=input("Check genre to see if correct")#human player selection process: 
    

    
    #omxplayer -o local /home/pi/Desktop/blueprintForFinalProjReconstruction/finalProjMusic/Jazz/modernJazz/electric-tric_-_Sketch_26.mp3
    lcd_string("modern jazz               ", LCD_LINE_1)
    lcd_string("is available      ", LCD_LINE_2)

    stuffToDisplay="Please choose from the following list of songs: "
    #lcdSays(stuffToDisplay)

    fileContent=""
    listOfSongsFile="songsList"

    os.system('ls /home/pi/Desktop/finalProject/music/Electronic/Chillout/*.mp3 > /home/pi/Desktop/finalProject/music/Electronic/Chillout/'+str(listOfSongsFile))
    fileContent=readFromFile('/home/pi/Desktop/finalProject/music/Electronic/Chillout/'+listOfSongsFile)
    lcdSays(fileContent)

    debugCount=2


    allSongsArray=['']
    allSongsArray=readFromFileArr('/home/pi/Desktop/finalProject/music/Electronic/Chillout/songsList')

    i=1
    numSongs=0
    numSongs=len(allSongsArray)
    fakeRandom=999
    fakeRandom=random.randint(1,(numSongs-1))


    randomSong=''
    cutSongArr=['']
    
    while(i<numSongs):
        cutSong1=''
        cutSong1=allSongsArray[i]

        startArr=0
        startArr=cutSong1.find('/home/pi/Desktop/finalProject/music/Electronic/Chillout/')+len('/home/pi/Desktop/finalProject/music/Electronic/Chillout/')
        cutSong2=''
        cutSong2=cutSong1[startArr:]
        cutSong3=''
        cutSong3=cutSong2[:-5]
        cutSongArr.append(cutSong3)
        print(str(i)+') ')
        #print(cutSong3)
        #if(randSongNum1==i):
          #randomSong=cutSong3
        print(cutSongArr[i])
        #fakeRandom=7
        if(i==fakeRandom):
            randomSong=cutSong3
        i=i+1

    fakeRandom=7
    print('fakeRandom song is '+str(cutSongArr[fakeRandom]))

    #randomSong = cutSongArr[random.randint(1,(len(allSongsArray)-1))]

    menuSays="Choose from the song list above by entering the number of the song on the list: "
    morseReply="@@@@@"
    try:
        lcdSays(menuSays)
    except:
        print(menuSays)
        morseReply=""
        morseReply=morseCode(morseReply,"")
    if(morseReply=="@@@@@"):
        playerReply=input("Choose from song list above using keyboard")#human player selection process:    
        morseReply=playerReply
    #try:
    songpath=cutSongArr[int(playerReply)]
    menuSays=("You chose: "+str(songpath))
    lcdSays(menuSays)
    #except:
    if (len(playerReply) > 3):
        songpath=cutSongArr[fakeRandom]
        menuSays=("No valid song choice selected... choosing a random song instead... Now Playing: "+str(songpath))        
        lcdSays(menuSays)
            


    songpath='/home/pi/Desktop/finalProject/music/'+genre+'/'+subgenre+'/'+randomSong+'.mp3'

    omxprocess = subprocess.Popen(['omxplayer', '-o', 'local', songpath], stdin=subprocess.PIPE, stdout=None, stderr=None, bufsize=0)

    time.sleep(5)
    
    print('NOspacing'+songpath+'NOspacing')    
    print("debug count is",debugCount)

    time.sleep(.25)
    lcdSays("button push to end song coming up")

    fileContent=("/home/pi/Desktop/finalProject/music/"+genre+"/"+subgenre+"/currentKeyCommands")
    lcdSays(fileContent)

    morseReply=""
    morseReply=morseCode(morseReply,"")
    playerReply=morseReply




    playerReplyU=playerReply.upper()
    defaultSongTimer=200
    while(playerReplyU.count("Q")<=1 and defaultSongTimer >=0):
      if(inputMode == "Keyboard"):
        playerReply=input("Choose from options using keyboard")#human player selection process:        
      if((0 != GPIO.input(ButtonPin))):
        morseReply=morseCode(morseReply,"")
        playerReply=morseReply
        print("You entered: ",morseReply)
      playerReplyU=playerReply.upper()
      
      if (playerReplyU.count("Q")>=1):
        lcdSays("QUITTING")
        omxprocess.stdin.write(b'q')
        defaultSongTimer=0
      if (playerReplyU.count("P")>=1):
        lcdSays("PAUSE PLAY")
        omxprocess.stdin.write(b'p')
      elif (playerReplyU.count("D")>=1):
        lcdSays("TURN VOLUME DOWN")
        omxprocess.stdin.write(b'-')
      elif (playerReplyU.count("U")>=1):
        lcdSays("TURN VOLUME UP")
        omxprocess.stdin.write(b'+')
      elif (playerReplyU.count("S")>=1):
        lcdSays("SLOW DOWN")
        omxprocess.stdin.write(b'1')
      elif (playerReplyU.count("I")>=1):
        lcdSays("INCREASE SPEED")
        omxprocess.stdin.write(b'2')
     
      defaultSongTimer=defaultSongTimer-10
      print(defaultSongTimer)



      
    time.sleep(11)

    mp3Names=[]

    time.sleep(1)
    lcd_string("Now Playing:               ", LCD_LINE_1)
    lcd_string("Lobo_Loco_-_14_-_Sofa_Fittness_ID_950.mp3          ", LCD_LINE_2)    
    os.system('omxplayer -o local '+str(songpath))

      
    time.sleep(5)
    lcd_string("Next up:               ", LCD_LINE_1)
    lcd_string("Sketch 26           ", LCD_LINE_2) 
    time.sleep(5)
    lcd_string("Now Playing:               ", LCD_LINE_1)
    lcd_string("Sketch 26           ", LCD_LINE_2)    
    os.system('omxplayer -o local /home/pi/Desktop/finalProject/music/Electronic/Chillout/electric-tric_-_Sketch_26.mp3')






 

inputMode=""


playerReply=""

morseReply=""


#MENU FROM END PLUGGED IN HERE %%%%%%% MENU FROM END PLUGGED IN HERE %%%%%%% MENU FROM END PLUGGED IN HERE %%%%%%% MENU FROM END PLUGGED IN HERE %%%%%%%%%%%%%%%%%%
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv


#playModernJazz('ElecTroNic','CHILLOUT')

#welcomeMessage="Welcome to the Raspberry Pi alternate emergency user input system.  This interactive interface allows the computer and the user to communicate with one another in a variety of different manners to best suit the needs or constraints of a given situation.  The raspberry pi while this program is running is now capable of communicating via text through an LCD screen or through LED blinks and button pushes as Morse Code in addition to conventional user input methods."
lcd_init()




#lcdSays(welcomeMessage)
menuOptionPicked="99"

playerReplyU="no quitting yet"

while (playerReplyU.count("8")< 1):

  menuSays="Choose from options using Morse Code: "
  lcdSays(menuSays)
  menuSays="Choose from the Following Menu Options : Option 1- Write to file   Option 2- read from file   Option 3- Perform online search   Option 4- check email   Option 5- send email   Option 6- execute terminal commands   Option 7- play music   Option 8- quit"
  lcdSays(menuSays)

  morseReply=""
  morseReply=morseCode(morseReply,"")
  playerReply=morseReply
  menuSays=("You entered: "+str(morseReply))
  lcdSays(menuSays)    

  if(morseReply=="@@@@@"):
    playerReply=input("Choose from 5 options using keyboard")#human player selection process:
    inputMode="Keyboard"
  else:
    inputMode="Morse Code"

  #########  MENU OPTIONS ##################################

  playerReplyU=playerReply.upper()
  
  # create write to file
  if (playerReplyU.count("1")>=1):
      fileNameIn=input("Enter file name:")    
      writeToFile(fileNameIn,"",inputMode)
      #menuSays=("Write to file is available at this time. ")
      #lcdSays(menuSays)
    

      #read from file
  elif (playerReplyU.count("2")>=1):
     # menuSays=("read from file is available at this time. ")
      #lcdSays(menuSays)
      createdFileName=input("Enter file name: ")
      fileContent=readFromFile("/home/pi/Desktop/finalProject/"+str(createdFileName))
      lcdSays(fileContent)

      #online search
  elif (playerReplyU.count("3")>=1):
      #menuSays=("online search is available at this time. ")
     #lcdSays(menuSays)
      fileContent=input("Enter stuff to search online:")    
      stuffFromWebsite=""
      stuffFromWebsite=quickGrabAll(("https://duckduckgo.com/?q="+str(fileContent)+"&t=h_&ia=web"),stuffFromWebsite)
      lcdSays(stuffFromWebsite)
      stuffFromWebsite=quickGrabAll(("https://en.wikipedia.org/wiki/"+str(fileContent)),stuffFromWebsite)
      lcdSays(stuffFromWebsite)

      #checking email
  elif (playerReplyU.count("4")>=1):
      menuSays=("checking email... ")
      lcdSays(menuSays)
      checkEmail()


      #sending emails
  elif (playerReplyU.count("5")>=1):
      menuSays=("sending email... ")
      lcdSays(menuSays)
      
      morseReply=morseCode(morseReply,"")
      playerReply=morseReply
      menuSays=("You entered: "+str(morseReply))
      lcdSays(menuSays)    
      if(morseReply=="@@@@@"):
        playerReply=input("Enter email message: ")#human player selection process:
        inputMode="Keyboard"
      
      email_sending('##########@gmail.com',''+str(playerReply))


      

      #terminal commands
  elif (playerReplyU.count("6")>=1):
      #menuSays=("terminal commands are available at this time. ")
      #lcdSays(menuSays)
      createdFile="stuff"

      morseReply=""
      morseReply=morseCode(morseReply,"")
      playerReply=morseReply
      print("You entered: ",morseReply)
      
      playerReplyU=playerReply.upper()
      if (playerReplyU.count("LS")>=1):
          os.system('ls -l /home/pi/Desktop/finalProject > /home/pi/Desktop/finalProject/'+str(createdFileName))
          fileContent=readFromFile("/home/pi/Desktop/finalProject/"+str(createdFileName))
          print(fileContent)

          
  # play music
  elif (playerReplyU.count("7")>=1):
      #menuSays=("music is available at this time. ")
      #lcdSays(menuSays)
      createdFile="stuff"
      createdFileName="subgenreList"
      menuSays="Choose a subgenre from the following list of choices: "
      lcdSays(menuSays)
      currentGenre='Electronic'
      os.system('ls /home/pi/Desktop/finalProject/music/'+str(currentGenre)+' > /home/pi/Desktop/finalProject/'+str(createdFileName))
      menuSays=readFromFile("/home/pi/Desktop/finalProject/"+str(createdFileName))
      lcdSays(menuSays)
      
      morseReply=""
      morseReply=morseCode(morseReply,"")
      playerReply=morseReply
      menuSays=("You entered: "+str(morseReply))
      lcdSays(menuSays)    

      if(morseReply=="@@@@@"):
        playerReply=input("No Morse Code detected.  Instead, choose from the options given using a keyboard")#human player selection process:
        inputMode="Keyboard"
      else:
        menuOptionPicked="4"
      currentSubgenre=''
      currentSubgenre=(''+str(playerReply))
      playModernJazz(currentGenre,currentSubgenre)


  # create write to file
  if (playerReplyU.count("8")>=1):
      menuSays=("Quitting Morse Code program...")
      lcdSays(menuSays)
    

      

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#MENU FROM END PLUGGED IN HERE %%%%%%% MENU FROM END PLUGGED IN HERE %%%%%%% MENU FROM END PLUGGED IN HERE %%%%%%% MENU FROM END PLUGGED IN HERE %%%%%%%%%%%%%%%%%%




