# a-blog-webapp-based-on-flask
a very fundamental blog webapp based on flask  
  
# 食用说明
  
## 通过**pip install -r requirements.txt** 来安装所需要的包  
  
  
  
## 数据库的**url**在**config.py**中指定  
### url格式
MYSQL：**mysql://username:password@hostname/database**  
SQLite(windows): **sqlite:///c:/absolute/path/to/database**  
SQLite(unix): **sqlite:////absolute/path/to/database**  
### 初始化数据库
使用本菜鸡搞的假迁移（migra.py)
