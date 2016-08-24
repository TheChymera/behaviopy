from psychopy import core, visual, data, event
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)


x0 = 0.
x1 = 0.25

y0 = 0.
y1 = 1.

# Store info about the experiment session
expName = u'untitled'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

endExpNow = False  # flag for 'escape' or other condition => quit the exp

win = visual.Window(
	size=(2048, 1152), fullscr=True, screen=0,
	allowGUI=False, allowStencil=True,
	monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
	blendMode='avg', useFBO=True,
	units="norm",
	)

aperture_x = 0.2
aperture_y = 1

# Initialize components for Routine "trial"
trialClock = core.Clock()
mov = visual.MovieStim(
	win=win, name='mov',
	filename=u'/home/chymera/data/cameras/nd750/a/nd750_a0037.mkv',
	ori=0, opacity=1,
	depth=0.0,
	volume=0,
	units="norm",
	size=2,
	)

mov_xsize, mov_ysize = mov.size

movsection_xpos = (x0+x1)/2.
movsection_ypos = (y0+y1)/2.

mov_xpos = mov_xsize*(1./2.-movsection_xpos)
mov_ypos = mov_ysize*(1./2.-movsection_ypos)

mov.pos = (mov_xpos,mov_ypos)

aperture_x = movsection_xpos*2*mov_xsize
aperture_y = movsection_ypos*2*mov_ysize

aperture = visual.Aperture(win, size=(aperture_x,aperture_y), pos=(0, 0), ori=0, nVert=120, shape='square', inverted=False, name=None, autoLog=None)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

# ------Prepare to start Routine "trial"-------
t = 0
trialClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(30.000000)
# update component parameters for each repeat
# keep track of which components have finished
trialComponents = [mov]
for thisComponent in trialComponents:
	if hasattr(thisComponent, 'status'):
		thisComponent.status = NOT_STARTED

# -------Start Routine "trial"-------
while continueRoutine and routineTimer.getTime() > 0:
	# get current time
	t = trialClock.getTime()
	frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
	# update/draw components on each frame

	# *mov* updates
	if t >= 0.0 and mov.status == NOT_STARTED:
		# keep track of start time/frame for later
		mov.tStart = t
		mov.frameNStart = frameN  # exact frame index
		mov.setAutoDraw(True)
	frameRemains = 0.0 + 30.0- win.monitorFramePeriod * 0.75  # most of one frame period left
	if mov.status == STARTED and t >= frameRemains:
		mov.setAutoDraw(False)

	# check if all components have finished
	if not continueRoutine:  # a component has requested a forced-end of Routine
		break
	continueRoutine = False  # will revert to True if at least one component still running
	for thisComponent in trialComponents:
		if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
			continueRoutine = True
			break  # at least one component has not yet finished

	# check for quit (the Esc key)
	if endExpNow or event.getKeys(keyList=["escape"]):
		core.quit()

	# refresh the screen
	if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
		win.flip()

# -------Ending Routine "trial"-------
for thisComponent in trialComponents:
	if hasattr(thisComponent, "setAutoDraw"):
		thisComponent.setAutoDraw(False)
# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
