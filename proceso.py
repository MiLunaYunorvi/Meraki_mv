import json

class Person():
      def __init__(self,id='',coor=''):
            self.id=id
            self.coor=coor

      def describe(self):
            string=(f'El id de la persona detectada : {self.id}\n'
                  f'Las coordenadas de la persona son : {self.coor}\n')
            print(string)



def muestra(data):
      n=len(data)
      for i in range(0,n):
            print("NÚMERO DE PERSONAS ACTUALMENTE: ",n)
            print("***************DETALLES***************")
            coorde=[data[i]['x0'],data[i]['x1'],data[i]['y0'],data[i]['y1']]
            person_n = Person()
            person_n.id = data[i]['oid']
            person_n.coor = coorde
            person_n.describe()
      
