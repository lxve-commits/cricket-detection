# cricket-detection
With this code, I train the Detectron2 image recognition neural network to also recognize crickets.
I started of by simply training the network in Google Colab. That was already a pretty big challange for me as I had to read the whole documentation
and learn about image recognition in general. After I had figured out how to train the network with computer generated data, I added more examples to the training
and created a functioning version. 

As the startup I worked for wanted a solution where video footage would automatically be evaluated on the cloud, I taught myself how to dockerize my code together with the neural network. Then I created an AWS bucket where new video footage would be uploaded. I then pushed my docker image to AWS and created a Lambda function
to run the neural network whenever a new video was uploaded. The recognition data would then be submitted to a data repository. 
