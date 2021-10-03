# CVS  
Автор: Астахова Ксения  


## Описание  
Локальная система контроля версий, реализованная как консольная утилита.  

## Требования  
- Python версии не ниже 3.8  
- click  
- checksumdir  

## Состав  
- пакет команд: commands/  
	- add.py  
	- commit.py  
	- init.py  
	- log.py  
	- reset.py  
- класс, описывающий репозиторий: Repository.py  
- файл, с помощью которого из консоли можно вызывать модули: setup.py  

## Установка    
pip install virtualenv  
virtualenv venv  
venv/bin/activate  
pip install --editable .  

## Использование  
Из консоли нужно вводить команды, начиная с cvs.   
 
### Примеры   
- cvs init  
- cvs add file.txt  
- cvs commit -m some_commit_text  
- cvs log  
- cvs reset 4660a5c5d6bc3ea19123157d8e4d582aea8d8637  

### Справка  
cvs --help  
cvs {command} --help  

##Подробности реализации  

