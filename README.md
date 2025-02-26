# Research-Department

How do I make this work?
Firstly you need to go to Google Cloud Console to create a API key, then you need to download the Credentials.json and paste it in main. After that you need to create config.py
with the following content:
```
Return = {
    "Token"PASTE YOUR TOKEN HERE"
    "Guild": 1343641690472185888,
    "Test-Log-Channel": 1343641691399389278,
    "Rolebinds": {
        "Director": [1343641756574416980]  
    },
    "CommandPermissions": {
        "add-points": [1343641756574416980],
        "my-points": [1343641756574416980],
        "remove-points": [1343641756574416980],
        "update": [1343641756574416980],
        "host": [1343641756574416980]
    },
    "Access Levels": {
        "Level 0": [1343641756574416980],
        "Level 1": [1343641756574416980],
        "Level 2": [1343641756574416980],
        "Level 3": [1343641756574416980],
        "Level 4": [1343641756574416980],
        "Level 5": [1343641756574416980],
        "OMNI": [1343641756574416980]
    },
    "Documents": {}
}```

Then you need to create .env file, this file needs the following:
--> .Token
--> .
