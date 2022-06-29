import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from mtcnn.mtcnn import MTCNN
from tkinter import *
import cv2

# create the root window
# Root window
root = tk.Tk()
root.title('Face Detection')
root.resizable(False, False)
root.geometry('250x150')

file = None

# open a file dialog
def select_file():
    filetypes = (('JPG Image', '*.JPG'), ('MP4 Video', '*.MP4'), ('PNG Image', '*.PNG'), ('All files', '*.*'))
    global filename
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    return filename
    
# draw an image with detected objects
def draw_image_with_boxes(filename, result_list):
	# load the image
	data = pyplot.imread(filename)
	# plot the image
	pyplot.imshow(data)
	# get the context for drawing boxes
	ax = pyplot.gca()
	# plot each box
	for result in result_list:
		# get coordinates
		x, y, width, height = result['box']
		# create the shape
		rect = Rectangle((x, y), width, height, fill=False, color='red')
		# draw the box
		ax.add_patch(rect)
	# show the plot
	pyplot.show()

# draw each face separately
def draw_faces(filename, result_list):
	# load the image
	data = pyplot.imread(filename)
	# plot each face as a subplot
	for i in range(len(result_list)):
		# get coordinates
		x1, y1, width, height = result_list[i]['box']
		x2, y2 = x1 + width, y1 + height
		# define subplot
		pyplot.subplot(1, len(result_list), i+1)
		pyplot.axis('off')
		# plot face
		pyplot.imshow(data[y1:y2, x1:x2])
	# show the plot
	pyplot.show()

# capture faces from camera
def cap():
    detector = MTCNN()
    if (video.isOpened() == False):
        print("Web Camera not detected")
    while (True):
        ret, frame = video.read()
        if ret == True:
            location = detector.detect_faces(frame)
            print("Found {0} faces!".format(len(location)))
            if len(location) > 0:
                for face in location:
                    x1, y1, width, height = face['box']
                    x2, y2 = x1 + width, y1 + height
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 4)
            cv2.imshow("Output",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    video.release()
    cv2.destroyAllWindows()

# capture faces from a video
def vid():
    video = cv2.VideoCapture(filename)
    detector = MTCNN()
    # We need to check if camera
    # is opened previously or not
    if (video.isOpened() == False):
        print("Error reading video file")

    # We need to set resolutions.
    # so, convert them from float to integer.
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)

    # Below VideoWriter object will create
    # a frame of above defined The output
    # is stored in 'filename.avi' file.
    result = cv2.VideoWriter('Output.avi',cv2.VideoWriter_fourcc(*'MJPG'),29, size)
    frame_num=0
    while (True):
        ret, frame = video.read()
        frame_num += 1
        print(frame_num)
        if ret == True:

            location = detector.detect_faces(frame)
            if len(location) > 0:
                for face in location:
                    x, y, width, height = face['box']
                    x2, y2 = x + width, y + height
                    cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 4)
            result.write(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break


    video.release()
    result.release()

    # Closes all the frames
    cv2.destroyAllWindows()

    print("The video was successfully saved")


    img=cv2.imread("input & output/input.jpg")
    location = detector.detect_faces(img)
    if len(location) > 0:
        for face in location:
            x, y, width, height = face['box']
            x2, y2 = x + width, y + height
            cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 255), 4)

    cv2.imwrite("input & output/Outputfile.jpg",img)
    print("The Image was successfully saved")

# Main function
def final():
    filename = select_file()
    global pixels
    global faces
    global detector
    pixels = pyplot.imread(filename)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    faces = detector.detect_faces(pixels)
    print(faces)


# open file dialog
btn = ttk.Button(root, text='Open File', command=final)
btn.pack()

# detect from camera
video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# creating button
btn1 = ttk.Button(root, text="Draw Faces", command=lambda : draw_faces(filename, faces))
btn1.pack()
btn2 = ttk.Button(root, text='Draw Images With Boxes', command=lambda : draw_image_with_boxes(filename, faces))
btn2.pack()
btn3 = ttk.Button(root, text='Detect Using Camera', command=cap)
btn3.pack()
btn4 = ttk.Button(root, text='Detect For A Video', command=vid)
btn4.pack()
# running the main loop
root.mainloop()
    
    
    

