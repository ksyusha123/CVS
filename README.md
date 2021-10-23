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
	- branch.py  
	- checkout.py  
	- commit.py  
	- init.py  
	- log.py  
	- reset.py  
	- squash.py  
	- status.py  
	- tag.py  
- класс, описывающий репозиторий: repository.py  
- файл, с помощью которого из консоли можно вызывать модули: setup.py  

## Установка    
pip install virtualenv  
virtualenv venv  
venv/bin/activate  
pip install --editable .  

## Использование  
Ввод команд, начиная с cvs.   
 
### Примеры   
- cvs init  
- cvs add file.txt  
- cvs commit -m some_commit_text  
- cvs log  
- cvs reset 4660a5c5d6bc3ea19123157d8e4d582aea8d8637  

### Справка  
cvs --help  
cvs {command} --help  

## Подробности реализации  
Каждая команда представляет собой отдельный модуль, который вызывается из командной строки. 
Все команды собраны в папке commands.  
Чтобы было удобнее работать с путями репозитория, я выделила класс Repository. Его предназначение в том, чтобы управлять путями служебных папок и объектов.  
Также для удобства пользователей применяется библиотека setuptools в связке с click. Click предоставляет удобный интерфейс командной строки, а setuptools и скрипт setup.py позволяют собрать commands в пакет python.  


