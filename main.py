from tkinter import *
import tkinter.font as font
from functools import partial



#window properties
window_width = 600
window_height = window_width
window_bg = "#aaffee"


cube_side_len = 3 #unit length of the edge of the cube


#Face class
class Face:
	def __init__(self, initial_color, face_name):
		self.inital_color = initial_color
		self.colors = [[initial_color, initial_color, initial_color], [initial_color, initial_color, initial_color], [initial_color, initial_color, initial_color]]
		self.name = face_name



front_face = Face("#00ff01", "Front")
back_face = Face("#0081f9", "Back")
top_face = Face("#ffffff", "Top")
bottom_face = Face("#fffc00", "Bottom")
left_face = Face("#ff7f42", "Left")
right_face = Face("#fc0102", "Right")

spotlight_face = front_face #The face that is enlarged and directly editable
spotlight_mini_cube_size = window_height/10 #The edge length of every unit cube in the rubix cube

spotlight_mini_cube_spacing = 3
spotlight_face_margin_width = window_width/2 - ((spotlight_mini_cube_size + spotlight_mini_cube_spacing + 1) * cube_side_len)
spotlight_face_margin_height = window_height - ((spotlight_mini_cube_size + spotlight_mini_cube_spacing + 1) * cube_side_len) - spotlight_face_margin_width

not_spotlight_faces = [back_face, top_face, bottom_face, left_face, right_face] #The shrunk faces that are not directly editable

faces_leftright_rot = [front_face, right_face, back_face, left_face] #Order of the faces on the cube when rotating left to right and vice versa
faces_topbottom_rot = [front_face, bottom_face, back_face, top_face] #Order of the faces on the cube when rotating top to bottom and vice versa



root = Tk() #generates a new Tk window
root.title("Rubix Cube (2D view)") #Title of window
root.geometry("{0}x{1}".format(window_width, window_height)) #Window dimensions
root.resizable(False, False)

canvas = Canvas(root, width = window_width, height = window_height, bg = window_bg) #New canvas in window
canvas.pack()



#Changes the spotlight face and "refreshes the canvas"
def change_face(face):
	global spotlight_face, not_spotlight_faces
	
	not_spotlight_faces.remove(face)
	not_spotlight_faces.append(spotlight_face)
	spotlight_face = face
	
	draw_cube() #there is code in this function that deletes all Labels, so that there is no build-up of text


