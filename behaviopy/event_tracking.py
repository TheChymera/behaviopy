import csv
import os
from psychopy import core, visual, data, event
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

def evaluate_db(db_path, test_type, animal_ids=[], animals_id_column="id_eth", dates=[], output_dir="~/data/behaviour", author="", volume=0):
	"""Wrapper for evaluate() passing data from a LabbookDB model database.

	"""
	import sys
	sys.path.append(os.path.expanduser('~/src/LabbookDB/db/'))
	from query import get_df

	if not author:
		print("It is advisable to add your name's three-letter abbreviation via the \"author\" argument. This helps identify your work and protects it from being overwritten.")

	db_path = os.path.expanduser(db_path)
	output_dir = os.path.expanduser(output_dir)

	if test_type == "forced_swim_test":
		measurements_table = "ForcedSwimTestMeasurement"
		output_dir = os.path.join(output_dir,"forced_swim_test")
		trial_duration = 360 #in seconds
		events = {"s":"swimming","f":"floating"}
	else:
		raise ValueError("The function does not support test_type=\'"+test_type+"\'.")


	col_entries=[
		("Animal","id"),
		(measurements_table,),
		]
	join_entries=[
		("Animal.measurements",),
		(measurements_table,),
		]

	filters = []
	if animal_ids:
		filter_entry = ["Animal",animals_id_column,]
		for animal_id in animal_ids:
			filter_entry.extend([animal_id])
		filters.append(filter_entry)
	if dates:
		filter_entry = ["measurements_table","date"]
		for date in dates:
			filter_entry.extend([date])
		filters.append(filter_entry)

	reference_df = get_df(db_path,col_entries=col_entries, join_entries=join_entries, filters=[])
	for _, measurement_df in reference_df.iterrows():
		recording_path = measurement_df.loc[measurements_table+"_recording"]
		if measurements_table+"_recording_bracket" in reference_df.columns:
			bracket = measurement_df.loc[measurements_table+"_recording_bracket"]
		else:
			bracket = ""
		outfile_name = os.path.splitext(os.path.basename(recording_path))[0]+"_"+bracket+"_"+author
		output_path = os.path.join(output_dir,outfile_name)
		evaluate(recording_path,trial_duration,events=events,bracket=bracket, volume=volume, output_path=output_path)

def evaluate(recording_path, trial_duration, skiptime=0, events={},bracket="", volume=1.,output_path="~/evaluation.csv"):
	"""Evaluate a behavioural recording.

	Parameters
	----------
	recording_path: str
		Path to the recording file.
	trial_duration: int
		Number of seconds the trial should last after pressing the evaluation start key.

	"""

	recording_path = os.path.expanduser(recording_path)
	output_path = os.path.expanduser(output_path)

	if os.path.exists(output_path):
		print("There is already a n evaluation file at "+output_path+". Please specify a different output path.")
		return

	keylist = ['left','right','up','down','escape','return']
	experiment_keylist = events.keys()
	keylist.extend(experiment_keylist)

	#process brackets string
	x_y_brackets = bracket.split(",")
	if len(x_y_brackets) == 1:
		x0, x1 = [float(i)/100 for i in x_y_brackets[0].split("-")]
		y0 = 0.
		y1 = 1.
	elif len(x_y_brackets) == 2:
		try:
			x0, x1 = [float(i)/100 for i in x_y_brackets[0].split("-")]
		except ValueError:
			x0 = 0.
			x1 = 1.
		try:
			y0, y1 = [float(i)/100 for i in x_y_brackets[1].split("-")]
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

	# Initialize components for Routine "trial"
	trialClock = core.Clock()
	mov = visual.MovieStim2(
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
	movsection_xsize = x1-x0
	movsection_ysize = y1-y0
	aperture_x = movsection_xsize*mov_xsize
	aperture_y = movsection_ysize*mov_ysize
	aperture = visual.Aperture(win, size=(aperture_x,aperture_y), pos=(0, 0), ori=0, nVert=120, shape='square', inverted=False, name=None, autoLog=None)

	# Create some handy timers
	globalClock = core.Clock()  # to track the time since experiment started
	routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

	# ------Prepare to start Routine "trial"-------
	t = 0
	trialClock.reset()  # clock
	frameN = -1
	mov.status = NOT_STARTED

	pre_evaluation = True
	outputWriter1 = csv.writer(open(output_path,'w'), lineterminator ='\n')
	outputWriter1.writerow(["start","behaviour"])
	# -------Start Routine "trial"-------
	while pre_evaluation or routineTimer.getTime() > 0:
		# get current time
		t = trialClock.getTime()
		resp_key = event.getKeys(keyList=keylist)
		if pre_evaluation:
			if "return" in resp_key:
				routineTimer.reset()  # clock
				routineTimer.add(trial_duration)
				pre_evaluation=False
		elif resp_key:
			if resp_key[0] in experiment_keylist:
				tempArray = [t, events[resp_key[0]]]
				outputWriter1.writerow(tempArray)
				tempArray =[] #make sure no info persists

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


	for i in range(0, len(responses)):
		(responses[i])
	win.close()

if __name__ == '__main__':
	# recording_path =u"/home/chymera/data/cameras/nd750/a/nd750_a0037.mkv"
	# recording_path =u"/home/chymera/data/cameras/nd750/a/nd750_a0038.mkv"
	recording_path =u"/home/chymera/data/cameras/nd750/a/nd750_a0039.mkv"
	bracket = "58-75,"
	evaluate(recording_path,5,events={"s":"swimming","f":"floating"}, bracket=bracket, volume=0.0001)
	# evaluate_db("~/syncdata/meta.db","forced_swim_test",animal_ids=[275511],author="chr",volume=0.0001)
