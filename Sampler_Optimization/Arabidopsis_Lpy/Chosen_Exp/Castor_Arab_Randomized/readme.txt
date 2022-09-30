-----------------------------------------------------------------------
Instruction for using the point sampler on any virtual L-Py plant model
-----------------------------------------------------------------------

General usage:
-------------

It is assumed that Lpy is already installed in your machine. If not, then follow the installation
guide from this link: https://lpy.readthedocs.io/en/latest/user/installing.html
Or you can simply run the following in the command line:
>> conda create -n lpy openalea.lpy -c fredboudon -c conda-forge
 
Activate the lpy environment in Python. Copy a (working) lpy model file in the current directory. 
Say your lpy model file name is 'mymodel.lpy'. We also need a dictionary that specifies the label
of the organs, which is written in 'labelDictionary.txt' file. The point sampler reads from this
file for the organ labels. An example of the content of the dictionary file is:

{"I": 1, "L": 2, "Flower": 3}

This says that we wish to assign label '1' to module 'I' (which is internode), label '2' to
module 'L' (which is leaf), and label '3' to 'Flower'. However, this will vary from model to model.
You need to modify the dictionary according to the need of the application as well as according
to the model. You can print the actual lstring modules in your lpy model as follows. Copy and paste
the following code snippet after the "module" declarations (or before the "Axiom") in your lpy code
(this is just for printing, do not include this for the point sampling):

def End(lstring, lscene):
  for shape in lscene:
    id = shape.id
    print(lstring[id].name)

If you run your lpy code in the lpy editor, this will print all the lstring modules in the model.
You can create the dictionary accordingly and modify the 'labelDictionary.txt' file.

Actually, a sample dictionary file is already provided by default and it contains many of the common
lstring modules that are typically used in practice. You can have a look and check if the lstring
module(s) you want to label is already included in the dictionary or not. If not, then you can append
the new modules in the dictionary. This is to be noted that the labels will automatically start from
'1', no matter what is the order of the label in the dictionary file. 

Now we are ready to launch the point sampler. The last thing you need to add to the lpy file 
('mymodel.lpy') is to import the 'scan_utils' at the top of the code. This can be done as:

from scan_utils import *

That's all set. Now you can run the point sampler as:

>> python generatePointCloud.py mymodel.lpy labelDictionary.txt 10000

where 'generatePointCloud.py' is the main automating script, and 10000 is the number of points
we wish to sample. The general command format for running the point sampler is the following:

>> python generatePointCloud.py LpyModelFile labelDictionaryFile numberOfPoints

Execution time of the point sampler depends on the complexity of the model and the number of points
to be sampled. Once the sampling process finishes, the sampler produces 3 files as output in the same
directory:


- pointsWithColor.xyz : sampled point cloud along with unique color for each label (this is for
                        visualization purpose). The format of the file is: x y z r g b

- rawPoints.xyz : sampled points without any label. The format of the file is: x y z

- rawLabels.txt : Per point label of the points as in rawPoints.xyz. The format of the file is:
                  labels

You can visualize the labelled color point cloud using viewers such as CloudCompare (recommended),
Meshlab, ParaView, etc.





