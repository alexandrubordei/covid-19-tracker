import http.server
import socketserver
from os import curdir, sep,environ, path
from update import update_and_upload
from jinja2 import Template, Environment,FileSystemLoader

PORT = int(environ.get("PORT", 5000))

TEMPLATES_DIR = curdir+sep+"templates"
STATIC_DIR= curdir+sep+"static"

STATS_PNG_NAME = STATIC_DIR+sep+"romania_stats.png"
TEMPLATE_SUFFIX=".tmpl"

#This class will handles any incoming request from
#the browser 
class myHandler(http.server.SimpleHTTPRequestHandler):

	#Handler for the GET requests
	def do_GET(self):
		

		if self.path=="/":
			self.path="/index.html"

		try:
			if self.path=="/update":
				update_and_upload()
				self.path="/updated.html"

		except Exception as e:
			print(e)
			self.send_error(500,'Internal error')
		
		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".png"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True

			if sendReply == True:
				p = STATIC_DIR + sep + self.path
				
				if path.exists(p):
					#Open the static file requested and send it
					f = open(p,"rb") 
					self.send_response(200)
					self.send_header('Content-type',mimetype)
					self.end_headers()
					self.wfile.write(f.read())
					f.close()

				else:
					tmpl = TEMPLATES_DIR + self.path + TEMPLATE_SUFFIX
					
					if self.path.endswith(".html") and path.exists(tmpl):
						print("in")
						env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
						template = env.get_template(self.path + TEMPLATE_SUFFIX)
						output = template.render()
						self.send_response(200)
						self.send_header('Content-type',mimetype)
						self.end_headers()
						self.wfile.write(output.encode('utf-8'))

			return


		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = socketserver.TCPServer(('', PORT), myHandler)
	print('Started httpserver on port ' , PORT)
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print('^C received, shutting down the web server')
	server.socket.close()
	