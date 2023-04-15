#####
# A Python script for OBS that allows a source to be controlled
# using the mouse. One source in one scene can be controlled. If
# you want to have a source move in multiple scenes, you can
# create a blank scene, add the source you want to move, and
# then add scene sources to other scenes where it should be
# visible.
#
# Dependent on pynput: https://pypi.org/project/pynput/
# pip install pynput
#
# Tested on Python 3.6 and OBS version 28.0.2
#####

import obspython as obs
from pynput import mouse as Mouse
import time

scene_item      = None
scene_name      = ""
source_name     = ""
scale           = 1
offset_x        = 0
offset_y        = 0
listener        = None
pos             = obs.vec2()

current_time    = 0
running_log     = ""


# ------------------------------------------------------------
# -- My functions
# ------------------------------------------------------------

def initialize():
	global scene_item
	global scene_name
	global source_name

	# Remove the callback in case this is from a repeating timer
	obs.remove_current_callback()

	# Get the list of scenes
	scene_list = obs.obs_frontend_get_scenes()

	# Search for the scene and source we want
	for scene_source in scene_list: # scene_source is a source, not a scene. See note at end of function
		name = obs.obs_source_get_name(scene_source)
		if name == scene_name:
			# Found!
			scene_item = obs.obs_scene_find_source(obs.obs_scene_from_source(scene_source), source_name)
			obs.source_list_release(scene_list)
			return

	# We didn't find what we were looking for, so try again later
	obs.timer_add(initialize, 2000)

	# Release the list of scenes from memory
	obs.source_list_release(scene_list)

	# Note on scenes and sources:
	# The obs_frontend_get_scenes funciton does not actually return a list of
	# scenes. Everything in OBS is a source and the list contains the source
	# for each scene. For functions that need the actual scene object,
	# obs_scene_from_source is used to extract ¿cast? the scene from its source.

def on_mouse_move(x, y):
	global scene_item
	global scale
	global offset_x
	global offset_y
	global pos

	if scene_item is not None and obs.obs_sceneitem_visible(scene_item):
		obs.vec2_set(pos, (x + offset_x) * scale, (y + offset_y) * scale)
		obs.obs_sceneitem_set_pos(scene_item, pos)

		position_check = obs.vect2()
		obs.obs_sceneitem_get_pos(scene_item, position_check)

		if abs(position_check[0]) < 10 and abs(position_check[1]) < 10:
			print("Found scene_item at " + stringify_pos(position_check) + "while pos is " + stringify_pos(pos))
		if position_check[0] != pos[0] or position_check[1] != pos[1]:
			print("Found improper movement. Found scene_item at " + stringify_pos(position_check) + ". Expected at " + stringify_pos(pos))

		running_log += "m"

def stringify_pos(pos):
	return "(" + str(pos[0]) + ", " + str(pos[1]) + ")"

# ------------------------------------------------------------
# -- Built-in functions
# ------------------------------------------------------------

def script_tick():

	if scene_item is not None and obs.obs_sceneitem_visible(scene_item):
		running_log += "T"
		if len(running_log) >= 100:
			print(running_log)
			running_log = ""

def script_description():
	return "Make a source move by copying mouse movement."


def script_load(settings):
	global listener

	#print("loading")

	initialize()

	if listener is None:
		listener = Mouse.Listener(
				on_move = on_mouse_move
		)
		listener.start()
		#listener.stop()


def script_update(settings):
	global scene_name
	global source_name
	global scale
	global offset_x
	global offset_y

	#print("updating")

	scale       = obs.obs_data_get_double(settings, "scale")
	offset_x    = obs.obs_data_get_double(settings, "offset_x")
	offset_y    = obs.obs_data_get_double(settings, "offset_y")
	scene_name = obs.obs_data_get_string(settings, "scene")
	source_name = obs.obs_data_get_string(settings, "source")
	
	initialize()


def script_unload():
	global listener
	listener.stop()


def script_defaults(settings):
	obs.obs_data_set_default_double(settings, "scale", 1)
	obs.obs_data_set_default_double(settings, "offset_x", 0)
	obs.obs_data_set_default_double(settings, "offset_y", 0)


def script_properties():
	props = obs.obs_properties_create()

	obs.obs_properties_add_text(props, "scene", "Scene Name", obs.OBS_TEXT_DEFAULT)
	obs.obs_properties_add_text(props, "source", "Source Name", obs.OBS_TEXT_DEFAULT)
	obs.obs_properties_add_float(props, "offset_x", "X offset", -1000, 1000, 1)
	obs.obs_properties_add_float(props, "offset_y", "Y offset", -1000, 1000, 1)
	obs.obs_properties_add_float(props, "scale", "Motion Scale", 0.01, 10, 0.2)

	return props