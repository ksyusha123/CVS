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
1.	pip install virtualenv  
2.	virtualenv venv  
3.  venv/bin/activate  
4.  pip install --editable .  

## Использование  
Из консоли нужно вводить команды  
 
###Примеры   
- init  
- add file.txt  
- commit -m some_commit_text  
- log  
- creset 4660a5c5d6bc3ea19123157d8e4d582aea8d8637  

##Подробности реализации  

