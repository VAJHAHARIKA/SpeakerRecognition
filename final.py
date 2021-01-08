from tkinter import *
from gtts import gTTS 
import random
import pandas as pd
import numpy as np
from audio import read_mfcc
from batcher import sample_from_mfcc
from constants import SAMPLE_RATE, NUM_FRAMES
from conv_models import DeepSpeakerModel
from test import batch_cosine_similarity
import pyaudio
import wave
import os
import librosa
import sys
import numpy as np
import pickle
import sys
import pyttsx3
from termcolor import colored
import speech_recognition as sr 
import datetime
import time 
from datetime import timedelta
import csv
from tempfile import NamedTemporaryFile
import shutil
from csv import writer 
from csv import DictWriter 
from datetime import date

# create tkinter window 
root = Tk() 

# styling the frame which helps to 
# make our background stylish 
frame1 = Frame(root, 
			bg = "#1f0036", 
			height = "150") 

# plcae the widget in gui window 
frame1.pack(fill = X) 


frame2 = Frame(root, 
			bg = "#1f0036", 
			height = "750") 
frame2.pack(fill=X) 



# styling the label which show the text 
# in our tkinter window 
label = Label(frame1, text = "eWarn System", 
			font = "bold, 30", 
			bg = "#f9f7cb") 

label.place(x = 180, y = 70) 



# entry is used to enter the text 
entry = Entry(frame2, width = 45, 
			bd = 4, font = 14) 

entry.place(x = 130, y = 52) 
entry.insert(0, "") 

# define a function which can 
engine = pyttsx3.init()
# get text and convert into audio 

