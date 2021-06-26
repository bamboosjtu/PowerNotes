# 环境配置

## 数据库

### MySQL

在Ubuntu 环境下，大致如下

1. 安装：`sudo apt-get install mysql-server`
2. 创建工作目录：`sudo mkdir -p /var/run/mysqld && sudo chown mysql /var/run/mysqld/ && sudo service mysql restart`
3. 初始化（设置密码）：`sudo mysql_secure_installation`
4. 登陆：`sudo mysql -uroot -p`
5. 创建数据库：`CREATE DATABASE <数据库名> CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
6. 创建用户：`CREATE USER '<用户名>'@'%' IDENTIFIED  BY '<密码>';`
7. 配置用户权限：`GRANT ALL PRIVILEGES ON <数据库名>.<表名> TO <用户名>@'%';`
8. 刷新配置：`FLUSH PRIVILEGES;`
9. 修改配置文件（可选）：`/etc/mysql/mysql.conf.d/mysqld.cnf`
10. 安装python包：`pipenv install pymysql && pipenv install cryptography`