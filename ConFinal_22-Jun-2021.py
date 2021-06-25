#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created by the PanLab in March 2018
by Brooke Staveland and Carlos Correa
Original task design by Leanne Williams and the Brain Resource Center
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008

"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import locale_setup, visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
from psychopy.visual import window
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys # to get file system encoding
from glob import glob
from get_usb import get_usb

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Faces Conscious'  # from the Builder filename that created this script
expInfo = {u'session': u'', u'participant': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_s%s_%s_%s' %(expInfo['participant'], expInfo['session'], expName, expInfo['date'])

#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation
## Create window based on the site config .yaml file
import pyglet
display = pyglet.window.get_platform().get_default_display()
screens = display.get_screens()
resolution = [screens[-1].width, screens[-1].height]
import yaml
from psychopy import monitors
if not os.path.exists('siteConfig.yaml'): raise IOError('Missing siteConfig.yaml - Please copy configuration text file')
with open('siteConfig.yaml') as f:
    config = yaml.safe_load(f)
mon = monitors.Monitor('newMonitor')
mon.setWidth(config['monitor']['width'])
mon.setDistance(config['monitor']['distance'])
mon.setSizePix(resolution)

# Setup the Window
win = visual.Window(size=resolution, fullscr=False, screen=config['monitor']['screen'], allowGUI=False, allowStencil=False,
    monitor=mon, color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='deg')

# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
    logging.exp('frame duration: {}'.format(frameDur))
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess
    logging.exp('frame duration was guessed: {}'.format(frameDur))
    logging.flush()
    raise IOError('Frame duration could not be reliably measured! Please close the other windows on the computer and try again!')
    raise IOError('Could not get a Stable Frame Rate')
if frameDur >= 0.020:
    logging.exp('Frame Rate Too Slow for Subliminal Stimuli!: {}'.format(frameDur))
    logging.flush()
    raise IOError('Frame Rate Too Slow for Subliminal Stimuli! Please close the other windows on the computer and try again!')

# Record Git Status in Subject Logs
from subprocess import check_output, check_call, CalledProcessError
try:
    revision = check_output(['git','rev-parse', '--short', 'HEAD'])
    revision = revision.strip()
    gitInstalled = True
except:
    if os.path.exists('VERSION'):
        with open('VERSION', 'r') as f:
            revision = f.read().strip()
    else:
        revision = ''
    gitInstalled = False

if gitInstalled:
    try:
        check_call(['git', 'diff', '--quiet', 'conFinal.py'])
    except CalledProcessError:
        revision = 'Task changes detected. Nearest head: %s' % revision
        status_msg = check_output(['git', 'diff', 'conFinal.py'])
        msg ="""%s
        Warning: the experiment has unexpected changes.
        """ % status_msg
        logging.exp(msg)
        logging.flush()
        raise IOError('This script has unexpected changes! Please get correct version from Github Repo')

expInfo['git-revision'] = revision
logging.exp('git-revision: %s' % revision)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
logging.exp('Task Started at: {}'.format(core.getAbsTime())) #Log the task start time
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine


#Font height
smallText = .75
medText = 2
largeText = 5

### Initialize components for Routine "Instructions" ###
instrClock = core.Clock()
instrText = visual.TextStim(win=win, ori=0, name='instrText',
    text="In this task, you will be doing the same thing as the previous task, but while viewing a new set of faces.  \n\nYou don't need to do anything but lay still and relax, but please pay attention because we may be asking you some questions about them later. ",    font='Arial',
    pos=[0, 0], height=smallText, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

### Initialize components for Routine "Get Ready" ###
readyClock = core.Clock()
instrText_2 = visual.TextStim(win=win, ori=0, name='instrText',
    text="Get Ready!",    font='Arial', units='deg',
    pos=[0, 0], height=medText, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

#################################################
### import modules
import serial
import time

### scanner trigger
### Set SCANNER_TRIGGER_NEEDED to False to bypass program abortion when scanner exception is thrown
SCANNER_TRIGGER_NEEDED = False
DEVICE_ID = get_usb()

### scanner trigger
def cni_trigger():
    try:
        ser = serial.Serial(DEVICE_ID, 57600, timeout=1)
        time.sleep(.5)    ### wait for 2 sec to ensure scanner is ready; CNI wiki default 0.1
        logging.exp('Trigger Sent: {}'.format(globalClock.getTime()))
        ser.write('[t][t][t]\n')
        logging.exp('Trigger Connection Closed: {}'.format(globalClock.getTime()))
        ser.close()
        #print("hi")
    except Exception as err:
        print(str(err))
        if not SCANNER_TRIGGER_NEEDED:
            pass
        else:
            core.quit()

### Initialize components for Routine "Countdown" ###

CountDownClock = core.Clock()
text3 = visual.TextStim(win=win, ori=0, name='text3',
    text=u'3',    font=u'Arial',  units = 'deg',
    pos=[0, 0], height=largeText, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-2.0)
text2 = visual.TextStim(win=win, ori=0, name='text2',
    text=u'2',    font=u'Arial',  units = 'deg',
    pos=[0, 0], height=largeText, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-3.0)
text1 = visual.TextStim(win=win, ori=0, name='text1',
    text=u'1',    font=u'Arial',  units = 'deg',
    pos=[0, 0], height=largeText, wrapWidth=None,
    color=u'white', colorSpace='rgb', opacity=1,
    depth=-4.0)

### Initialize components for Main Loop ###

# Initialize Loop Clocks
blankClock = core.Clock()
emotionClock = core.Clock()

## Initialize components for Routine "emotion" ##

# set up handler to look after randomisation of conditions etc
# We move this up here to avoid any timing impact from loading conditions from disk.
trials = data.TrialHandler(nReps=1, method='sequential',
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions('../panlab_stimuli/EmotionConscious-task/stimulus_order.csv'),
    seed=None, name='trials')

# We preload all images to avoid performance issues during display.
# We load the images into two different caches to avoid any issues with the `name` kwarg for the ImageStim.
emotion_image_cache = {}
for image_path in glob(os.path.join(_thisDir, '../panlab_stimuli/EmotionConscious-task/images/*.png')):
    short_name = os.path.join('images', os.path.basename(image_path))
    emotion_image_cache[short_name] = visual.ImageStim(
        win=win, name='emotion_image',
        image=image_path, mask=None, #FLAG why not 'sin'
        ori=0, pos=[0, 0], size=None,
        color=[1, 1, 1], colorSpace='rgb', opacity=1,
        flipHoriz=False, flipVert=False,
        texRes=128, interpolate=True, depth=0.0)

# Now that images and other things are loaded, we record frames.
win.recordFrameIntervals = True
win.refreshThreshold = frameDur + 0.004
# HACK we increase the number of dropped frames that need to be reported
# to more easily monitor rendering issues.
window.reportNDroppedFrames = 300

## Initialize components for Routine "blank" ##
space = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='space')

### Initialize components for Routine "Question Prep"" ###
qpClock = core.Clock()
instrText_3point5 = visual.TextStim(win=win, ori=0, name='instrText',
    text="Good Job!",    font='Arial', units='deg',
    pos=[0, 3], height=medText, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
instrText_3 = visual.TextStim(win=win, ori=0, name='instrText',
    text="Now for a quick question about the faces you saw.",    font='Arial', units='deg',
    pos=[0, -2], height=1, wrapWidth=40,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

### Initialize components for Routine "question"" ###
questClock = core.Clock()
'''
### commenting this out to get rid of the images of the button box###
image1 = visual.ImageStim(win=win, name='image',
    image=os.path.join(_thisDir, '../panlab_stimuli/GoNoGo-task/Slide1.png'), mask=None,
    ori=0, pos=[-12,-3], size=[3, 4],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)
image2 = visual.ImageStim(win=win, name='image',
    image=os.path.join(_thisDir, '../panlab_stimuli/GoNoGo-task/Slide2.png'), mask=None,
    ori=0, pos=[12, -3], size=[3, 4],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
image3 = visual.ImageStim(win=win, name='image',
    image=os.path.join(_thisDir, '../panlab_stimuli/GoNoGo-task/Slide2.png'), mask=None,
    ori=0, pos=[-1.5, -3], size=[3, 4],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
image4 = visual.ImageStim(win=win, name='image',
    image=os.path.join(_thisDir, '../panlab_stimuli/GoNoGo-task/Slide2.png'), mask=None,
    ori=0, pos=[1.5, -3], size=[3, 4],
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-4.0)
'''
instrText_4 = visual.TextStim(win=win, ori=0, name='instrText',
    text="Which of the following statements is TRUE concerning the faces you just saw?",    font='Arial', units='deg',
    pos=[0, 5], height=1, wrapWidth=40,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

# Set Up for Different questions for sessions
if int(expInfo['session']) ==1:
    ansText_1 = visual.TextStim(win=win, ori=0, name='instrText',
        text="There were more female\n\n faces than male faces.\n\n\n\n Press the thumb button.",    font='Arial', units='deg',
        pos=[-12, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
    ansText_2 = visual.TextStim(win=win, ori=0, name='instrText',
        text="The number of female faces was\n\nequal to the number of male faces.\n\n\n\n Press the index finger button.", font='Arial', units='deg',
        pos=[0, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
    ansText_3 = visual.TextStim(win=win, ori=0, name='instrText',
        text=" There were more male\n\n faces than female faces.\n\n\n\n Press the middle finger button.",    font='Arial', units='deg',
        pos=[12, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
elif int(expInfo['session']) ==2:
    ansText_1 = visual.TextStim(win=win, ori=0, name='instrText',
        text="There were more angry\n\n faces than sad faces.\n\n\n\n Press the thumb button.",    font='Arial', units='deg',
        pos=[-12, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
    ansText_2 = visual.TextStim(win=win, ori=0, name='instrText',
        text="The number of angry faces was\n\nequal to the number of sad faces.\n\n\n\n Press the index finger button.", font='Arial', units='deg',
        pos=[0, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
    ansText_3 = visual.TextStim(win=win, ori=0, name='instrText',
        text="There were more sad\n\n faces than angry faces.\n\n\n\n Press the middle finger button.",    font='Arial', units='deg',
        pos=[12, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
elif int(expInfo['session']) ==3:
    ansText_1 = visual.TextStim(win=win, ori=0, name='instrText',
        text="There were more neutral\n\n faces than happy faces.\n\n Press the thumb button.",    font='Arial', units='deg',
        pos=[-12, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
    ansText_2 = visual.TextStim(win=win, ori=0, name='instrText',
        text="The number of neutral faces was\n\nequal to the number of happy faces.\n\n\n\n Press the index finger button.", font='Arial', units='deg',
        pos=[0, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
    ansText_3 = visual.TextStim(win=win, ori=0, name='instrText',
        text="There were more happy\n\n faces than neutral faces.\n\n\n\n Press the middle finger button.",    font='Arial', units='deg',
        pos=[12, 1], height=smallText, wrapWidth=20,
        color='white', colorSpace='rgb', opacity=1,
        depth=-1.0)
'''
### commenting this out because above has been updated with our new instructions to use the 1-5 button box###
respText_1 = visual.TextStim(win=win, ori=0, name='instrText',
    text="Left",    font='Arial', units='deg',
    pos=[-12, -6], height=smallText, wrapWidth=20,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
respText_2 = visual.TextStim(win=win, ori=0, name='instrText',
    text="Both",    font='Arial', units='deg',
    pos=[0, -6], height=smallText, wrapWidth=20,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
respText_3 = visual.TextStim(win=win, ori=0, name='instrText',
    text="Right",    font='Arial', units='deg',
    pos=[12, -6], height=smallText, wrapWidth=20,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
'''

### Initialize components for Routine "Well Done"" ###
doneClock = core.Clock()
instrText_5 = visual.TextStim(win=win, ori=0, name='instrText',
    text="Well Done!",    font='Arial', units='deg',
    pos=[0, 0], height=medText, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)

### Start Task ###


#------Prepare to start Routine "Instructions"-------
t = 0
instrClock.reset()  # clock
frameN = -1
# update component parameters for each repeat
instrKey = event.BuilderKeyResponse()  # create an object of type KeyResponse
instrKey.status = NOT_STARTED

# keep track of which components have finished
instrComponents = []
instrComponents.append(instrText)
instrComponents.append(instrKey)
for thisComponent in instrComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Instructions"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = instrClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *instrText* updates
    if t >= 0.0 and instrText.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText.tStart = t  # underestimates by a little under one frame
        instrText.frameNStart = frameN  # exact frame index
        instrText.setAutoDraw(True)

    # *instrKey* updates
    if t >= 0.0 and instrKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrKey.tStart = t  # underestimates by a little under one frame
        instrKey.frameNStart = frameN  # exact frame index
        instrKey.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(instrKey.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if instrKey.status == STARTED:
        theseKeys = event.getKeys(keyList=['s'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            instrKey.keys = theseKeys[-1]  # just the last key pressed
            instrKey.rt = instrKey.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in instrComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Instructions"-------
for thisComponent in instrComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

#------Prepare to start Routine "Get Ready"-------
t = 0
readyClock.reset()  # clock
frameN = -1
# update component parameters for each repeat
instrKey = event.BuilderKeyResponse()  # create an object of type KeyResponse
instrKey.status = NOT_STARTED

# keep track of which components have finished
readyComponents = []
readyComponents.append(instrText_2)
readyComponents.append(instrKey)
for thisComponent in readyComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Get Ready"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = readyClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *instrText_2* updates
    if t >= 0.0 and instrText_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText_2.tStart = t  # underestimates by a little under one frame
        instrText_2.frameNStart = frameN  # exact frame index
        instrText_2.setAutoDraw(True)

    # *instrKey* updates
    if t >= 0.0 and instrKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrKey.tStart = t  # underestimates by a little under one frame
        instrKey.frameNStart = frameN  # exact frame index
        instrKey.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(instrKey.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if instrKey.status == STARTED:
        theseKeys = event.getKeys(keyList=['s'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            instrKey.keys = theseKeys[-1]  # just the last key pressed
            instrKey.rt = instrKey.clock.getTime()
            cni_trigger()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in readyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Get Ready"-------
for thisComponent in readyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "Get Ready" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()


#------Prepare to start Routine "CountDown"-------
t = 0
CountDownClock.reset()  # clock
frameN = -1
routineTimer.add(8.000000)
# keep track of which components have finished
CountDownComponents = []
CountDownComponents.append(text3)
CountDownComponents.append(text2)
CountDownComponents.append(text1)
for thisComponent in CountDownComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "CountDown"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = CountDownClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

    # update/draw components on each frame
    if t >= 0.0 and space.status == NOT_STARTED:
        # keep track of start time/frame for later
        space.tStart = t  # underestimates by a little under one frame
        space.frameNStart = frameN  # exact frame index
        space.start(2)
    elif space.status == STARTED: #one frame should pass before updating params and completing
        space.complete() #finish the static period

    # *text3* updates
    if t >= 2 and text3.status == NOT_STARTED:
        # keep track of start time/frame for later
        text3.tStart = t  # underestimates by a little under one frame
        text3.frameNStart = frameN  # exact frame index
        text3.setAutoDraw(True)
    if text3.status == STARTED and t >= (2 + (2.0-win.monitorFramePeriod*0.75)): #most of one frame period left
        text3.setAutoDraw(False)

    # *text2* updates
    if t >= 4 and text2.status == NOT_STARTED:
        # keep track of start time/frame for later
        text2.tStart = t  # underestimates by a little under one frame
        text2.frameNStart = frameN  # exact frame index
        text2.setAutoDraw(True)
    if text2.status == STARTED and t >= (4 + (2.0-win.monitorFramePeriod*0.75)): #most of one frame period left
        text2.setAutoDraw(False)

    # *text1* updates
    if t >= 6 and text1.status == NOT_STARTED:
        # keep track of start time/frame for later
        text1.tStart = t  # underestimates by a little under one frame
        text1.frameNStart = frameN  # exact frame index
        text1.setAutoDraw(True)
    if text1.status == STARTED and t >= (6 + (2.0-win.monitorFramePeriod*0.75)): #most of one frame period left
        text1.setAutoDraw(False)

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in CountDownComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "CountDown"-------
for thisComponent in CountDownComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

### Start Main Loop ###

thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)


    #------Prepare to start Routine "emotion"-------
    t = 0
    emotionClock.reset()  # clock
    frameN = -1
    routineTimer.add(0.500000)
    # update component parameters for each repeat
    emotion_image = emotion_image_cache[emotion]
    # keep track of which components have finished
    emotionComponents = []
    emotionComponents.append(emotion_image)
    for thisComponent in emotionComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "emotion"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = emotionClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *emotion_image* updates
        if t >= 0.0 and emotion_image.status == NOT_STARTED:
            # keep track of start time/frame for later
            emotion_image.tStart = t  # underestimates by a little under one frame
            emotion_image.frameNStart = frameN  # exact frame index
            emotion_image.setAutoDraw(True)
        if emotion_image.status == STARTED and t >= (0.0 + (0.50-win.monitorFramePeriod*0.75)): #most of one frame period left
            emotion_image.setAutoDraw(False)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in emotionComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "emotion"-------
    for thisComponent in emotionComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    # Routine "emotion" was not slip safe, so reset timer
    routineTimer.reset()

    #------Prepare to start Routine "blank"-------
    t = 0
    blankClock.reset()  # clock
    frameN = -1
    routineTimer.add(0.750000)
    # update component parameters for each repeat
    # keep track of which components have finished
    blankComponents = []
    blankComponents.append(space)
    for thisComponent in blankComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    #-------Start Routine "blank"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = blankClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *space* period
        if t >= 0.0 and space.status == NOT_STARTED:
            # keep track of start time/frame for later
            space.tStart = t  # underestimates by a little under one frame
            space.frameNStart = frameN  # exact frame index
            space.start(0.75)
        elif space.status == STARTED: #one frame should pass before updating params and completing
            space.complete() #finish the static period
            # HACK because StaticPeriod disables this
            win.recordFrameIntervals = True

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in blankComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    #-------Ending Routine "blank"-------
    for thisComponent in blankComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # these shouldn't be strictly necessary (should auto-save)
    logging.flush()
    # the Routine "blank" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

### End Main Loop ###
#------Prepare to start Routine "Question Prep"-------
t = 0
qpClock.reset()  # clock
frameN = -1
# update component parameters for each repeat
instrKey = event.BuilderKeyResponse()  # create an object of type KeyResponse
instrKey.status = NOT_STARTED

# keep track of which components have finished
qpComponents = []
qpComponents.append(instrText_3point5)
qpComponents.append(instrText_3)
qpComponents.append(instrKey)
for thisComponent in qpComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Question Prep"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = qpClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *instrText_3* updates
    if t >= 0.0 and instrText_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText_3.tStart = t  # underestimates by a little under one frame
        instrText_3.frameNStart = frameN  # exact frame index
        instrText_3.setAutoDraw(True)

    # *instrText_3point5* updates
    if t >= 0.0 and instrText_3point5.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText_3point5.tStart = t  # underestimates by a little under one frame
        instrText_3point5.frameNStart = frameN  # exact frame index
        instrText_3point5.setAutoDraw(True)

    # *instrKey* updates
    if t >= 0.0 and instrKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrKey.tStart = t  # underestimates by a little under one frame
        instrKey.frameNStart = frameN  # exact frame index
        instrKey.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(instrKey.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if instrKey.status == STARTED:
        theseKeys = event.getKeys(keyList=['s'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            instrKey.keys = theseKeys[-1]  # just the last key pressed
            instrKey.rt = instrKey.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in qpComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Question Prep"-------
for thisComponent in qpComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

#------Prepare to start Routine "question"-------
t = 0
questClock.reset()  # clock
frameN = -1
# update component parameters for each repeat
subKey = event.BuilderKeyResponse()  # create an object of type KeyResponse
subKey.status = NOT_STARTED

# keep track of which components have finished
questComponents = []
questComponents.append(instrText_4)
questComponents.append(ansText_1)
questComponents.append(ansText_2)
questComponents.append(ansText_3)
'''
questComponents.append(respText_1)
questComponents.append(respText_2)
questComponents.append(respText_3)
questComponents.append(image1)
questComponents.append(image2)
questComponents.append(image3)
questComponents.append(image4)
'''
questComponents.append(subKey)
for thisComponent in questComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "question"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = questClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *instrText_4* updates
    if t >= 0.0 and instrText_4.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText_4.tStart = t  # underestimates by a little under one frame
        instrText_4.frameNStart = frameN  # exact frame index
        instrText_4.setAutoDraw(True)

    # *ansText_1* updates
    if t >= 0.0 and ansText_1.status == NOT_STARTED:
        # keep track of start time/frame for later
        ansText_1.tStart = t  # underestimates by a little under one frame
        ansText_1.frameNStart = frameN  # exact frame index
        ansText_1.setAutoDraw(True)

    # *ansText_2* updates
    if t >= 0.0 and ansText_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        ansText_2.tStart = t  # underestimates by a little under one frame
        ansText_2.frameNStart = frameN  # exact frame index
        ansText_2.setAutoDraw(True)

    # *ansText_3* updates
    if t >= 0.0 and ansText_3.status == NOT_STARTED:
        # keep track of start time/frame for later
        ansText_3.tStart = t  # underestimates by a little under one frame
        ansText_3.frameNStart = frameN  # exact frame index
        ansText_3.setAutoDraw(True)

#     # *respText_1* updates
#     if t >= 0.0 and respText_1.status == NOT_STARTED:
#         # keep track of start time/frame for later
#         respText_1.tStart = t  # underestimates by a little under one frame
#         respText_1.frameNStart = frameN  # exact frame index
#         respText_1.setAutoDraw(True)
# 
#     # *respText_2* updates
#     if t >= 0.0 and respText_2.status == NOT_STARTED:
#         # keep track of start time/frame for later
#         respText_2.tStart = t  # underestimates by a little under one frame
#         respText_2.frameNStart = frameN  # exact frame index
#         respText_2.setAutoDraw(True)
# 
#     # *respText_3* updates
#     if t >= 0.0 and respText_3.status == NOT_STARTED:
#         # keep track of start time/frame for later
#         respText_3.tStart = t  # underestimates by a little under one frame
#         respText_3.frameNStart = frameN  # exact frame index
#         respText_3.setAutoDraw(True)
# 
#     # *image1* updates
#     if t >= 0.0 and image1.status == NOT_STARTED:
#         # keep track of start time/frame for later
#         image1.tStart = t  # underestimates by a little under one frame
#         image1.frameNStart = frameN  # exact frame index
#         image1.setAutoDraw(True)
# 
#     # *image2* updates
#     if t >= 0.0 and image2.status == NOT_STARTED:
#         # keep track of start time/frame for later
#         image2.tStart = t  # underestimates by a little under one frame
#         image2.frameNStart = frameN  # exact frame index
#         image2.setAutoDraw(True)
# 
#     # *image3* updates
#     if t >= 0.0 and image3.status == NOT_STARTED:
#         # keep track of start time/frame for later
#         image3.tStart = t  # underestimates by a little under one frame
#         image3.frameNStart = frameN  # exact frame index
#         image3.setAutoDraw(True)
# 
#     # *image4* updates
#     if t >= 0.0 and image4.status == NOT_STARTED:
#         # keep track of start time/frame for later
#         image4.tStart = t  # underestimates by a little under one frame
#         image4.frameNStart = frameN  # exact frame index
#         image4.setAutoDraw(True)

    # *instrKey* updates
    if t >= 0.0 and subKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        subKey.tStart = t  # underestimates by a little under one frame
        subKey.frameNStart = frameN  # exact frame index
        subKey.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(instrKey.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if instrKey.status == STARTED:
        theseKeys = event.getKeys()

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            instrKey.keys = theseKeys[-1]  # just the last key pressed
            instrKey.rt = instrKey.clock.getTime()
            # a response ends the routine
            time.sleep(.500) # hold to catch all button responses
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in questComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "question"-------
for thisComponent in questComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)


#------Prepare to start Routine "Well Done"-------
t = 0
doneClock.reset()  # clock
frameN = -1
# update component parameters for each repeat
instrKey = event.BuilderKeyResponse()  # create an object of type KeyResponse
instrKey.status = NOT_STARTED

# keep track of which components have finished
doneComponents = []
doneComponents.append(instrText_5)
doneComponents.append(instrKey)
for thisComponent in doneComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "Well Done"-------
continueRoutine = True
while continueRoutine:
    # get current time
    t = doneClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *instrText_5* updates
    if t >= 0.0 and instrText_5.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrText_5.tStart = t  # underestimates by a little under one frame
        instrText_5.frameNStart = frameN  # exact frame index
        instrText_5.setAutoDraw(True)

    # *instrKey* updates
    if t >= 0.0 and instrKey.status == NOT_STARTED:
        # keep track of start time/frame for later
        instrKey.tStart = t  # underestimates by a little under one frame
        instrKey.frameNStart = frameN  # exact frame index
        instrKey.status = STARTED
        # keyboard checking is just starting
        win.callOnFlip(instrKey.clock.reset)  # t=0 on next screen flip
        event.clearEvents(eventType='keyboard')
    if instrKey.status == STARTED:
        theseKeys = event.getKeys(keyList=['s'])

        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            instrKey.keys = theseKeys[-1]  # just the last key pressed
            instrKey.rt = instrKey.clock.getTime()
            # a response ends the routine
            continueRoutine = False

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in doneComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "Well Done"-------
for thisComponent in doneComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# these shouldn't be strictly necessary (should auto-save)
logging.flush()
# make sure everything is closed down
win.close()
core.quit()