def play():

    text = None
    out_file =r"D:/Projects/Internship/samtest/file_out.wav"
    rootdir = os.path.join(os.getcwd(), 'samples') 
    attendance_file_path = os.path.join(os.getcwd(), 'Attendance_data\out.csv')
    
    def print_data(info):
    	with open(r'\Attendance_data\out.csv', 'rb') as handle:
    		unserialized_data = csv.reader(handle)
    		print(info, unserialized_data)
    
    # if data doesn't exist
    if not os.path.exists(attendance_file_path) and not os.path.isfile(attendance_file_path):
    	if not os.path.exists('Attendance_data'):
    		os.makedirs('Attendance_data')
    		d = {'Date': [], 'EmpName': [], 'EmpID':[], 'In':[], 'Out':[], 'Duration':[], 'Attendance':[]}
    		df = pd.DataFrame(data=d)
    		print('\nCreating New Attendance DataFrame : ')
    		print(df)
    		df.to_csv(r'Attendance_data\out.csv', index=False)
    	#print_data('Data is created : \n')
    
    
    # compression_opts = dict(method='zip',
    #                         archive_name='out.csv')  
    # df.to_csv('out.zip', index=False,           
    #           compression=compression_opts)  
    
    names = []
    
    for subdir, dirs, files in os.walk(rootdir):
        for dir_name in dirs:
        	names.append(dir_name)
    
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        
    
    def pyttsx3(text):
    	# obtain voice property
    	voices = engine.getProperty('voices')
    	# voice id 1 is for female and 0 for male
    	engine.setProperty('voice', voices[1].id)
    	# convert to audio and play
    	engine.say(text)
    	engine.runAndWait()
    print(bcolors.OKGREEN+"\n\nWelcome to Attendance System based on Speaker Recognition.\n\nRules are simple, say your name and roll num and the attendance will be updated.\n")
    pyttsx3("Welcome to Attendance System based on Speaker Recognition. Rules are simple, say your name and roll num and the attendance will be updated. Warning: Don't try to give proxy")
    print(bcolors.WARNING + "Warning: Don't try to give proxy" + bcolors.ENDC+"\n")
    audio = pyaudio.PyAudio()
     
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 12
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    r=sr.Recognizer()
    print("Speak something...\n")
    pyttsx3("The recording has started, please say Hello ewarn,along with your name and employee ID and if you are signing in or out")
    
    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    pyttsx3("The recording has completed, and now your information will be updated, please be patient and if you feel there is an error kindly contact the adminstrator")
    print("Recording saved\n")
    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(out_file, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    
    with sr.AudioFile(out_file) as source:
        #print("Say something!")
        audio = r.record(source)  # read the entire audio file
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        #print("Did you say? " + r.recognize_google(audio))
        text=r.recognize_google(audio)
    except sr.UnknownValueError:
        print("eWarn could not understand audio")
    
    if  "hello" not in text:
        print("Trigger word missing, Please try again")
        pyttsx3("Trigger word missing, Please try again")
        exit(0)
    
    # Reproducible results.
    np.random.seed(123)
    random.seed(123)
    
    # Define the model here.
    model = DeepSpeakerModel()
    
    # Load the checkpoint.
    model.m.load_weights('Model.h5', by_name=True)
    
    mfcc_005 = sample_from_mfcc(read_mfcc(out_file, SAMPLE_RATE), NUM_FRAMES)
    
    # Call the model to get the embeddings of shape (1, 512) for each file.
    predict_005 = model.m.predict(np.expand_dims(mfcc_005, axis=0))
    
    #names = []
    select = dict()
    
    from statistics import mean
    
    for subdir, dirs, files in os.walk(rootdir):
        for dir_name in dirs:
        	#names.append(dir_name)
        	#print('person dir : ', dir_name)
        	#print('person dir files : \n', os.listdir(os.path.join(rootdir, dir_name)))
        	select_list = list()
        	for file_name in os.listdir(os.path.join(rootdir, dir_name)):
        		#print(file_name)
        		#print('person dir files seperate : \n', os.path.join(rootdir, dir_name, file_name))
        		mfcc_001 = sample_from_mfcc(read_mfcc(os.path.join(rootdir, dir_name, file_name) , SAMPLE_RATE), NUM_FRAMES)
        		predict_001 = model.m.predict(np.expand_dims(mfcc_001, axis=0))
    
        		select_list.append(batch_cosine_similarity(predict_005,predict_001)[0])
        	
        	#print(select_list)
        	select[dir_name] = mean(select_list)
        	select_list.clear()
    
    
    #print('Names : ', names)
    print('\nPredcitions :', select)
    Keymax = max(select, key=select.get) 

    if (select[Keymax])>=0.5:
        print('The Speaker is: ', Keymax.split('+')[0])
        pyttsx3('The Speaker is '+ str(Keymax.split('+')[0]))
        time_in= None
        time_out= None
        
        #'EmpName': [], 'EmpID':[], 'In':[], 'Out':[], 'Duration':[], 'Attendance':[]}
        if text.lower().split().count('in') == 1:
            #print('text has in', text)
            time_in= datetime.datetime.now() 
            print("Current time for in:-", time_in) 
        
            df_in = pd.read_csv(attendance_file_path, parse_dates=['Date'])
            temp_in = {'Date': datetime.datetime.date(time_in), 'EmpName': Keymax.split('+')[0], 'EmpID': Keymax.split('+')[1], \
        		'In': time_in, 'Out': 'zero', 'Duration': 'zero', 'Attendance': 'zero'}
            temp_df = pd.DataFrame(temp_in, index=[0])
            #print("temp_in", temp_in)
            #print("temp_df", temp_df)
            if not df_in.empty:
                print('DataFrame is not empty!')
                #df_in.append(temp_df, ignore_index = True)
                print('\n\nIN Before Update\n', df_in)
                df3 = pd.concat([df_in, temp_df], ignore_index = True) 
                df3.reset_index() 
                df3.to_csv(r'Attendance_data\out.csv', index=False)
                print('\n\ndf3\n', df3.tail(5))
            if df_in.empty:
                print('DataFrame is empty!')
                #df_new = pd.DataFrame(temp_in)
                temp_df.to_csv(r'Attendance_data\out.csv', index=False)
                print('After IN Update', temp_df)	
                exit(0)
        
        if text.lower().split().count('out') == 1:
            #print('Text has out')
            df_out = pd.read_csv(attendance_file_path, parse_dates=['Date'])
            #print(df_out)
            time_out= datetime.datetime.now()
            print("Current time for out:-", time_out) 
            in1 = df_out['In'].loc[ (df_out['Date'] == pd.to_datetime(datetime.datetime.date(datetime.datetime.now()))) & (df_out['EmpName'] == Keymax.split('+')[0]) & (df_out['EmpID'] == int(Keymax.split('+')[1]))]
            #print(in1)
            df_out['Out'].loc[ (df_out['Date'] == pd.to_datetime(datetime.datetime.date(datetime.datetime.now()))) & (df_out['EmpName'] == Keymax.split('+')[0]) & (df_out['EmpID'] == int(Keymax.split('+')[1]))] = time_out
            out1 = df_out['Out'].loc[ (df_out['Date'] == pd.to_datetime(datetime.datetime.date(datetime.datetime.now()))) & (df_out['EmpName'] == Keymax.split('+')[0]) & (df_out['EmpID'] == int(Keymax.split('+')[1]))]
            #print(out1)
            delta = pd.to_datetime(out1)-pd.to_datetime(in1)
            #print(delta)
            df_out['Duration'].loc[ (df_out['Date'] == pd.to_datetime(datetime.datetime.date(datetime.datetime.now()))) & (df_out['EmpName'] == Keymax.split('+')[0]) & (df_out['EmpID'] == int(Keymax.split('+')[1]))] = delta
            day1 = df_out['Attendance'].loc[ (df_out['Date'] == pd.to_datetime(datetime.datetime.date(datetime.datetime.now() - datetime.timedelta(days=1))  ) ) & (df_out['EmpName'] == Keymax.split('+')[0]) & (df_out['EmpID'] == int(Keymax.split('+')[1]))]
            #print(day1.empty)
            if day1.empty: 
                df_out['Attendance'].loc[ (df_out['Date'] == pd.to_datetime(datetime.datetime.date(datetime.datetime.now()))) & (df_out['EmpName'] == Keymax.split('+')[0]) & (df_out['EmpID'] == int(Keymax.split('+')[1]))] = 1
            else:
                df_out['Attendance'].loc[ (df_out['Date'] == pd.to_datetime(datetime.datetime.date(datetime.datetime.now()))) & (df_out['EmpName'] == Keymax.split('+')[0]) & (df_out['EmpID'] == int(Keymax.split('+')[1]))] = int(day1[0]) + 1
            
            df_out.to_csv(r'Attendance_data\out.csv', index=False)
            print(df_out.tail(5))
            exit(0)
    else:
         print("Don't try to give proxy")
         pyttsx3("Don't try to give proxy")
         exit(0)
    
btn = Button(frame2, text = "SUBMIT", 
			width = "15", pady = 10, 
			font = "bold, 15", 
			command = play, bg='#f9f7cb') 


# the label's textvariable is set to the variable class instance

btn.place(x = 250, 
		y = 130) 
# give a title 
root.title("eWarn Attendance System") 



# we can not change the size 
# if you want you can change 
root.geometry("650x550+350+200") 

# start the gui 
root.mainloop()

