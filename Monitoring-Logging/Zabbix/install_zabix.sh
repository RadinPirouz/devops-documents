#!bin/bash 

DISTRO=$(lsb_release -is)
if [ "$DISTRO" != "Ubuntu" ]; then
    echo "This script is designed for Ubuntu. Exiting..."
    exit 1
fi



#update package list and upgrade them 

sudo apt update && sudo apt upgrade -y 

#install prerequisite packeges 

sudo apt install wget gnupg lsb-release -y 

#Add zabix repo 

wget https://repo.zabbix.com/zabbix/6.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.4-1+ubuntu$(lsb_release -sc)_all.deb

sudo dpkg -i zabbix-release_6.4-1+${(lsb_release -sc)_all.deb

sudo apt update 

#install zabix server-mysql 
sudo apt install zabbix-server-mysql zabbix-frontend-php zabbix-apache-conf zabbix-sql-scripts zabbix-agent -y

#install mysql and configure it 

sudo apt install mysql-server -y 
sudo systemctl start mysql 
sudo systemctl enable mysql 

# creating database 

echo "please enter a password for zabix"
read -s ZABBIX_DB_PASS
mysql -uroot -p -e "create database zabbix character set utf8 collate utf8_bin;"
mysql -uroot -p -e "create user zabbix@localhost identified by '$ZABBIX_DB_PASS';"
mysql -uroot -p -e "grant all privileges on zabbix.* to zabbix@localhost;"
zcat /usr/share/doc/zabbix-sql-scripts/mysql/create.sql.gz | mysql -uzabbix -p$ZABBIX_DB_PASS zabbix

#update pass 

sudo sed -i "s/# DBPassword=/DBPassword=$ZABBIX_DB_PASS/" /etc/zabbix/zabbix_server.conf

# Start Zabbix server and agent processes
sudo systemctl restart zabbix-server zabbix-agent apache2
sudo systemctl enable zabbix-server zabbix-agent apache2


echo "done!,installation complated!"
