import time

def mop_floor():
    print("I am going to mop the floor.")
    time.sleep(1)
    print('Floor mopped.')
    
def heat_up_water():
    print('I am going to boil some water.')
    time.sleep(3)
    print('Water boiled.')

#=============== Single Thread =================   
# start_time = time.time()
# heat_up_water()
# mop_floor()
# end_time = time.time()
# print(f'Total elapse: {end_time - start_time}')

import threading

#============ Multiple Thread ==================
start_time = time.time()
t1 = threading.Thread(target=mop_floor)
t2 = threading.Thread(target=heat_up_water)
t1.start()
t2.start()
t1.join()
t2.join()
end_time = time.time()
print(f'Total elapse: {end_time - start_time}')