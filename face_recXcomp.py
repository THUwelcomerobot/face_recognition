import os
import cv2    
import face_recognition
import rospy
from std_msgs.msg import String 

class DetXRec(object):
	"""
	DESCRIPTION:
		class 'DetXRec' assembles both the face detection and the face recognition function,
		which will generate labeled images and lists of recognized individuals as the output.
	FUNCTION:
		- __init__()
		- compare_faces()
		- whoIsThis()	  
		- display()		  

	"""
	def __init__(self):
		templates_path = os.path.dirname(os.path.dirname(__file__)) + "/templates"
		templates_files = os.listdir(templates_path)
		templates = []

		for template in templates_files:
			templates.append(os.path.join(templates_path, template))
		self.templates = templates

		self.images = []
		self.face_encodings = [] 

		# loading templates (src_pictures) as the fudicial marks
		for template in self.templates:
			# filename = template + ".jpg" 			
			image = face_recognition.load_image_file(template)  
			self.images.append(image) 

      	# encoding src_pictures
		for image in self.images:
			encoding = face_recognition.face_encodings(image)[0]  			
			self.face_encodings.append(encoding) 

	def update_templates(self):
		templates_path = os.path.dirname(os.path.dirname(__file__)) + "/templates"
		templates_files = os.listdir(templates_path)
		templates = []

		for template in templates_path:
			templates.append(os.path.join(templates_path, template))

		self.templates = templates

	def load_unknown_face(self, dest):
		"""
 		DESCRIPTION:
 			compare_faces(self, dest) function executes the detection & recognition process,
 			and returns the labeled image as well as a list holding the names of the recogn
 			-ized individuals.

 		PARAMETER:
 			dest - string, indicating the path of the dest. picture
 		"""
 		dest = os.path.join(os.path.dirname(os.path.dirname(__file__)), dest)
		unknown_image = face_recognition.load_image_file(dest) 
		self.unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0] 

		# for i in range(len(unknown_face_encodings)):     
		# 	unknown_encoding = unknown_face_encodings[i]      
		# 	face_location = face_locations[i]      
		# 	top, right, bottom, left = face_location      
		# 	cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)      
		
		# cv2.putText(unknown_image, name, (left-10, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)        		 
     
		# self.unknown_image_rgb = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB) 
		# return unknown_image_rgb

	def whoIsThis(self):
		results = face_recognition.compare_faces(self.face_encodings, self.unknown_face_encoding, tolerance = 0.35)
			# print(len(self.face_encodings),len(unknown_face_encodings))
			# print(len(self.images))
			      
		try:
			j = results.index(True)
			name = os.path.splitext(os.path.split(self.templates[j])[1])[0]
		except ValueError:
			name = 'unknown'
		return name

	def whoIsMostlikely(self):
		distances = face_recognition.face_distance(self.face_encodings, self.unknown_face_encoding).tolist()
		list = distances[:]
		print(list)
		list[list.index(min(list))] = 1

		name = os.path.splitext(os.path.split(self.templates[list.index(min(list))])[1])[0]
		return name, self.templates[list.index(min(list))]

# test
# templates = ["ryp", "2016011417", "2016011493"] 

# instance = DetXRec(templates) 
# instance.compare_faces('test.jpg')
# # labeled_img = instance.display()
# # cv2.imshow("Output", labeled_img) 
# # cv2.waitKey(0)
# print(instance.whoIsThis())
# print(instance.whoIsMostlikely())