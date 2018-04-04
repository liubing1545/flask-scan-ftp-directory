# flask-scan-ftp-directory

## Provides two functions
Use a timer to scan ftp server files    
Provide a restful interface to get ftp files list    

## Note
Celery 4.1.0    
Windows 10 Enterprise 64 bit    
celery -A app.celery worker -l info -P eventlet    
