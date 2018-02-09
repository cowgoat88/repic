# Installing MySQL locally
ASSUMING YOUR VIRTUALENV IS RUNNING
1. brew install mysql 
2. brew install openssl
3. add this to ~/.bash_profile:
  `export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/`
  
  ```nano ~/.bash_profile
  export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/opt/openssl/lib/
  
  write the file with ctl o
  exit with ctl x```
  
4. source ~/.bash_profile
5. create root user:
  mysqladmin -u root password {yourpasswordhere}
6. start the mysql local instance:
  brew services start mysql
7. (optional) log on to local mysql 
  mysql -u root -p
  {type your password on the next line}
8. Install the django mysqlclient
  `pip install mysqlclient`
9. Update your settings file to connect to your local db