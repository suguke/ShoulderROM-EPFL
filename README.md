# Shoulder Range of Motion Evaluation
EPFL - Biomechanics of the musculo-skeletal system project

# Abstract


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
