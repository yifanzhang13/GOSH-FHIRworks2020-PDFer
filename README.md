# Deployment Guide

## Install Visual Studio Code

- Download and install [Visual Studio Code](https://code.visualstudio.com/)

## Install .NET Core 2.1

- Download and install .NET Core 2.1 [SDK 2.1.803](https://dotnet.microsoft.com/download/dotnet-core/2.1)
- Test your installation by opening a new terminal and running the following command:

    ```bash
    dotnet
    ```
    
## Install PyFPDF library

- Install the python library by using Pipe:
	- `python -m pip install fpdf`
- Check [PyFPDF](https://pyfpdf.readthedocs.io/en/latest/#installation) which provides other ways to install the library

# Running the app

- Clone the project and open it in Visual Studio Code.
- Navigate to the directory **dotnet-azure-fhir-web-api** using the terminal inside Visual Studio Code.
- In the terminal, run the following command:

    ```bash
    dotnet run
    ```
- Open a web browser and navigate to [https://localhost:5001/api/Patient/](https://localhost:5001/api/Patient/) to view a list of all patients.


## List of API endpoints

#### Generate and view a patient's PDF file

- Find a patient ID: `/api/Patient/`
	- ![Find a patient ID](/Users/yifancheung/Desktop/Systems Engineering /Legal_Implementation/GOSH-FHIRworks2020-pdfGenerator/screenshots/Screen Shot 2020-03-17 at 11.41.08 PM.png) 
- Generate PDF file: `/api/Patient/patient ID`
	- ![Generate PDF file](/Users/yifancheung/Desktop/Systems Engineering /Legal_Implementation/GOSH-FHIRworks2020-pdfGenerator/screenshots/Screen Shot 2020-03-17 at 11.43.36 PM.png) 
- View the PDF file: `/api/Patient/patient ID/view`
	- ![View the PDF file](/Users/yifancheung/Desktop/Systems Engineering /Legal_Implementation/GOSH-FHIRworks2020-pdfGenerator/screenshots/Screen Shot 2020-03-17 at 11.44.55 PM.png) 

#### Generate and view an Observation PDF file

- Find an observation ID from the list of observations of a patient: `/api/Observation/patient ID`
	- ![Find an observation ID](/Users/yifancheung/Desktop/Systems Engineering /Legal_Implementation/GOSH-FHIRworks2020-pdfGenerator/screenshots/Screen Shot 2020-03-17 at 11.33.05 PM.png) 
- Generate PDF file: `api/Observation/single/ observation ID`
	- ![Generate PDF](/Users/yifancheung/Desktop/Systems Engineering /Legal_Implementation/GOSH-FHIRworks2020-pdfGenerator/screenshots/Screen Shot 2020-03-17 at 11.35.39 PM.png) 
- View the PDF file: `api/Observation/single/ observation ID/view`
	- ![Observation PDF](/Users/yifancheung/Desktop/Systems Engineering /Legal_Implementation/GOSH-FHIRworks2020-pdfGenerator/screenshots/Screen Shot 2020-03-17 at 11.36.59 PM.png) 

#### Patients

- GET all patients: **/api/Patient**
- GET a patient: **/api/Patient/** *patient ID*
- GET a selected number of pages of patient: **api/pages/** *number of pages*


#### Observations

- GET all observations for a patient: **/api/Observation/** *patient ID*
- GET a single observation for a patient: **api/Observation/single/** *observation ID*
- GET a selected number of pages of observations for a patient: **api/Observation/pages/** *number of pages/patient ID*
