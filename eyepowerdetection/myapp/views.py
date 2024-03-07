from rest_framework.views import APIView
import cv2
from rest_framework.response import Response

class PredictPower(APIView):
    def post(self,request):

        # Load the pre-trained Haar cascade classifier for eye detection
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        # Camera parameters for distance estimation (in real-world units)
        focal_length = 800  # Focal length of the camera in pixels (example value)
        average_eye_size = 30  # Average size of an eye in pixels (example value)

        print(request.data['image'])
        # Load the image
        image = cv2.imread(request.data['image'])

        # Convert the image to grayscale for better processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect eyes in the image
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        totaldistance = 0
        # Draw rectangles around detected eyes and estimate distance
        for (ex, ey, ew, eh) in eyes:
            # Draw rectangle around the detected eye
            cv2.rectangle(image, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
            
            # Calculate distance to the eye using monocular depth estimation
            # Depth = (average_eye_size * focal_length) / eye_size_in_pixels
            distance = (average_eye_size * focal_length) / ew
            distance = round(distance, 2)/100  # Round to two decimal places
            
            # Display distance on the image
            cv2.putText(image, f'{distance}', (ex, ey - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            totaldistance += distance

        totaldistance = totaldistance/2

        # Display the image with detected eyes and distance information
        cv2.imshow('Eye Detection with Distance Estimation', image)
        pupildis = 0.03
        distantpower = (1/pupildis)
        closepower = (1/totaldistance) + (1/pupildis)
        print("Close Vision",1/closepower)
        print("Distant Vision",1/distantpower)
        power = (1/closepower) + (1/distantpower)
        print(round(power))

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return Response({"power":power})
