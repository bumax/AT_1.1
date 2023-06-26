from datetime import datetime
import sys, getopt

class Note():
    def __init__(self, id, title, data, date):
        self.__id = id
        self.__title = title
        self.__data = data
        self.__date = date
    def getID(self):
        return self.__id
    def print(self):
        print(f"Заметка № {self.__id} от {self.__date}: \'{self.__title}\' - {self.__data}" )
    def formatToCSV(self):
        return f"{self.__id};{self.__title};{self.__data};{self.__date}\n"
    def isContainText(self, text):
        return text.lower() in self.__title.lower() 
    def edit(self, title, data):
        if((self.__title != title and title != '') or (self.__data != data and data != '')):
            if title != '':
                self.__title = title
            if data != '':
                self.__data = data
            self.__date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class DataBase():
    def __init__(self, filename):
        self.__maxID = 0
        self.__filename = filename
        self.__DB = {}
        self.CSVreader()
    def CSVreader(self):
        f = open(self.__filename, "r", encoding='utf8')
        for readData in f:
            if len(readData) > 1:
                noteData = readData.replace("\n","").split(";")
                self.__DB[noteData[0]] = Note(noteData[0], noteData[1], noteData[2], noteData[3])
                if int(noteData[0]) > self.__maxID:
                    self.__maxID = int(noteData[0])
        f.close()
    def CSVwrite(self):
        f = open(self.__filename, "w", encoding='utf8')
        for key in self.__DB:
            f.write(self.__DB[key].formatToCSV())
        f.close()
    def search(self, text):
        result = []
        for key in self.__DB:
            if self.__DB[key].isContainText(text):
                result.append(self.__DB[key].getID())
        if len(result) == 0:
            print ("Ничего не найдено")
        else:
            for index in result:
                self.__DB[index].print()
    def printAll(self):
        for key in self.__DB:
            self.__DB[key].print()
    def edit(self, id, title, data):
        if id in self.__DB:
            self.__DB[id].edit(title, data)
            self.CSVwrite() 
        else:
            print("ошибка, данная записка не найдена!")
    def add(self, title, data):
        if(title != '' and data != ''):
            self.__maxID = self.__maxID + 1
            self.__DB[self.__maxID] = Note(self.__maxID, title, data, datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
            self.CSVwrite()
        else:
            print("ошибка, заголовок и данные не должны быть пустыми!")
    def delete(self, id):
        if id in self.__DB:
            self.__DB.pop(id)
            self.CSVwrite()    
        else:
            print("ошибка, данная записка не найдена!")


def main(argv):
    optlist, args = getopt.getopt(argv, 'f:ps:ae:h:d:r:')
    database = DataBase(getArgVal(optlist, '-f'))
    if checkArg(optlist, '-p'):
        database.printAll()
    elif checkArg(optlist, '-a'):
        database.add(getArgVal(optlist, '-h'), getArgVal(optlist, '-d'))
    elif checkArg(optlist, '-s'):
        database.search(getArgVal(optlist, '-s'))
    elif checkArg(optlist, '-e'):
        database.edit(getArgVal(optlist, '-e'), getArgVal(optlist, '-h'), getArgVal(optlist, '-d'))
    elif checkArg(optlist, '-r'):
        database.delete(getArgVal(optlist, '-r'))
def checkArg(olist, arg):
    retVal = False
    for o, a in olist:
        if o == arg:
            retVal = True
    return retVal
def getArgVal(olist, arg):
    retVal = ''
    for o, a in olist:
        if o == arg:
            retVal = a
    return retVal

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(  '''Cинтаксис: 
-f [filename] - имя CSV файла с базой данных
-p - вывод на экран всех записок
-s [text] - поиск по заголовку записки
-a - добавить новую записку
-e [id] - редактировать записку с номером id
-h [text] - новый заголовок редактируемой записки
-d [text] - новое содержимое редактируемой записки
-r [id] - удалить записку
--------
Примеры:
notes.py -f data.csv -p
notes.py -f data.csv -a -h "Zagolovok 9" -d "Text 9"
notes.py -f data.csv -s 'заголовок 1'
notes.py -f data.csv -e 4 -h "Zagolovok 4" -d "Text 4"
notes.py -f data.csv -r 9''')
    else:
        main(sys.argv[1:])