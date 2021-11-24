import asyncio
from binance import AsyncClient, BinanceSocketManager
from binance.enums import FuturesType
import time, json, pprint
import psycopg2
import os

class shot():
    def __init__(self,price_st,t_st,rzn):
        self.price_st = price_st
        self.t_st = t_st
        self.data = []
        self.rzn = rzn
    def print(self):
        print(self.rzn)
class settings():
        Distance = []
        x = 0.15
        while x < 1.01:
            Distance.append(round(x,2))
            x +=0.05
        while x < 5.01:
            Distance.append(round(x,2))
            x +=0.6
        TakeProfit = []
        x = 0.15
        while x < 1.01:
            TakeProfit.append(round(x,2))
            x += 0.1
        while x < 5.01:
            Distance.append(round(x,2))
            x +=0.4
        StopLos = []
        x = 0.2
        while x < 0.81:
            StopLos.append(round(x,2))
            x += 0.1
class BOT():
    def __init__(self,name) -> None:
        self.listing_to_data = False
        self.name = name
        self.data = []
        self.first_data = 0
        self.ban_time = []
        
    def send_data(self,data):
        self.data.append(data)
        
    def modify_data(self):
        
        new_data = []
        for i in range(1,len(self.data)-1):
            
            
            if self.data[i]['p'] == self.data[i-1]['p'] and self.data[i]['T']==self.data[i-1]['T']:
                continue
            new_data.append(self.data[i])
        self.data = new_data

        
    def send_post_data(self,data):
        self.post_data.append(data)
    def clear_data(self):
    	self.data.clear()
    def clear_used_distance(self):
    	self.used_distance.clear()
    def clear_post_data(self):
    	self.post_data.clear()
    def get_name(self):
        return self.name
    def first_time(self):
        return self.first_data['T']
    def set_listing_to_data(self):
        self.listing_to_data = True
    def unset_listing_to_data(self):
        self.listing_to_data = True
    def get_shots(self):
        self.modify_data()

        try:
            db = psycopg2.connect(user="postgres",
                                        # пароль, который указали при установке PostgreSQL

                                        password="qazWqwpo1",
                                        host="80.89.238.221",#
                                        port="5432",
                                        database="websockets_data")#
            cursor = db.cursor()
            query = ''
            """ with open('test.txt','a') as fi:
                for data in self.data:
                    fi.write(f"{data}\n") """
            used_t = []
            shots =[]
            first_i = 0
            last_i = 1
            ban_distance = []


            for i in range(1,len(self.data)-1):
                if self.data[i-1]['T'] == self.data[i]['T'] and not(self.data[i]['T'] in used_t):
                    used_t.append(self.data[i]['T'])
                    first_p = self.data[i-1]['p']
                    first_t = self.data[i-1]['T']
                    first_i = i-1
                    
                    
                    
                elif self.data[i]['T'] in used_t and self.data[i+1]['T'] != self.data[i]['T']:
                    last_i = i
                    x = round(float(self.data[i]['p'])/(float(first_p)/100)-100,3)
                    if x > 0.15 or x < -0.15:
                        print(f"Shot!  {x}    {self.name} TIME: {self.data[i]['T']}")
                        
                        
                    
                    for distance in settings.Distance:
                        
                        if round(float(self.data[i]['p'])/(float(first_p)/100)-100,3) > distance and (distance not in ban_distance):
                            print(i,round(float(self.data[i]['p'])/(float(first_p)/100)-100,3),float(first_p),distance)
                            ban_distance.append(distance)
                            print(ban_distance)

                            for tp in settings.TakeProfit:
                                
                                
                                for sl in settings.StopLos:
                                    
                                    operator = 'None'
                                    start = 0
                                    start_i = 1
                                    change = 0
                                    time_of = 0
                                    for j in range(first_i,last_i+1):
                                        if round(float(self.data[j]['p'])/(float(first_p)/100)-100,3) > distance:
                                            start = self.data[j]
                                            start_i = j
                                            break
                                        else:
                                            pass
                                    if start != 0:
                                        for k in range(start_i+1,len(self.data)):
                                            if round(float(self.data[k]['p'])/(float(start['p'])/100)-100,3) > sl:
                                                operator = 'sl'
                                                time_of = self.data[k]['T']
                                                
                                                break
                                            elif round(float(self.data[k]['p'])/(float(start['p'])/100)-100,3) < -tp:
                                                operator = 'tp'
                                                time_of = self.data[k]['T']
                                                
                                                
                                                break
                                            
                                        if operator == 'None':
                                            
                                            change = round(float(self.data[k-1]['p'])/(float(start['p'])/100)-100,3)
                                            time_of = self.data[k]['T']
                                        query = f""" INSERT INTO data(coin,tp_or_sl,change,tp,sl,distance,type_of_,time) VALUES ('{self.name}','{operator}',{change},{tp},{sl},{distance},'{'sell'}',{time_of})
                                                """
                                        cursor.execute(query)
                                            
                                        db.commit()
                                        used_t.clear()


                        elif round(float(self.data[i]['p'])/(float(first_p)/100)-100,3) < -distance and (distance not in ban_distance):
                            print(i,round(float(self.data[i]['p'])/(float(first_p)/100)-100,3),float(first_p),distance)
                            ban_distance.append(distance)
                            for tp in settings.TakeProfit:
                                
                                
                                for sl in settings.StopLos:
                                    
                                    operator = 'None'
                                    start = 0
                                    start_i = 1
                                    change = 0
                                    time_of = 0
                                    for k in range(first_i,last_i+1):
                                        if round(float(self.data[k]['p'])/(float(first_p)/100)-100,3) < -distance:
                                            start = self.data[k]
                                            start_i = i
                                            break
                                        else:
                                            pass
                                    if start != 0:
                                        
                                        for j in range(start_i+1,len(self.data)):
                                            if round(float(self.data[j]['p'])/(float(start['p'])/100)-100,3) < -sl:
                                                operator = 'sl'
                                                time_of = self.data[j]['T']
                                                
                                                break
                                            elif round(float(self.data[j]['p'])/(float(start['p'])/100)-100,3) > tp:
                                                operator = 'tp'
                                                time_of = self.data[j]['T']
                                                
                                                break
                                            
                                        if operator == 'None':
                                            
                                            change = round(float(self.data[i-1]['p'])/(float(start['p'])/100)-100,2)
                                            time_of = self.data[i]['T']
                                        query = f""" INSERT INTO data(coin,tp_or_sl,change,tp,sl,distance,type_of_,time) VALUES ('{self.name}','{operator}',{change},{tp},{sl},{distance},'{'buy'}',{time_of})
                                                """
                                        cursor.execute(query)
                                            
                                        db.commit()
                                        used_t.clear()
                    ban_distance.clear()
             
        except Exception:
            os.system("systemctl restart postgresql") 




