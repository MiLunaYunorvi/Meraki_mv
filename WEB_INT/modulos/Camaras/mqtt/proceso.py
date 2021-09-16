import json

class Person():
      def __init__(self,id='',coor=''):
            self.id=id
            self.coor=coor

      def describe(self):
            string=(f'El id de la persona detectada : {self.id}\n'
                  f'Las coordenadas de la persona son : {self.coor}\n')
            print(string)



def muestra_general(data):
      n=len(data)
      print("NÚMERO DE PERSONAS ACTUALMENTE: ",n)
      print("***************DETALLES***************")
      for i in range(0,n):
            coorde=[data[i]['x0'],data[i]['x1'],data[i]['y0'],data[i]['y1']]
            person_n = Person()
            person_n.id = data[i]['oid']
            person_n.coor = coorde
            person_n.describe()
      
def muestra_caja(mensaje):
      print(mensaje)
      n=mensaje['person']
      print("NÚMERO DE PERSONAS ACTUALMENTE: ",n)
      print("***************DETALLES***************")

def muestra_cola(mensaje):
      print(mensaje)
      n=mensaje['person']
      print("NÚMERO DE PERSONAS ACTUALMENTE: ",n)
      print("***************DETALLES***************")
