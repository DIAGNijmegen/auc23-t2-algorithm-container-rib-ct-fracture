# AUC23 Baseline Algorithm Submission

This codebase contains an example submission for the [Automated Universal Classification challenge](https://auc23.grand-challenge.org/) (AUC23). It implements the [AUC23 baseline algorithm](https://github.com/DIAGNijmegen/universal-classifier-t9603). You can use this repo as a template for submitting to AUC23. 

If something does not work for you, please do not hesitate to contact us through a post in the forum on [https://auc23.grand-challenge.org/](https://auc23.grand-challenge.org/).

## Table of Contents
* [Prerequisites](#prerequisites)
* [Creating an Algorithm on grand-challenge.org](#creating)
* [Linking your repository to your Algorithm](#linking)
* [Submitting](#submitting) 
* [implement your own algorithm](#implementing) 

<a id="prerequisites"></a>
## Prerequisites
- Have an account on grand-challenge.org and make sure that you are a [verified user](https://grand-challenge.org/documentation/account-verification/) there.
- Have this repository forked or cloned and uploaded to a GitHub repository on your own GitHub account.
- Have created a python package in the form of a `.whl` file that implements a function `predict()`. This function should, given a trained model for a task at hand and input medical image(s), classify those medical image(s) accordingly. This repository already contains a `.whl` file, containing the [AUC23 baseline]((https://github.com/DIAGNijmegen/universal-classifier-t9603)). For specifiics about the expected usage of the `predict` function and for instructions on how to create a `.whl` file yourself, you can follow the tutorial in  the [AUC23 baseline algorithm repo](https://github.com/DIAGNijmegen/universal-classifier-t9603).
- Have a folder containing a model artifact in the format that your python package (`.whl` file) expects. The model artifact folder should contain all task-specific information, such as model weights, that your inference codebase needs to produce its output from the input medical image(s). The `./artifact/` directory in this repository already contains a trained baseline model for the task at hand. For more information about the baseline model, and for information on how to generate your own model artifact, follow the tutorial in the [AUC23 baseline algorithm repo](https://github.com/DIAGNijmegen/universal-classifier-t9603).

<a id="creating"></a>
## Creating an Algorithm on grand-challenge.org
Start by creating an Algorithm on grand-challenge.org. AUC23 has separate leaderboards for each of its classification tasks. You will need to create separate Algorithms for each of the tasks.

You can create an Algorithm by following [this link](https://grand-challenge.org/algorithms/create/). Some important fields are:
   * Please choose a `Title` and `Description` for your algorithm;
   * Select a logo to represent your algorithm (preferably square image);
   * Consult `task_config.json` for the `Inputs` and `Outputs`. Please select the `Inputs` and `Outputs` depending on the classification task for which you are creating your Algorithm:
   
| Task                                      | Input                                                                 | Output                                         |
|-------------------------------------------|----------------------------------------------------------------------|---------------------------------------------   |
| Lung - CT - COVID-19                      | `CT Image`, `Lobe and COVID-19 lesion segmentation`                  | `Probability COVID-19`, `Probability Severe COVID-19` |
| Rib - CT - Fracture                       | `Rib fracture segmentation`, `CT Image`                              | `Fracture type`                                 |
| Lung nodule - CT - False positive reduction | `CT Image`                                                          | `Lung nodule malignancy risk`                 |
| Brain - MRI - Glioma                      | `T1 Brain MRI`, `T1GD Brain MRI`, `T2 Brain MRI`, `FLAIR Brain MRI` | `WHO grade probabilities`                      |
| Breast - MRI - Molecular cancer type      | `T1 subtraction MRI`                                                | `Breast cancer molecular subtype probabilities` |
| Retina - OCT - Glaucoma                   | `Optical coherence tomography image (OCT)`                           | `Probability POAG`                             |
| Prostate - MRI - Clinically significant cancer | `Transverse T2 Prostate MRI`, `Transverse HBV Prostate MRI`, `Transverse ADC Prostate MRI` | `Case-level Cancer Likelihood Prostate MRI`   |
| Kidney - CT - Abnormality                 | `CT Image`                                                           | `Probability kidney abnormality`               |

   * Choose `Viewer CIRRUS Core (Public)` as a `Workstation`;
   * At the bottom of the page, indicate that you would like your Docker image to use GPU and how much memory it needs.
After filling in the form, click the "Save" button at the bottom of the page to create your Algorithm.   

<a id="linking"></a>
## Linking a GitHub repo to your Algorithm 
Your Algorithm is now ready to be linked to this codebase.

### Linking a GitHub repo
The preferred way to link your Algorithm to this codebase, is by directly linking this GitHub repo. Once your repo is linked, grand-challenge.org will automatically build the docker image for you, and add the updated container to your Algorithm.
* First, click "Link Github Repo". You will then see a dropdown box, where your Github repo is listed only if it has the Grand-Challenge app already installed. Usually this is not the case to begin with, so you should click on "link a new Github Repo". This will guide you through the installation of the Grand-challenge app in your repository.
* After the installation of the app in your repository is complete you should be automatically returned to the Grand Challenge page, where you will find your repository now in the dropdown list (In the case you are not automatically returned to the same page you can [find your algorithm](https://grand-challenge.org/algorithms/) and click "Link Github Repo" again). Select your repository from the dropdown list and click "Save". 
* Finally, you need to tag your repository, this will trigger Grand-Challenge to start building the docker container. Note: If want to update your Algorithm after you have made changes to your repository, just tag your repository again, and Grand-Challenge will start building the new docker container.

### Make sure your container is Active 
Please note that it can take a while until the container becomes active (The status will change from "Ready: False" to "Active") after linking your Github repo. Check back later or refresh the URL after some time. 

<a id="submitting"></a>
## Submitting
You are now ready to submit to the corresponding Leaderboard. On https://auc23.grand-challenge.org/, navigate to the "Submit" tab. Navigate to the tab that corresponds to the task to which you want to submit your Algorithm, and select your Algorithm from the drop down list.

Note that, depending on the availability of compute nodes on grand-challenge.org, it may take some time before the evaluation of your Algorithm finishes and its results can be found on the Leaderboard.

Note: If have made changes to your Algorithm, and updated your Algorithm as described in [Linking a GitHub repo](#linking), you will still have to re-submit your Algorithm to have the changes of your method be reflected in the Leaderboard.

<a id="implementing"></a>
## Implementing your own algorithm
This repository mainly consists of code that allows your code to run in the grand-challenge ecosystem. The only two parts that need to be edited to implement your own algorithm into this codebase are the inference code and the trained model needed to run your algorithm.
### Inference code
The inference codebase is packaged in the `.whl` file in `/vendor`. This python package contains all task-agnostic code that your algorithm needs to run inference. 

To implement your own algorithm, replace the `.whl` file with one that contains inference code of your own algorithm. See the [AUC23 baseline algorithm repo](https://github.com/DIAGNijmegen/universal-classifier-t9603) for how to create a `.whl` for your own codebase. As also detailed in that repository, your algorithm should implement a `predict()` function that runs your algorithm on input images. This function should expect as arguments paths to the input images, as well as a path to your trained model, i.e. the weights and data that your algorithm additionally needs to produce its output. This is described in more detail in the [AUC23 baseline algorithm repo](https://github.com/DIAGNijmegen/universal-classifier-t9603).

If you use a `.whl` file with a different name, make sure to update the package name in `requirements.txt` as well.

### Trained model
The trained model is stored in the `./artifact` folder. This folder contains all task-specific information, such as model weights, that your inference codebase needs to produce its output from the input 3D medical image(s). 

How you want to structure the `./artifact` is completely up to you. Do note that this directory may only contain data that your training codebase fully automatically generates from the tasks training dataset during the training process. For an example training codebase, see the [AUC23 baseline algorithm repo](https://github.com/DIAGNijmegen/universal-classifier-t9603).
