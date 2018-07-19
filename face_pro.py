import os
import time
import shutil
from face_recXcomp import DetXRec
from makeup import makeup

dest = "/run/user/1000/gvfs/smb-share:server=192.168.0.127,share=share/makeup.png"
src = "/run/user/1000/gvfs/smb-share:server=192.168.0.127,share=share/unknown.png"
likely_face = "/run/user/1000/gvfs/smb-share:server=192.168.0.127,share=share/likely_face.png"

def recognition(file, node):
	node.load_unknown_face(file)
	name, index = node.whoIsMostlikely()
	print(name)
	print(node.whoIsThis())
	shutil.copyfile(index,likely_face)          
	f = open('/run/user/1000/gvfs/smb-share:server=192.168.0.127,share=share/result_1.txt', 'w') 
	f.write(node.whoIsThis())
	f.close()
	f = open('/run/user/1000/gvfs/smb-share:server=192.168.0.127,share=share/result_2.txt', 'w') 
	f.write(name)
	f.close()

if __name__ == '__main__':
	node = DetXRec()
	while(True):
		try:
			# start = time.time()
			recognition(src, node)
			makeup(src, dest)
			# print(time.time()-start)	
			time.sleep(10)
			os.remove(src)
		except Exception:
			print("!")
		