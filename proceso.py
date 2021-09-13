import json

class Person():
      def __init__(self,id='',coor=''):
            self.id=id
            self.coor=coor

      def describe(self):
            string=(f'El id de la persona detectada : {self.id}\n'
                  f'Las coordenadas de la persona son : {self.coor}\n')
            print(string)

def cont(data):
      return(len(data))

def muestra(n, data):
      for i in range(0,n+1):
            person_n = Person()
            person_n.id = data[i]['oid']
            person_n.describe()
