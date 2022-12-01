# ROMI_3D_Growth_Modeling

## 1 Introduction 

Plants are complex dynamical systems, i.e. systems that can be described by a state and its change over time. In classical dynamical systems, the system’s state is usually represented as a vector in Rn , for n fixed. The change in the system’s state is modeled by an evolution equation, often defined as a  differential equation, that makes it possible to compute the system’s state at time t+dt knowing the  system’s state at time t. Knowing the state, or an estimation of the state at a date t, it is thus possible to predict the system’s state in the future. 
Procedural methods such as L-systems (Prunsinkiewicz, et al. 1996, Boudon, et al. 2012), are adequate for simulating plant growth starting from an initial state corresponding to a plant seed. But, as of today, they cannot easily be used to predict the development of a phenotyped plant. This is mainly due to the fact that producing a detailed L-string (formal string representing the state of the plant at a given date  in the L-system formalism) corresponding exactly to the phenotyped architecture is still mostly out of  reach at such a detailed level in the phenotyping community.
Thanks to the rapid progress in plant phenotyping, it is now possible to acquire data about plant architecture. Although this data can be quite detailed (in the form of high resolution point clouds for example), it is not yet possible to have detailed information about the plant architecture in the format of L-systems that could be used to predict the evolution of the state of the plant. Alternatively, we propose to rely on data driven methods which predict the next state using techniques such as machine learning. Recent Machine learning approaches used for plant growth modeling are mostly focused on  using 2D data such as images as input (Sakurai et al. 2019), (Yasrab et al. 2021). In this work, we aim at taking advantage of 3D data as input to better extract the geometric information of the data. In our case, we have decided to use 3D point clouds as input due to their relatively low computational cost and high resolution (compared to other forms of 3D data). 
In our application, the network takes as input the current point cloud and will output the future point cloud. Among the tasks related to point clouds which have been already investigated, the task of point cloud completion is well-suited as a starting point for this research since similar to the case at hand, it takes as input the partial point cloud of an object and outputs the complete point cloud. Numerous models have been designed to perform the task of point cloud completion. In this work, we focus on PoinTr (Yu et al., 2021), which takes inspiration from the well-known Transformer (Vaswani et al., 2017) architecture and introduces geometry aware transformers which are adapted to take 3D point clouds as input. PoinTr has been previously trained on the shapeNet, PCN and KITTI datasets which contain big objects such as cars, airplanes etc. Our goal is to investigate its potential for being used on plant data.  
 2 Methods 
The structure of PoinTr can be seen in Fig 1. The input point cloud is first converted into a set of feature vectors, named point proxies, that represent the local regions in the point clouds. To do so, Furthest Point Sampling (FPS) (Eldar et al., 1997) is conducted to locate a fixed number of point centers in the partial point cloud. Then, to extract the local and global information of the points and the center points two different ANNs (Artificial Neural Network) are used. The sum of the output of these two networks is the point proxy. 



![alt text](https://github.com/Mona-ShZeinoddin/ROMI_3D_Growth_Modeling/blob/main/Results.png)
 

Figure 1:The Pipeline of PoinTr. The input partial point cloud is first downsampled to obtain the center points. Then, to extract the local and global information of the points and the proxies two different ANNs are used, the sum of the output of the two networks is fed into the geometry-aware transformer. A transformer architecture is utilized to predict the point proxies for the missing parts. A simple ANN is used at the end to complete the point cloud based on the predicted point proxies in a coarse-to-fine manner. 
The point proxy is then given to the geometry-aware transformer block inspired by the well-known  Transformer architecture. This Transformer is an encoder-decoder structure which utilizes the attention (Eldar et al., 1997) mechanism, a mechanism designed to improve the performance of encoder-decoder models by determining the parts of the input that contribute most to making a correct output and give more weight to them. At the output of the geometry-aware transformer, the predicted point proxies are fed into another ANN with the aim of recovering the detailed local shapes centered at the predicted proxies. 
The PoinTr structure has been trained on datasets such as ShapeNet, PCN and KITTI and has proven to be well suited for completing point clouds of big objects without too many subtle details. The goal of this work is to put PoinTr to the test. First, the network is trained and tested on a stochastic model of a simple random growing stem. Second, the network is trained and tested on a dataset of the Arabidopsis plant, which is partly random and can be seen as a medium case between the highly stochastic stem and the more regular shape, that is the airplane, in Figure 2. 
3 Results 
In order to test PoinTr, two datasets have been developed using L-Py and then sampled following the method introduced by (Chaudhury et al., 2020) to produce their corresponding point clouds. One includes point clouds of a growing stem, in two different stages of growth consisting of 100 pairs of point clouds, in which the partial point clouds have 10000 points and the complete point clouds have 15000 points. The second dataset consists of the point clouds of one single Arabidopsis where for each partial point cloud, a random group of neighboring points have been removed from the original point cloud. The training set contains 1800 samples, each containing between 700 and 1200 points, and the test and validation test each contain 200 point clouds composed of 1000 points. The complete point clouds have 15000 points. The growing stem dataset represents a fully random dataset and the Arabidopsis dataset represents a more botanically oriented dataset with less variations (since all of the inputs belong to one unique Arabidopsis plant). In doing these basic experiments, our aim is to demonstrate the potential of using PoinTr for plant growth modeling and to come up with a strategy for making PoinTr more adaptable to plants and improve its performance. 



![alt text](https://github.com/Mona-ShZeinoddin/ROMI_3D_Growth_Modeling/blob/main/PoinTr_Review.png)


Figure 2: Results of PoinTr- Partial inputs (Green), Predicted outputs (Red) and Groundtruths (Blue) - First row: Testing a pretrained PoinTr network on the PCN dataset, CDL1 (chamfer distance L1) = 0.007263, CDL2 (chamfer distance L2) = 0.000227- Second row: Fientuning the pretrained PoinTr on the Stem dataset for 300 epochs, CDL1= 0.04, CDL2 = 0.0138 - Third row: Fientuning the pretrained PoinTr on the Arabidopsis dataset for 700 epochs, CDL1 = 0.003596, CDL2 = 0.000051 
Between the Arabidopsis and the Stem models, the Arabidopsis model has outperformed the Stem model by far and its performance is even better than the PoinTr tested on the PCN dataset. This was already expected since the Arabidopsis dataset contains only a single plant. Yet still, this shows that with the right amount of data and suitable amount of training, the model is able to perform point cloud completion quite well. In the case of the Stem dataset, the results show that the model is capable of predicting the part intersecting with the partial input very well but cannot predict any more than that (the outliers can be seen in Fig2.) 
4 Discussion 
Based on our first results, PoinTr shows promising performance to do 3D plant growth modeling. There are quite a number of ways to continue to improve PoinTr. First, we will enlarge the datasets and experiment with bigger datasets. Second, we will try out the model with a dataset composed of detailed stochastic plants (e.g., an Arabidopsis which has random angles and random internode length). Third, we would like to investigate the effect of having different numbers of points in the input partial point cloud (like the difference between the Arabidopsis and the Stem dataset) and finally, in order to approach our long-term goal which is plant growth modeling, we will extend our point cloud completion model and construct a dataset of detailed plants in different stages of growth and try to perform prediction.



