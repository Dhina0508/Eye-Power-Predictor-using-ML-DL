from rest_framework.views import APIView
import cv2
from rest_framework.response import Response
import numpy as np
import urllib.request
from .serializers import DataModelSerializer
from rest_framework import status
import joblib
import os


path=os.getcwd()

diag=joblib.load(path+"/myapp/models/diag.joblib")
lf_pow=joblib.load(path+"/myapp/models/lf_pow.joblib")
rf_pow=joblib.load(path+"/myapp/models/rf_pow.joblib")
# diag=joblib.load(path+"\\myapp\\models\\diag.joblib")
# lf_pow=joblib.load(path+"\\myapp\\models\\lf_pow.joblib")
# rf_pow=joblib.load(path+"\\myapp\\models\\rf_pow.joblib")

class PredictPower(APIView):
     def post(self, request):
        try:
                # Parse incoming data from request
            data = request.data
            
            # Deserialize and validate data using serializer
            serializer = DataModelSerializer(data=data)
            if serializer.is_valid():
            # Save validated data to database
                serializer.save()
                # fontsize=request.data['fontSize']

                # Camera parameters for distance estimation (in real-world units)
                focal_length = 800  # Focal length of the camera in pixels (example value)
                average_eye_size = 30  # Average size of an eye in pixels (example value)
                left =request.data['left']
                right =request.data['right']
                both =request.data['both']

                # Download the image from the URL
                lefturl = urllib.request.urlopen(left)
                righturl = urllib.request.urlopen(right)
                bothurl = urllib.request.urlopen(both)


                leftarr = np.asarray(bytearray(lefturl.read()), dtype=np.uint8)
                rightarr = np.asarray(bytearray(righturl.read()), dtype=np.uint8)
                botharr = np.asarray(bytearray(bothurl.read()), dtype=np.uint8)

                # Decode the image data
                leftimg = cv2.imdecode(leftarr, -1)
                rightimg = cv2.imdecode(rightarr, -1)
                bothimg = cv2.imdecode(botharr, -1)

                # Load the image
                # cv2.imwrite('testing_image.jpg', img)

                # # Read the downloaded image
                # image = cv2.imread('testing_image.jpg')

                # Convert the image to grayscale for better processing
                leftgray = cv2.cvtColor(leftimg, cv2.COLOR_BGR2GRAY)
                rightgray = cv2.cvtColor(rightimg, cv2.COLOR_BGR2GRAY)
                bothgray = cv2.cvtColor(bothimg, cv2.COLOR_BGR2GRAY)

                
                # Load the pre-trained Haar cascade classifier for eye detection
                xml_path = 'myapp/models/haarcascade_eye.xml'
                eye_cascade = cv2.CascadeClassifier(xml_path)

                # Detect eyes in the image
                lefteye = eye_cascade.detectMultiScale(leftgray, scaleFactor=1.1, minNeighbors=5)
                righteye = eye_cascade.detectMultiScale(rightgray, scaleFactor=1.1, minNeighbors=5)
                botheyes = eye_cascade.detectMultiScale(bothgray, scaleFactor=1.1, minNeighbors=5)
                leftdistance = 0
                leftcount = 0
                rightdistance = 0
                rightcount = 0 
                bothdistance = 0
                bothcount = 0
                # Draw rectangles around detected eyes and estimate distance
                for (ex, ey, ew, eh) in lefteye:
                    # Calculate distance to the eye using monocular depth estimation
                    # Depth = (average_eye_size * focal_length) / eye_size_in_pixels
                    distance = (average_eye_size * focal_length) / ew
                    distance = round(distance, 2) / 100  # Round to two decimal places
                    leftdistance += distance
                    leftcount +=1
                leftdistance = leftdistance/leftcount
                
                for (ex, ey, ew, eh) in righteye:
                    # Calculate distance to the eye using monocular depth estimation
                    # Depth = (average_eye_size * focal_length) / eye_size_in_pixels
                    distance = (average_eye_size * focal_length) / ew
                    distance = round(distance, 2) / 100  # Round to two decimal places
                    rightdistance += distance
                    rightcount +=1
                rightdistance = rightdistance/rightcount
                
                for (ex, ey, ew, eh) in botheyes:
                    # Calculate distance to the eye using monocular depth estimation
                    # Depth = (average_eye_size * focal_length) / eye_size_in_pixels
                    distance = (average_eye_size * focal_length) / ew
                    distance = round(distance, 2) / 100  # Round to two decimal places
                    bothdistance += distance
                    bothcount +=1
                bothdistance = bothdistance/bothcount


                # pupildis = 0.03
                # distantpower = (1 / pupildis)
                # closepower = (1 / totaldistance) + (1 / pupildis)
                # power = (1 / closepower) + (1 / distantpower)
                data = {"left_eye_distance": leftdistance,"right_eye_distance": rightdistance,    "both_eye_distance": bothdistance,
    "left_fontsize": request.data['left_fontsize'],
    "right_fontsize": request.data['right_fontsize'],
    "both_eye_fontsize": request.data['both_eye_fontsize']
} 
                dg=diag.predict(data)
                lf=lf_pow.predict(data)
                rf=rf_pow.predict(data)
                return Response({"diagnosis":dg,"left_power":lf,"right_power":rf})
            else:   
            # Return error response if data is invalid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)}, status=500)
        
class diagonisis(APIView):
     def post(self, request):
         request_data = request.data
         input_data = np.array([list(request_data.values())])
         dg=diag.predict(input_data)
         lf=lf_pow.predict(input_data)
         rf=rf_pow.predict(input_data)
         return Response({"diagnosis":dg,"left_power":lf,"right_power":rf})