#Draws the large spotlight face, every other small face, labels and control buttons. Practically the whole "cube"
def draw_cube():
	global canvas
	
	for child in list(root.children.values()): #For every widget that root possess
		if str(type(child)) == "<class 'tkinter.Label'>": #If the type of the widget is the tkinter.Label class, meaning that is a Label object
			child.destroy() #It will be self-terminated , so that there is no build-up of Labels each time this function is calld.
	
	not_spotlight_mini_cube_spacing = spotlight_mini_cube_spacing//2 + 1
	not_spotlight_mini_cube_size = spotlight_mini_cube_size//2 + 1
	
	not_spotlight_margin_height = 60
	
	black_outline = canvas.create_rectangle(0, 0, (spotlight_mini_cube_size + spotlight_mini_cube_spacing + 1) * cube_side_len, (spotlight_mini_cube_size + spotlight_mini_cube_spacing + 1) * cube_side_len, fill = "black", outline = "")
	canvas.move(black_outline, spotlight_face_margin_width - spotlight_mini_cube_spacing, spotlight_face_margin_height - spotlight_mini_cube_spacing)
	
	Label(root, text = spotlight_face.name + " face", background = window_bg).place(x = spotlight_face_margin_width - spotlight_mini_cube_spacing + (spotlight_mini_cube_size + spotlight_mini_cube_spacing + 1) * cube_side_len, y = spotlight_face_margin_height - spotlight_mini_cube_spacing + (spotlight_mini_cube_size + spotlight_mini_cube_spacing + 1) * cube_side_len)
	
	for i in range(cube_side_len):
		for j in range(cube_side_len):
			mini_cube = canvas.create_rectangle(0, 0, spotlight_mini_cube_size, spotlight_mini_cube_size, fill = spotlight_face.colors[j][i], outline = "")
			canvas.move(mini_cube, spotlight_face_margin_width + i * (spotlight_mini_cube_size + spotlight_mini_cube_spacing), spotlight_face_margin_height + j * (spotlight_mini_cube_size + spotlight_mini_cube_spacing))
			
			
	for k in range(len(not_spotlight_faces)):
		nsf = not_spotlight_faces[k]
		
		black_outline = canvas.create_rectangle(0, 0, (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing + 1) * cube_side_len, (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing + 1) * cube_side_len, fill = "black", outline = "")
		canvas.move(black_outline, ((window_width - ((len(not_spotlight_faces)-1)*spotlight_face_margin_width + (cube_side_len * (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing)))) / 2) + k*spotlight_face_margin_width - not_spotlight_mini_cube_spacing, not_spotlight_margin_height - not_spotlight_mini_cube_spacing)
		
		Label(root, text = nsf.name + " face", background = window_bg).place(x = (window_width - ((len(not_spotlight_faces)-1)*spotlight_face_margin_width + (cube_side_len * (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing)))) / 2 + (k * ((not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing*4) * cube_side_len)), y = 3 + not_spotlight_margin_height + cube_side_len * (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing))
		
		view_face_btn = Button(root, text = "view", command = partial(change_face, nsf)) #button changes spotlight face when clicked
		view_face_btn.place(x = ((window_width - ((len(not_spotlight_faces)-1)*spotlight_face_margin_width + (cube_side_len * (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing)))) / 2) + k*spotlight_face_margin_width - not_spotlight_mini_cube_spacing, y = not_spotlight_margin_height - not_spotlight_mini_cube_spacing - not_spotlight_mini_cube_size, width = not_spotlight_mini_cube_spacing + (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing) * 3, height = not_spotlight_mini_cube_size)
		
		for i in range(cube_side_len):
			for j in range(cube_side_len):
				mini_cube = canvas.create_rectangle(0, 0, not_spotlight_mini_cube_size, not_spotlight_mini_cube_size, fill = nsf.colors[j][i], outline = "")
				canvas.move(mini_cube, (window_width - ((len(not_spotlight_faces)-1)*spotlight_face_margin_width + (cube_side_len * (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing)))) / 2 + k*spotlight_face_margin_width + (i * (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing)), not_spotlight_margin_height + j * (not_spotlight_mini_cube_size + not_spotlight_mini_cube_spacing))
	



