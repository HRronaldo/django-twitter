#!/usr/bin/env bash
# 说明：第一次vagrant reload --provision，可能会出现一些红色报错，不要担心，它是没有检测到，会随后自动安装；
# 如果vagrant reload --provision有报错情况，请反复多次执行（2-3次）

echo 'Start!'

update-alternatives --install /usr/bin/python python /usr/bin/python3.6 2

cd /vagrant

sudo apt-get update
# sudo apt-get install -y apache2
# if ! [ -L /var/www ]; then
#   rm -rf /var/www
#   ln -fs /vagrant /var/www
# fi

# apt-get install -y git

# if pip | cout \|
# wget https://bootstrap.pypa.io/get-pip.py
# sudo python get-pip.py
sudo apt-get install -y python3-pip
sudo apt-get install -y python-setuptools
sudo ln -s /usr/bin/pip3 /usr/bin/pip

# 升级pip，目前存在问题，read timed out，看脸，有时候可以，但大多时候不行
# python -m pip install --upgrade pip
# 换源完美解决
# 安装pip所需依赖
pip install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install --ignore-installed wrapt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 安装pip最新版
pip install -U pip -i https://pypi.tuna.tsinghua.edu.cn/simple

# 默认安装Django最新版
pip install django -i https://pypi.tuna.tsinghua.edu.cn/simple
# 安装Django restframework
pip install djangorestframework -i https://pypi.tuna.tsinghua.edu.cn/simple

sudo apt-get install tree

# 安装配置mysql8
if ! [ -e /vagrant/mysql-apt-config_0.8.15-1_all.deb ]; then
	wget -c https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb
fi

sudo dpkg -i mysql-apt-config_0.8.15-1_all.deb

sudo apt-get update

sudo DEBIAN_FRONTEND=noninteractivate apt-get install -y mysql-server
sudo apt-get install -y libmysqlclient-dev
pip install mysqlclient


# if ! sudo mysql -u root show datahases; | cut -d \| -f 1 | grep -w twitter; then
sudo mysql -u root << EOF
	ALTER USER 'root'@'localhost' IDENTIFIED BY '*{password}*';
	show databases;
	CREATE DATABASE twitter;
EOF
# fi


# 修改mysql密码&创建database
# 设置密码为password
# ALTER USER 'root'@'localhost' IDENTIFIED BY '*{password}*';	 
# 创建名为twitter的数据库
# CRESTE DATABASE twitter;


echo 'All Done!'
