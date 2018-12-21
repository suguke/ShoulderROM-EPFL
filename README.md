# Shoulder Range of Motion Evaluation
EPFL - Biomechanics of the musculo-skeletal system project

# Abstract
This project sought to develop a tool to evaluate the range of motion of the shoulder, in the context of a consultation, based on inertial measurement units. Since shoulder problems represent a significant mass of hospital admissions, it is interesting to speed up consultations by improving the quality of angle measurements. The various constraints are an angle accuracy of less than 5°, ease of use through an interface, compatibility with the institution's databases and the possibility of outsourcing the system. This project achieved the precision objective with a maximum error of 1.51°. The implementation of a user-friendly and cross-platform application makes it easy to use during consultations as well as using the interface on various operating systems. Temporary solutions have been found to the various technical difficulties and perspectives are provided on the limitations of a system  based on inertial measurement units. In conclusion, this project proposes a promising pipeline application to integrate inertial measurement units into the clinical world.

# Approach
In order to automate the clinical examination of the shoulder, we developed a user-friendly application capable of bringing together all the necessary steps for the consultation. Python has proven to be the most suitable programming language for its rapid development, its numerous libraries and its dynamic community. The graphic user interface (GUI) is obtained thanks to the `Kivy` library. It is an open source and cross-platform library, ideal for using the application on different operating systems. 

The interface can be described according to the different screens consisting of: 
- The *Barcode Screen*, for the medical doctor (MD) to type in the patient and consultation codes, 
- The *Question screen* gathering request about the *Score of Constant* and the *ISOBEX* force measurment allows the MD to enter the values for both the left and right arm at the same time,
- The *Measurement Screen*, where the MD have to import csv files for each movement of each arm,
- The *Results Screen* summarizes all the measured angles. It also displays the \textit{scores of Constant} for both shoulders, as well as the difference between these two scores. 

All data can be saved by the MD in a *csv* file.

# Note
All the in-depth analysis and conclusions can be found in the final report.
