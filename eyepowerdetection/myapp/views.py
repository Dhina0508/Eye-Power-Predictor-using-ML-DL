from rest_framework.views import APIView
import cv2
from rest_framework.response import Response
import numpy as np
import urllib.request
from .serializers import DataModelSerializer
from rest_framework import status

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
                # Load the pre-trained Haar cascade classifier for eye detection
                xml_path = 'myapp/haarcascade_eye.xml'
                eye_cascade = cv2.CascadeClassifier(xml_path)

                # Camera parameters for distance estimation (in real-world units)
                focal_length = 800  # Focal length of the camera in pixels (example value)
                average_eye_size = 30  # Average size of an eye in pixels (example value)
                url =request.data['image']

                # Download the image from the URL
                req = urllib.request.urlopen(url)
                arr = np.asarray(bytearray(req.read()), dtype=np.uint8)

                # Decode the image data
                img = cv2.imdecode(arr, -1)
                # Load the image
                cv2.imwrite('testing_image.jpg', img)

    # Read the downloaded image
                image = cv2.imread('testing_image.jpg')

                # Convert the image to grayscale for better processing
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Detect eyes in the image
                eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
                totaldistance = 0
                # Draw rectangles around detected eyes and estimate distance
                for (ex, ey, ew, eh) in eyes:
                    # Calculate distance to the eye using monocular depth estimation
                    # Depth = (average_eye_size * focal_length) / eye_size_in_pixels
                    distance = (average_eye_size * focal_length) / ew
                    distance = round(distance, 2) / 100  # Round to two decimal places
                    totaldistance += distance
                totaldistance = totaldistance / 2


                pupildis = 0.03
                distantpower = (1 / pupildis)
                closepower = (1 / totaldistance) + (1 / pupildis)
                power = (1 / closepower) + (1 / distantpower)
                return Response({"power": power})
            else:   
            # Return error response if data is invalid
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error":str(e)}, status=500)