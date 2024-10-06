# Api Endpoints

## GET /add-connection
adds connection requested to config.json
```json 
{
    "SSID": "[Wifi Name]",
    "password": "[yourpassword]"
}
```

 ### returns:

success
```json
{
    "error":[empty]
}
```
error
```json
{
    "error":"[error message]"
}
```



## GET /delete-connection
deletes requested connection from config.json
```json 
{
    "SSID": "[Wifi Name]",
    "password": "[yourpassword]"
}
```

 ### returns:

success
```json
{
    "error":[empty]
}
```
error
```json
{
    "error":"[error message]"
}
```