async def main():
    pairs_txt = open('pairs.txt','r')
    pairs_txt_with_symb = pairs_txt.readlines()
    pairs = []
    for pair in pairs_txt_with_symb:
        pairs.append(pair.replace('\n','').lower())


    
    streams = ''
    try:
        os.mkdir('data')
        
    except Exception:
        pass
    for pair in pairs:
        streams = streams+pair+"@trade/"
    streams = streams[:streams.rfind('/')]
    

    #streams = 'iotxusdt@trade'
    holder = {name: BOT(name=name) for name in pairs}
    
    client = await AsyncClient.create()
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm._get_futures_socket(path=streams,futures_type=FuturesType.USD_M,)
    timer = time.time()
    # then start receiving messages
    print("Starting to hearing websockets...")
    
    async with ts as tscm:
        print("All works fine, waiting for shots...")
        while True:
            res = await tscm.recv()
            name = res['stream'][:res['stream'].find('@')]
            data = res['data']
            with open(f'data/{name}.txt','a') as f:
                f.write(f'{data}\n')
            
            if holder[name].first_data == 0:
                holder[name].first_data = data
                holder[name].send_data(data)

            elif data['T']-60000 > holder[name].first_data['T']:
                holder[name].send_data(data)
                holder[name].get_shots()
                holder[name].clear_data()
                holder[name].first_data = 0

            else:
                holder[name].send_data(data)

                
            
            
            await client.close_connection()

if __name__ == "__main__":
    
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    """ Settings = settings()
    print(Settings.Dictance)
    print(Settings.StopLos)
    print(Settings.TakeProfit) """