#Draws the control buttons to rotate each slice of the "cube".
def draw_rotation_buttons():
	button_width = spotlight_mini_cube_size
	button_height = spotlight_mini_cube_size/2
	
	def rotate_to_left(layer_num):
		old_spotlight_face_colors = spotlight_face.colors[layer_num]
		
		for face in faces_leftright_rot:
			face.colors[layer_num] = faces_leftright_rot[(faces_leftright_rot.index(face) + 1) % len(faces_leftright_rot)].colors[layer_num]
			
		faces_leftright_rot[faces_leftright_rot.index(spotlight_face) - 1].colors[layer_num] = old_spotlight_face_colors
		
		draw_cube()
		
	def rotate_to_right(layer_num):
		global spotlight_face
		
		old_face_before_spotlight_colors = faces_leftright_rot[faces_leftright_rot.index(spotlight_face) - 1].colors[layer_num]
		
		for i in range(len(faces_leftright_rot), 0, -1):
			face = faces_leftright_rot[i - 1]
			face.colors[layer_num] = faces_leftright_rot[(faces_leftright_rot.index(face) - 1) % len(faces_leftright_rot)].colors[layer_num]
			
		spotlight_face.colors[layer_num] = old_face_before_spotlight_colors
		
		draw_cube()
		
	
	def rotate_to_up(layer_num):
		old_spotlight_face_colors = [spotlight_face.colors[0][layer_num], spotlight_face.colors[1][layer_num], spotlight_face.colors[2][layer_num]]
		
		for face in faces_topbottom_rot:
			face.colors[0][layer_num] = faces_topbottom_rot[(faces_topbottom_rot.index(face) + 1) % len(faces_topbottom_rot)].colors[0][layer_num]
			face.colors[1][layer_num] = faces_topbottom_rot[(faces_topbottom_rot.index(face) + 1) % len(faces_topbottom_rot)].colors[1][layer_num]
			face.colors[2][layer_num] = faces_topbottom_rot[(faces_topbottom_rot.index(face) + 1) % len(faces_topbottom_rot)].colors[2][layer_num]
			
		faces_topbottom_rot[faces_topbottom_rot.index(spotlight_face) - 1].colors[0][layer_num] = old_spotlight_face_colors[0]
		faces_topbottom_rot[faces_topbottom_rot.index(spotlight_face) - 1].colors[1][layer_num] = old_spotlight_face_colors[1]
		faces_topbottom_rot[faces_topbottom_rot.index(spotlight_face) - 1].colors[2][layer_num] = old_spotlight_face_colors[2]
		
		draw_cube()
		
		
	def rotate_to_down(layer_num):
		global spotlight_face
		
		old_face_before_spotlight_colors = [faces_topbottom_rot[faces_topbottom_rot.index(spotlight_face) - 1].colors[0][layer_num], faces_topbottom_rot[faces_topbottom_rot.index(spotlight_face) - 1].colors[1][layer_num], faces_topbottom_rot[faces_topbottom_rot.index(spotlight_face) - 1].colors[2][layer_num]]
		
		for i in range(len(faces_topbottom_rot), 0, -1):
			face = faces_topbottom_rot[i - 1]
			
			face.colors[0][layer_num] = faces_topbottom_rot[(faces_topbottom_rot.index(face) - 1) % len(faces_topbottom_rot)].colors[0][layer_num]
			face.colors[1][layer_num] = faces_topbottom_rot[(faces_topbottom_rot.index(face) - 1) % len(faces_topbottom_rot)].colors[1][layer_num]
			face.colors[2][layer_num] = faces_topbottom_rot[(faces_topbottom_rot.index(face) - 1) % len(faces_topbottom_rot)].colors[2][layer_num]
			
		spotlight_face.colors[0][layer_num] = old_face_before_spotlight_colors[0]
		spotlight_face.colors[1][layer_num] = old_face_before_spotlight_colors[1]
		spotlight_face.colors[2][layer_num] = old_face_before_spotlight_colors[2]
		
		draw_cube()
		
	
	
	for i in range(cube_side_len):
		to_up_layer_btn = Button(root, text = "↑", command = partial(rotate_to_up, i))
		to_up_layer_btn.place(x = spotlight_face_margin_width + button_height/2 + i * (spotlight_mini_cube_size + spotlight_mini_cube_spacing), y = spotlight_face_margin_height - spotlight_mini_cube_size - spotlight_mini_cube_spacing - spotlight_mini_cube_size/4, width = button_height, height = button_width)
		to_up_layer_btn["font"] = font.Font(family = "High Tower Text", size = int(spotlight_mini_cube_size/3))
		
		to_down_layer_btn = Button(root, text = "↓", command = partial(rotate_to_down, i))
		to_down_layer_btn.place(x = spotlight_face_margin_width + button_height/2 + i * (spotlight_mini_cube_size + spotlight_mini_cube_spacing), y = (spotlight_face_margin_height + cube_side_len * (spotlight_mini_cube_size + spotlight_mini_cube_spacing)) + spotlight_mini_cube_size/4, width = button_height, height = button_width)
		to_down_layer_btn["font"] = font.Font(family = "High Tower Text", size = int(spotlight_mini_cube_size/3))
	
	
	for i in range(cube_side_len):
		to_left_layer_btn = Button(root, text = "←", command = partial(rotate_to_left, i))
		to_left_layer_btn.place(x = spotlight_face_margin_width - button_width - spotlight_mini_cube_spacing - spotlight_mini_cube_size/4, y = ((spotlight_face_margin_height + spotlight_mini_cube_size/2) - button_height/2) + i * (spotlight_mini_cube_size + spotlight_mini_cube_spacing), width = button_width, height = button_height)
		to_left_layer_btn["font"] = font.Font(family = "High Tower Text", size = int(spotlight_mini_cube_size/3))
		
		to_right_layer_btn = Button(root, text = "→", command = partial(rotate_to_right, i))
		to_right_layer_btn.place(x = ((spotlight_face_margin_width + spotlight_mini_cube_size/2) + button_width/2 + spotlight_mini_cube_spacing + spotlight_mini_cube_size/4) + (cube_side_len-1) * (spotlight_mini_cube_size + spotlight_mini_cube_spacing), y = ((spotlight_face_margin_height + spotlight_mini_cube_size/2) - button_height/2) + i * (spotlight_mini_cube_size + spotlight_mini_cube_spacing), width = button_width, height = button_height)
		to_right_layer_btn["font"] = font.Font(family = "High Tower Text", size = int(spotlight_mini_cube_size/3))



draw_cube()
draw_rotation_buttons()

root.mainloop()
