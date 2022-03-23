# Exordle Deployment

## Installation
```
git clone git@github.com:YoussefElshemi/Exordle.git
```

Once installed, you can navigate to the Exordle folder by using the following command:
```
cd ./Exordle
```

We will need to install all dependencies for this project by doing
```
python -m pip install -r requirements.txt
```

## Microsoft Login
Next, we register an Azure application by clicking [here](https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade). 
It should be set up to be a single tenant, with these three redirect URLs:

 - <DOMAIN>/microsoft/auth-callback
 - <DOMAIN>/microsoft/from-auth-callback
 - <DOMAIN>/microsoft/to-auth-callback

Create a .env file inside the exordle folder by navigating using
```
cd ./src/exordle
nano .env
```

The contents of this .env file should be as followed:
```
SECRET_KEY=<DJANGO SECRET KEY>
MICROSOFT_AUTH_CLIENT_SECRET=<CLIENT SECRET>
```

`MICROSOFT_AUTH_CLIENT_SECRET` can be obtained from the Azure application, the client and tenant ID also need to be stored in the settings.py file in the same directory.

After we will edit the settings file using the below command
```
nano settings.py
```

Here we will also change `MICROSOFT_AUTH_CLIENT_ID` and `MICROSOFT_AUTH_TENANT_ID` to their corresponding values from the Azure application.

## Running
First navigate to your admin panel, here we need to change the "Sites" table and replace example.com in both fields with the correct new domain, eg. `localhost:8000` if you are hosting locally.

Next, we need to populate our locations table, this will store all of the locations on campus which can be assosicated to words.

After locations are added, you can begin to add entries to the Words table, these should be words you want the user to guess.