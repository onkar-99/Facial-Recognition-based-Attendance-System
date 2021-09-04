# Facial-Recognition-based-Attendance-System
This is a Facenet based implementation for Face Recognition which recognises the employees/students in a video feed and marks the attendance accordingly. 

# Facenet:
FaceNet is a face recognition pipeline that learns mapping from faces to a position in a multidimensional space where the distance between points directly correspond to a measure of face similarity.
So in simple terms we find the face encodings which are unique to each face image, and then compare the face encodings of test images with the face encodings in the train dataset. 
These face encodings are the output given by Facenet

There is a well functional GUI which has three options to either Add a new record, View Attendance or Take Attendane. Add record can be used to add an employee/student details along with their pictures for face recognition. 
Attendance can be viewed on GUI by entering the unique ID and Pin of the person. 
