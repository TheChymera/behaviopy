import os
from psychopy import core, visual, data, event
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

def evaluate(recording_path, trial_duration, events={},bracket="", volume=1.):
	"""Evaluate a behavioural recording.

	Parameters
	----------
	recording_path: str
		Path to the recording file.
	trial_duration: int
		Number of seconds the trial should last after pressing the evaluation start key.

	"""

	recording_path = os.path.expanduser(recording_path)

	keylist = ['left','right','up','down','escape','return']
	experiment_keylist = events.keys()
	keylist.extend(experiment_keylist)

	#process brackets string
	x_y_brackets = bracket.split(",")
	if len(x_y_brackets) == 1:
		x0, x1 = [float(i) for i in x_y_brackets[0].split("-")]
		y0 = 0.
		y1 = 1.
	elif len(x_y_brackets) == 2:
		try:
			x0, x1 = [float(i) for i in x_y_brackets[0].split("-")]
		except ValueError:
			x0 = 0.
			x1 = 1.
		try:
			y0, y1 = [float(i) for i in x_y_brackets[1].split("-")]
		except ValueError:
			y0 = 0.
			y1 = 1.

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
		filename=recording_path,
		depth=0.0,
		volume=volume,
		units="norm",
		size=2,
		)

	#position video in order to center bracket
	mov_xsize, mov_ysize = mov.size
	movsection_xpos = (x0+x1)/2.
	movsection_ypos = (y0+y1)/2.
	mov_xpos = mov_xsize*(1./2.-movsection_xpos)
	mov_ypos = mov_ysize*(1./2.-movsection_ypos)
	mov.pos = (mov_xpos,mov_ypos)

	#set aperture to bracket
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
	# update component parameters for each repeat
	# keep track of which components have finished
	mov.status = NOT_STARTED

	pre_evaluation = True

	# -------Start Routine "trial"-------
	while pre_evaluation or routineTimer.getTime() > 0:

		resp_key = event.getKeys(keyList=keylist)
		if pre_evaluation:
			if "return" in resp_key:
				routineTimer.reset()  # clock
				routineTimer.add(trial_duration)
				pre_evaluation=False
		else:
			pass

		# get current time
		t = trialClock.getTime()

		#start movie and keep track of start time
		if t >= 0.0 and mov.status == NOT_STARTED:
			mov.tStart = t
			mov.setAutoDraw(True)

		if mov.status == FINISHED:
			break

		# check for quit (the Esc key)
		if "escape" in resp_key:
			core.quit()

		win.flip()

	# -------Ending Routine "trial"-------
	mov.setAutoDraw(False)
	# these shouldn't be strictly necessary (should auto-save)
	thisExp.saveAsWideText(filename+'.csv')
	thisExp.saveAsPickle(filename)
	logging.flush()
	# make sure everything is closed down
	thisExp.abort()  # or data files will save again on exit
	win.close()
	core.quit()

if __name__ == '__main__':
	recording_path =u"/home/chymera/data/cameras/nd750/a/nd750_a0037.mkv"
	# recording_path = u"/home/chymera/data/cameras/nd750/a/.MOV/nd750_a0037.MOV"
	evaluate(recording_path,10,events={"s":"swimming","f":"floating"}, bracket="0-0.25,", volume=0)
