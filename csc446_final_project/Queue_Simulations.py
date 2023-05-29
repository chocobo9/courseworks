import random
import numpy as np
import pandas as pd  # save data into Excel file.

random.seed(12)

size = 5000

mean = 0.64

mu = 2.4

# Start of 4-Queue
inter_arrival_time1 = np.random.exponential(mean, size - 1)
inter_arrival_time = [0 for i in range(size)]
for i in range(len(inter_arrival_time1)):
    inter_arrival_time[i + 1] = inter_arrival_time1[i]

arrival_time_1 = []
arrival_time_2 = []
arrival_time_3 = []
arrival_time_4 = []

service_time_1 = []
service_time_2 = []
service_time_3 = []
service_time_4 = []

last_arrival_time = 0

for i in range(0, len(inter_arrival_time)):
    service_time = np.random.exponential(mu, size=1)[0]

    q = random.randint(1, 4)
    if q == 1:
        arrival_time_1.append(last_arrival_time + inter_arrival_time[i])
        service_time_1.append(service_time)
        last_arrival_time = arrival_time_1[-1]
    elif q == 2:
        arrival_time_2.append(last_arrival_time + inter_arrival_time[i])
        service_time_2.append(service_time)
        last_arrival_time = arrival_time_2[-1]
    elif q == 3:
        arrival_time_3.append(last_arrival_time + inter_arrival_time[i])
        service_time_3.append(service_time)
        last_arrival_time = arrival_time_3[-1]
    else:
        arrival_time_4.append(last_arrival_time + inter_arrival_time[i])
        service_time_4.append(service_time)
        last_arrival_time = arrival_time_4[-1]

Time_Service_Begin_1 = [0 for i in range(len(arrival_time_1))]
Time_Customer_Waiting_in_Queue_1 = [0 for i in range(len(arrival_time_1))]
Time_Service_Ends_1 = [0 for i in range(len(arrival_time_1))]
Time_Customer_Spend_in_System_1 = [0 for i in range(len(arrival_time_1))]
System_idle_1 = [0 for i in range(len(arrival_time_1))]

Time_Service_Begin_2 = [0 for i in range(len(arrival_time_2))]
Time_Customer_Waiting_in_Queue_2 = [0 for i in range(len(arrival_time_2))]
Time_Service_Ends_2 = [0 for i in range(len(arrival_time_2))]
Time_Customer_Spend_in_System_2 = [0 for i in range(len(arrival_time_2))]
System_idle_2 = [0 for i in range(len(arrival_time_2))]

Time_Service_Begin_3 = [0 for i in range(len(arrival_time_3))]
Time_Customer_Waiting_in_Queue_3 = [0 for i in range(len(arrival_time_3))]
Time_Service_Ends_3 = [0 for i in range(len(arrival_time_3))]
Time_Customer_Spend_in_System_3 = [0 for i in range(len(arrival_time_3))]
System_idle_3 = [0 for i in range(len(arrival_time_3))]

Time_Service_Begin_4 = [0 for i in range(len(arrival_time_4))]
Time_Customer_Waiting_in_Queue_4 = [0 for i in range(len(arrival_time_4))]
Time_Service_Ends_4 = [0 for i in range(len(arrival_time_4))]
Time_Customer_Spend_in_System_4 = [0 for i in range(len(arrival_time_4))]
System_idle_4 = [0 for i in range(len(arrival_time_4))]

Time_Service_Begin_1[0] = arrival_time_1[0]
Time_Customer_Spend_in_System_1[0] = service_time_1[0]
Time_Service_Ends_1[0] = Time_Service_Begin_1[0] + service_time_1[0]

for i in range(1, len(arrival_time_1)):
    # Time Service Begin 
    Time_Service_Begin_1[i] = max(arrival_time_1[i], Time_Service_Ends_1[i - 1])

    # Time customer waiting in queue   
    Time_Customer_Waiting_in_Queue_1[i] = Time_Service_Begin_1[i] - arrival_time_1[i]

    # Time service ends
    Time_Service_Ends_1[i] = Time_Service_Begin_1[i] + service_time_1[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_1[i] = Time_Service_Ends_1[i] - arrival_time_1[i]

    # Time when system remains idle
    if (arrival_time_1[i] > Time_Service_Ends_1[i - 1]):
        System_idle_1[i] = arrival_time_1[i] - Time_Service_Ends_1[i - 1]
    else:
        System_idle_1[i] = 0

Time_Service_Begin_2[0] = arrival_time_2[0]
Time_Customer_Spend_in_System_2[0] = service_time_2[0]
Time_Service_Ends_2[0] = Time_Service_Begin_2[0] + service_time_2[0]

for i in range(1, len(arrival_time_2)):
    # Time Service Begin 
    Time_Service_Begin_2[i] = max(arrival_time_2[i], Time_Service_Ends_2[i - 1])

    # Time customer waiting in queue   
    Time_Customer_Waiting_in_Queue_2[i] = Time_Service_Begin_2[i] - arrival_time_2[i]

    # Time service ends
    Time_Service_Ends_2[i] = Time_Service_Begin_2[i] + service_time_2[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_2[i] = Time_Service_Ends_2[i] - arrival_time_2[i]

    # Time when system remains idle
    if (arrival_time_2[i] > Time_Service_Ends_2[i - 1]):
        System_idle_2[i] = arrival_time_2[i] - Time_Service_Ends_2[i - 1]
    else:
        System_idle_2[i] = 0

Time_Service_Begin_3[0] = arrival_time_3[0]
Time_Customer_Spend_in_System_3[0] = service_time_3[0]
Time_Service_Ends_3[0] = Time_Service_Begin_3[0] + service_time_3[0]

for i in range(1, len(arrival_time_3)):
    # Time Service Begin 
    Time_Service_Begin_3[i] = max(arrival_time_3[i], Time_Service_Ends_3[i - 1])

    # Time customer waiting in queue   
    Time_Customer_Waiting_in_Queue_3[i] = Time_Service_Begin_3[i] - arrival_time_3[i]

    # Time service ends
    Time_Service_Ends_3[i] = Time_Service_Begin_3[i] + service_time_3[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_3[i] = Time_Service_Ends_3[i] - arrival_time_3[i]

    # Time when system remains idle
    if (arrival_time_3[i] > Time_Service_Ends_3[i - 1]):
        System_idle_3[i] = arrival_time_3[i] - Time_Service_Ends_3[i - 1]
    else:
        System_idle_3[i] = 0

Time_Service_Begin_4[0] = arrival_time_4[0]
Time_Customer_Spend_in_System_4[0] = service_time_4[0]
Time_Service_Ends_4[0] = Time_Service_Begin_4[0] + service_time_4[0]

for i in range(1, len(arrival_time_4)):
    # Time Service Begin 
    Time_Service_Begin_4[i] = max(arrival_time_4[i], Time_Service_Ends_4[i - 1])

    # Time customer waiting in queue   
    Time_Customer_Waiting_in_Queue_4[i] = Time_Service_Begin_4[i] - arrival_time_4[i]

    # Time service ends
    Time_Service_Ends_4[i] = Time_Service_Begin_4[i] + service_time_4[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_4[i] = Time_Service_Ends_4[i] - arrival_time_4[i]

    # Time when system remains idle
    if (arrival_time_4[i] > Time_Service_Ends_4[i - 1]):
        System_idle_4[i] = arrival_time_4[i] - Time_Service_Ends_4[i - 1]
    else:
        System_idle_4[i] = 0

'''
from prettytable import PrettyTable

x = PrettyTable()

column_names = ['AT','ST','TSB','TCWQ','TSE','TCSS','System Idle']
data = [arrival_time_2,service_time_2, Time_Service_Begin_2, Time_Customer_Waiting_in_Queue_2, Time_Service_Ends_2, Time_Customer_Spend_in_System_2, System_idle_2]

length = len(column_names)

for i in range(length):
  x.add_column(column_names[i],data[i])
  
print(x)
'''

print()
print("avg.service time at the whole system (4-QUEUE): " + str(
    (sum(service_time_1) + sum(service_time_2) + sum(service_time_3) + sum(service_time_4)) / (
                len(service_time_1) + len(service_time_2) + len(service_time_3) + len(service_time_4))))

avg_queue_1 = sum(Time_Customer_Waiting_in_Queue_1) / len(Time_Customer_Waiting_in_Queue_1)

avg_queue_2 = sum(Time_Customer_Waiting_in_Queue_2) / len(Time_Customer_Waiting_in_Queue_2)

avg_queue_3 = sum(Time_Customer_Waiting_in_Queue_3) / len(Time_Customer_Waiting_in_Queue_3)

avg_queue_4 = sum(Time_Customer_Waiting_in_Queue_4) / len(Time_Customer_Waiting_in_Queue_4)

avg_queue = (avg_queue_1 + avg_queue_2 + avg_queue_3 + avg_queue_4) / 4

print("avg.time customer spent in the queue (4-QUEUE): " + str(avg_queue))

avg_system_1 = sum(Time_Customer_Spend_in_System_1) / len(Time_Customer_Spend_in_System_1)

avg_system_2 = sum(Time_Customer_Spend_in_System_2) / len(Time_Customer_Spend_in_System_2)

avg_system_3 = sum(Time_Customer_Spend_in_System_3) / len(Time_Customer_Spend_in_System_3)

avg_system_4 = sum(Time_Customer_Spend_in_System_4) / len(Time_Customer_Spend_in_System_4)

avg_sys = (avg_system_1 + avg_system_2 + avg_system_3 + avg_system_4) / 4

print("avg.time customer spent in the system (4-QUEUE): " + str(avg_sys))

print("The total time spent by the system (4-QUEUE): " + str(
    max(Time_Service_Ends_1[-1], Time_Service_Ends_2[-1], Time_Service_Ends_3[-1], Time_Service_Ends_4[-1])))
# The code below is used to write all data into a single Excel file.
# data_dict1_4 = {
#     'AT': arrival_time_1,
#     'ST': service_time_1,
#     'TSB': Time_Service_Begin_1,
#     'TCWQ': Time_Customer_Waiting_in_Queue_1,
#     'TSE': Time_Service_Ends_1,
#     'TCSS': Time_Customer_Spend_in_System_1,
#     'System Idle': System_idle_1
# }
#
# data_dict2_4 = {
#     'AT': arrival_time_2,
#     'ST': service_time_2,
#     'TSB': Time_Service_Begin_2,
#     'TCWQ': Time_Customer_Waiting_in_Queue_2,
#     'TSE': Time_Service_Ends_2,
#     'TCSS': Time_Customer_Spend_in_System_2,
#     'System Idle': System_idle_2
# }
#
# data_dict3_4 = {
#     'AT': arrival_time_3,
#     'ST': service_time_3,
#     'TSB': Time_Service_Begin_3,
#     'TCWQ': Time_Customer_Waiting_in_Queue_3,
#     'TSE': Time_Service_Ends_3,
#     'TCSS': Time_Customer_Spend_in_System_3,
#     'System Idle': System_idle_3
# }
#
# data_dict4_4 = {
#     'AT': arrival_time_4,
#     'ST': service_time_4,
#     'TSB': Time_Service_Begin_4,
#     'TCWQ': Time_Customer_Waiting_in_Queue_4,
#     'TSE': Time_Service_Ends_4,
#     'TCSS': Time_Customer_Spend_in_System_4,
#     'System Idle': System_idle_4
# }
# file_name = 'merged_test_data_4.xlsx'
# test_data_4 = [data_dict1_4,data_dict2_4,data_dict3_4,data_dict4_4]
# data_frames = [pd.DataFrame(data_dict) for data_dict in test_data_4]
# merged_data = pd.concat(data_frames, ignore_index=True)
# with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
#     merged_data.to_excel(writer, sheet_name='All Data', index=False)


# Start of 5-Queue
inter_arrival_time1 = np.random.exponential(mean, size - 1)
inter_arrival_time = [0 for i in range(size)]
for i in range(len(inter_arrival_time1)):
    inter_arrival_time[i + 1] = inter_arrival_time1[i]

arrival_time_1 = []
arrival_time_2 = []
arrival_time_3 = []
arrival_time_4 = []
arrival_time_5 = []

service_time_1 = []
service_time_2 = []
service_time_3 = []
service_time_4 = []
service_time_5 = []

last_arrival_time = 0

for i in range(0, len(inter_arrival_time)):
    service_time = np.random.exponential(mu, size=1)[0]

    q = random.randint(1, 5)
    if q == 1:
        arrival_time_1.append(last_arrival_time + inter_arrival_time[i])
        service_time_1.append(service_time)
        last_arrival_time = arrival_time_1[-1]
    elif q == 2:
        arrival_time_2.append(last_arrival_time + inter_arrival_time[i])
        service_time_2.append(service_time)
        last_arrival_time = arrival_time_2[-1]
    elif q == 3:
        arrival_time_3.append(last_arrival_time + inter_arrival_time[i])
        service_time_3.append(service_time)
        last_arrival_time = arrival_time_3[-1]
    elif q == 4:
        arrival_time_4.append(last_arrival_time + inter_arrival_time[i])
        service_time_4.append(service_time)
        last_arrival_time = arrival_time_4[-1]
    else:
        arrival_time_5.append(last_arrival_time + inter_arrival_time[i])
        service_time_5.append(service_time)
        last_arrival_time = arrival_time_5[-1]

Time_Service_Begin_1 = [0 for i in range(len(arrival_time_1))]
Time_Customer_Waiting_in_Queue_1 = [0 for i in range(len(arrival_time_1))]
Time_Service_Ends_1 = [0 for i in range(len(arrival_time_1))]
Time_Customer_Spend_in_System_1 = [0 for i in range(len(arrival_time_1))]
System_idle_1 = [0 for i in range(len(arrival_time_1))]

Time_Service_Begin_2 = [0 for i in range(len(arrival_time_2))]
Time_Customer_Waiting_in_Queue_2 = [0 for i in range(len(arrival_time_2))]
Time_Service_Ends_2 = [0 for i in range(len(arrival_time_2))]
Time_Customer_Spend_in_System_2 = [0 for i in range(len(arrival_time_2))]
System_idle_2 = [0 for i in range(len(arrival_time_2))]

Time_Service_Begin_3 = [0 for i in range(len(arrival_time_3))]
Time_Customer_Waiting_in_Queue_3 = [0 for i in range(len(arrival_time_3))]
Time_Service_Ends_3 = [0 for i in range(len(arrival_time_3))]
Time_Customer_Spend_in_System_3 = [0 for i in range(len(arrival_time_3))]
System_idle_3 = [0 for i in range(len(arrival_time_3))]

Time_Service_Begin_4 = [0 for i in range(len(arrival_time_4))]
Time_Customer_Waiting_in_Queue_4 = [0 for i in range(len(arrival_time_4))]
Time_Service_Ends_4 = [0 for i in range(len(arrival_time_4))]
Time_Customer_Spend_in_System_4 = [0 for i in range(len(arrival_time_4))]
System_idle_4 = [0 for i in range(len(arrival_time_4))]

Time_Service_Begin_5 = [0 for i in range(len(arrival_time_5))]
Time_Customer_Waiting_in_Queue_5 = [0 for i in range(len(arrival_time_5))]
Time_Service_Ends_5 = [0 for i in range(len(arrival_time_5))]
Time_Customer_Spend_in_System_5 = [0 for i in range(len(arrival_time_5))]
System_idle_5 = [0 for i in range(len(arrival_time_5))]

Time_Service_Begin_1[0] = arrival_time_1[0]
Time_Customer_Spend_in_System_1[0] = service_time_1[0]
Time_Service_Ends_1[0] = Time_Service_Begin_1[0] + service_time_1[0]

for i in range(1, len(arrival_time_1)):
    # Time Service Begin
    Time_Service_Begin_1[i] = max(arrival_time_1[i], Time_Service_Ends_1[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_1[i] = Time_Service_Begin_1[i] - arrival_time_1[i]

    # Time service ends
    Time_Service_Ends_1[i] = Time_Service_Begin_1[i] + service_time_1[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_1[i] = Time_Service_Ends_1[i] - arrival_time_1[i]

    # Time when system remains idle
    if (arrival_time_1[i] > Time_Service_Ends_1[i - 1]):
        System_idle_1[i] = arrival_time_1[i] - Time_Service_Ends_1[i - 1]
    else:
        System_idle_1[i] = 0

Time_Service_Begin_2[0] = arrival_time_2[0]
Time_Customer_Spend_in_System_2[0] = service_time_2[0]
Time_Service_Ends_2[0] = Time_Service_Begin_2[0] + service_time_2[0]

for i in range(1, len(arrival_time_2)):
    # Time Service Begin
    Time_Service_Begin_2[i] = max(arrival_time_2[i], Time_Service_Ends_2[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_2[i] = Time_Service_Begin_2[i] - arrival_time_2[i]

    # Time service ends
    Time_Service_Ends_2[i] = Time_Service_Begin_2[i] + service_time_2[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_2[i] = Time_Service_Ends_2[i] - arrival_time_2[i]

    # Time when system remains idle
    if (arrival_time_2[i] > Time_Service_Ends_2[i - 1]):
        System_idle_2[i] = arrival_time_2[i] - Time_Service_Ends_2[i - 1]
    else:
        System_idle_2[i] = 0

Time_Service_Begin_3[0] = arrival_time_3[0]
Time_Customer_Spend_in_System_3[0] = service_time_3[0]
Time_Service_Ends_3[0] = Time_Service_Begin_3[0] + service_time_3[0]

for i in range(1, len(arrival_time_3)):
    # Time Service Begin
    Time_Service_Begin_3[i] = max(arrival_time_3[i], Time_Service_Ends_3[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_3[i] = Time_Service_Begin_3[i] - arrival_time_3[i]

    # Time service ends
    Time_Service_Ends_3[i] = Time_Service_Begin_3[i] + service_time_3[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_3[i] = Time_Service_Ends_3[i] - arrival_time_3[i]

    # Time when system remains idle
    if (arrival_time_3[i] > Time_Service_Ends_3[i - 1]):
        System_idle_3[i] = arrival_time_3[i] - Time_Service_Ends_3[i - 1]
    else:
        System_idle_3[i] = 0

Time_Service_Begin_4[0] = arrival_time_4[0]
Time_Customer_Spend_in_System_4[0] = service_time_4[0]
Time_Service_Ends_4[0] = Time_Service_Begin_4[0] + service_time_4[0]

for i in range(1, len(arrival_time_4)):
    # Time Service Begin
    Time_Service_Begin_4[i] = max(arrival_time_4[i], Time_Service_Ends_4[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_4[i] = Time_Service_Begin_4[i] - arrival_time_4[i]

    # Time service ends
    Time_Service_Ends_4[i] = Time_Service_Begin_4[i] + service_time_4[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_4[i] = Time_Service_Ends_4[i] - arrival_time_4[i]

    # Time when system remains idle
    if (arrival_time_4[i] > Time_Service_Ends_4[i - 1]):
        System_idle_4[i] = arrival_time_4[i] - Time_Service_Ends_4[i - 1]
    else:
        System_idle_4[i] = 0

Time_Service_Begin_5[0] = arrival_time_5[0]
Time_Customer_Spend_in_System_5[0] = service_time_5[0]
Time_Service_Ends_5[0] = Time_Service_Begin_5[0] + service_time_5[0]

for i in range(1, len(arrival_time_5)):
    # Time Service Begin
    Time_Service_Begin_5[i] = max(arrival_time_5[i], Time_Service_Ends_5[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_5[i] = Time_Service_Begin_5[i] - arrival_time_5[i]

    # Time service ends
    Time_Service_Ends_5[i] = Time_Service_Begin_5[i] + service_time_5[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_5[i] = Time_Service_Ends_5[i] - arrival_time_5[i]

    # Time when system remains idle
    if (arrival_time_5[i] > Time_Service_Ends_5[i - 1]):
        System_idle_5[i] = arrival_time_5[i] - Time_Service_Ends_5[i - 1]
    else:
        System_idle_5[i] = 0

'''
from prettytable import PrettyTable

x = PrettyTable()

column_names = ['AT','ST','TSB','TCWQ','TSE','TCSS','System Idle']
data = [arrival_time_2,service_time_2, Time_Service_Begin_2, Time_Customer_Waiting_in_Queue_2, Time_Service_Ends_2, Time_Customer_Spend_in_System_2, System_idle_2]

length = len(column_names)

for i in range(length):
  x.add_column(column_names[i],data[i])
  
print(x)
'''

print()
print("avg.service time at the whole system (5-QUEUE): " + str(
    (sum(service_time_1) + sum(service_time_2) + sum(service_time_3) +
     sum(service_time_4) + sum(service_time_5)) / (
                len(service_time_1) + len(service_time_2) + len(service_time_3) + len(service_time_4) + len(
            service_time_5))))

avg_queue_1 = sum(Time_Customer_Waiting_in_Queue_1) / len(Time_Customer_Waiting_in_Queue_1)

avg_queue_2 = sum(Time_Customer_Waiting_in_Queue_2) / len(Time_Customer_Waiting_in_Queue_2)

avg_queue_3 = sum(Time_Customer_Waiting_in_Queue_3) / len(Time_Customer_Waiting_in_Queue_3)

avg_queue_4 = sum(Time_Customer_Waiting_in_Queue_4) / len(Time_Customer_Waiting_in_Queue_4)

avg_queue_5 = sum(Time_Customer_Waiting_in_Queue_5) / len(Time_Customer_Waiting_in_Queue_5)

avg_queue = (avg_queue_1 + avg_queue_2 + avg_queue_3 + avg_queue_4 + avg_queue_5) / 5

print("avg.time customer spent in the queue (5-QUEUE): " + str(avg_queue))

avg_system_1 = sum(Time_Customer_Spend_in_System_1) / len(Time_Customer_Spend_in_System_1)

avg_system_2 = sum(Time_Customer_Spend_in_System_2) / len(Time_Customer_Spend_in_System_2)

avg_system_3 = sum(Time_Customer_Spend_in_System_3) / len(Time_Customer_Spend_in_System_3)

avg_system_4 = sum(Time_Customer_Spend_in_System_4) / len(Time_Customer_Spend_in_System_4)

avg_system_5 = sum(Time_Customer_Spend_in_System_5) / len(Time_Customer_Spend_in_System_5)

avg_sys = (avg_system_1 + avg_system_2 + avg_system_3 + avg_system_4 + avg_system_5) / 5

print("avg.time customer spent in the system (5-QUEUE): " + str(avg_sys))

print("The total time spent by the system (5-QUEUE): " +
      str(max(Time_Service_Ends_1[-1], Time_Service_Ends_2[-1], Time_Service_Ends_3[-1], Time_Service_Ends_4[-1],
              Time_Service_Ends_5[-1])))
# The code below is used to write all data into a single Excel file.
# data_dict1_5 = {
#     'AT': arrival_time_1,
#     'ST': service_time_1,
#     'TSB': Time_Service_Begin_1,
#     'TCWQ': Time_Customer_Waiting_in_Queue_1,
#     'TSE': Time_Service_Ends_1,
#     'TCSS': Time_Customer_Spend_in_System_1,
#     'System Idle': System_idle_1
# }
#
# data_dict2_5 = {
#     'AT': arrival_time_2,
#     'ST': service_time_2,
#     'TSB': Time_Service_Begin_2,
#     'TCWQ': Time_Customer_Waiting_in_Queue_2,
#     'TSE': Time_Service_Ends_2,
#     'TCSS': Time_Customer_Spend_in_System_2,
#     'System Idle': System_idle_2
# }
#
# data_dict3_5 = {
#     'AT': arrival_time_3,
#     'ST': service_time_3,
#     'TSB': Time_Service_Begin_3,
#     'TCWQ': Time_Customer_Waiting_in_Queue_3,
#     'TSE': Time_Service_Ends_3,
#     'TCSS': Time_Customer_Spend_in_System_3,
#     'System Idle': System_idle_3
# }
#
# data_dict4_5 = {
#     'AT': arrival_time_4,
#     'ST': service_time_4,
#     'TSB': Time_Service_Begin_4,
#     'TCWQ': Time_Customer_Waiting_in_Queue_4,
#     'TSE': Time_Service_Ends_4,
#     'TCSS': Time_Customer_Spend_in_System_4,
#     'System Idle': System_idle_4
# }
#
# data_dict5_5 = {
#     'AT': arrival_time_5,
#     'ST': service_time_5,
#     'TSB': Time_Service_Begin_5,
#     'TCWQ': Time_Customer_Waiting_in_Queue_5,
#     'TSE': Time_Service_Ends_5,
#     'TCSS': Time_Customer_Spend_in_System_5,
#     'System Idle': System_idle_5
# }
#
# file_name = 'merged_test_data_5.xlsx'
# test_data_5 = [data_dict1_5,data_dict2_5,data_dict3_5,data_dict4_5,data_dict5_5]
# data_frames = [pd.DataFrame(data_dict) for data_dict in test_data_5]
# merged_data = pd.concat(data_frames, ignore_index=True)
# with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
#     merged_data.to_excel(writer, sheet_name='All Data', index=False)

# Start of 6-Queue
inter_arrival_time1 = np.random.exponential(mean, size - 1)
inter_arrival_time = [0 for i in range(size)]
for i in range(len(inter_arrival_time1)):
    inter_arrival_time[i + 1] = inter_arrival_time1[i]

arrival_time_1 = []
arrival_time_2 = []
arrival_time_3 = []
arrival_time_4 = []
arrival_time_5 = []
arrival_time_6 = []

service_time_1 = []
service_time_2 = []
service_time_3 = []
service_time_4 = []
service_time_5 = []
service_time_6 = []

last_arrival_time = 0

for i in range(0, len(inter_arrival_time)):
    service_time = np.random.exponential(mu, size=1)[0]

    q = random.randint(1, 6)
    if q == 1:
        arrival_time_1.append(last_arrival_time + inter_arrival_time[i])
        service_time_1.append(service_time)
        last_arrival_time = arrival_time_1[-1]
    elif q == 2:
        arrival_time_2.append(last_arrival_time + inter_arrival_time[i])
        service_time_2.append(service_time)
        last_arrival_time = arrival_time_2[-1]
    elif q == 3:
        arrival_time_3.append(last_arrival_time + inter_arrival_time[i])
        service_time_3.append(service_time)
        last_arrival_time = arrival_time_3[-1]
    elif q == 4:
        arrival_time_4.append(last_arrival_time + inter_arrival_time[i])
        service_time_4.append(service_time)
        last_arrival_time = arrival_time_4[-1]
    elif q == 5:
        arrival_time_5.append(last_arrival_time + inter_arrival_time[i])
        service_time_5.append(service_time)
        last_arrival_time = arrival_time_5[-1]
    else:
        arrival_time_6.append(last_arrival_time + inter_arrival_time[i])
        service_time_6.append(service_time)
        last_arrival_time = arrival_time_6[-1]

Time_Service_Begin_1 = [0 for i in range(len(arrival_time_1))]
Time_Customer_Waiting_in_Queue_1 = [0 for i in range(len(arrival_time_1))]
Time_Service_Ends_1 = [0 for i in range(len(arrival_time_1))]
Time_Customer_Spend_in_System_1 = [0 for i in range(len(arrival_time_1))]
System_idle_1 = [0 for i in range(len(arrival_time_1))]

Time_Service_Begin_2 = [0 for i in range(len(arrival_time_2))]
Time_Customer_Waiting_in_Queue_2 = [0 for i in range(len(arrival_time_2))]
Time_Service_Ends_2 = [0 for i in range(len(arrival_time_2))]
Time_Customer_Spend_in_System_2 = [0 for i in range(len(arrival_time_2))]
System_idle_2 = [0 for i in range(len(arrival_time_2))]

Time_Service_Begin_3 = [0 for i in range(len(arrival_time_3))]
Time_Customer_Waiting_in_Queue_3 = [0 for i in range(len(arrival_time_3))]
Time_Service_Ends_3 = [0 for i in range(len(arrival_time_3))]
Time_Customer_Spend_in_System_3 = [0 for i in range(len(arrival_time_3))]
System_idle_3 = [0 for i in range(len(arrival_time_3))]

Time_Service_Begin_4 = [0 for i in range(len(arrival_time_4))]
Time_Customer_Waiting_in_Queue_4 = [0 for i in range(len(arrival_time_4))]
Time_Service_Ends_4 = [0 for i in range(len(arrival_time_4))]
Time_Customer_Spend_in_System_4 = [0 for i in range(len(arrival_time_4))]
System_idle_4 = [0 for i in range(len(arrival_time_4))]

Time_Service_Begin_5 = [0 for i in range(len(arrival_time_5))]
Time_Customer_Waiting_in_Queue_5 = [0 for i in range(len(arrival_time_5))]
Time_Service_Ends_5 = [0 for i in range(len(arrival_time_5))]
Time_Customer_Spend_in_System_5 = [0 for i in range(len(arrival_time_5))]
System_idle_5 = [0 for i in range(len(arrival_time_5))]

Time_Service_Begin_6 = [0 for i in range(len(arrival_time_6))]
Time_Customer_Waiting_in_Queue_6 = [0 for i in range(len(arrival_time_6))]
Time_Service_Ends_6 = [0 for i in range(len(arrival_time_6))]
Time_Customer_Spend_in_System_6 = [0 for i in range(len(arrival_time_6))]
System_idle_6 = [0 for i in range(len(arrival_time_6))]

Time_Service_Begin_1[0] = arrival_time_1[0]
Time_Customer_Spend_in_System_1[0] = service_time_1[0]
Time_Service_Ends_1[0] = Time_Service_Begin_1[0] + service_time_1[0]

for i in range(1, len(arrival_time_1)):
    # Time Service Begin
    Time_Service_Begin_1[i] = max(arrival_time_1[i], Time_Service_Ends_1[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_1[i] = Time_Service_Begin_1[i] - arrival_time_1[i]

    # Time service ends
    Time_Service_Ends_1[i] = Time_Service_Begin_1[i] + service_time_1[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_1[i] = Time_Service_Ends_1[i] - arrival_time_1[i]

    # Time when system remains idle
    if (arrival_time_1[i] > Time_Service_Ends_1[i - 1]):
        System_idle_1[i] = arrival_time_1[i] - Time_Service_Ends_1[i - 1]
    else:
        System_idle_1[i] = 0

Time_Service_Begin_2[0] = arrival_time_2[0]
Time_Customer_Spend_in_System_2[0] = service_time_2[0]
Time_Service_Ends_2[0] = Time_Service_Begin_2[0] + service_time_2[0]

for i in range(1, len(arrival_time_2)):
    # Time Service Begin
    Time_Service_Begin_2[i] = max(arrival_time_2[i], Time_Service_Ends_2[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_2[i] = Time_Service_Begin_2[i] - arrival_time_2[i]

    # Time service ends
    Time_Service_Ends_2[i] = Time_Service_Begin_2[i] + service_time_2[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_2[i] = Time_Service_Ends_2[i] - arrival_time_2[i]

    # Time when system remains idle
    if (arrival_time_2[i] > Time_Service_Ends_2[i - 1]):
        System_idle_2[i] = arrival_time_2[i] - Time_Service_Ends_2[i - 1]
    else:
        System_idle_2[i] = 0

Time_Service_Begin_3[0] = arrival_time_3[0]
Time_Customer_Spend_in_System_3[0] = service_time_3[0]
Time_Service_Ends_3[0] = Time_Service_Begin_3[0] + service_time_3[0]

for i in range(1, len(arrival_time_3)):
    # Time Service Begin
    Time_Service_Begin_3[i] = max(arrival_time_3[i], Time_Service_Ends_3[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_3[i] = Time_Service_Begin_3[i] - arrival_time_3[i]

    # Time service ends
    Time_Service_Ends_3[i] = Time_Service_Begin_3[i] + service_time_3[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_3[i] = Time_Service_Ends_3[i] - arrival_time_3[i]

    # Time when system remains idle
    if (arrival_time_3[i] > Time_Service_Ends_3[i - 1]):
        System_idle_3[i] = arrival_time_3[i] - Time_Service_Ends_3[i - 1]
    else:
        System_idle_3[i] = 0

Time_Service_Begin_4[0] = arrival_time_4[0]
Time_Customer_Spend_in_System_4[0] = service_time_4[0]
Time_Service_Ends_4[0] = Time_Service_Begin_4[0] + service_time_4[0]

for i in range(1, len(arrival_time_4)):
    # Time Service Begin
    Time_Service_Begin_4[i] = max(arrival_time_4[i], Time_Service_Ends_4[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_4[i] = Time_Service_Begin_4[i] - arrival_time_4[i]

    # Time service ends
    Time_Service_Ends_4[i] = Time_Service_Begin_4[i] + service_time_4[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_4[i] = Time_Service_Ends_4[i] - arrival_time_4[i]

    # Time when system remains idle
    if (arrival_time_4[i] > Time_Service_Ends_4[i - 1]):
        System_idle_4[i] = arrival_time_4[i] - Time_Service_Ends_4[i - 1]
    else:
        System_idle_4[i] = 0

Time_Service_Begin_5[0] = arrival_time_5[0]
Time_Customer_Spend_in_System_5[0] = service_time_5[0]
Time_Service_Ends_5[0] = Time_Service_Begin_5[0] + service_time_5[0]

for i in range(1, len(arrival_time_5)):
    # Time Service Begin
    Time_Service_Begin_5[i] = max(arrival_time_5[i], Time_Service_Ends_5[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_5[i] = Time_Service_Begin_5[i] - arrival_time_5[i]

    # Time service ends
    Time_Service_Ends_5[i] = Time_Service_Begin_5[i] + service_time_5[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_5[i] = Time_Service_Ends_5[i] - arrival_time_5[i]

    # Time when system remains idle
    if (arrival_time_5[i] > Time_Service_Ends_5[i - 1]):
        System_idle_5[i] = arrival_time_5[i] - Time_Service_Ends_5[i - 1]
    else:
        System_idle_5[i] = 0

Time_Service_Begin_6[0] = arrival_time_6[0]
Time_Customer_Spend_in_System_6[0] = service_time_6[0]
Time_Service_Ends_6[0] = Time_Service_Begin_6[0] + service_time_6[0]

for i in range(1, len(arrival_time_6)):
    # Time Service Begin
    Time_Service_Begin_6[i] = max(arrival_time_6[i], Time_Service_Ends_6[i - 1])

    # Time customer waiting in queue
    Time_Customer_Waiting_in_Queue_6[i] = Time_Service_Begin_6[i] - arrival_time_6[i]

    # Time service ends
    Time_Service_Ends_6[i] = Time_Service_Begin_6[i] + service_time_6[i]

    # Time Customer Spend in the system
    Time_Customer_Spend_in_System_6[i] = Time_Service_Ends_6[i] - arrival_time_6[i]

    # Time when system remains idle
    if (arrival_time_6[i] > Time_Service_Ends_6[i - 1]):
        System_idle_6[i] = arrival_time_6[i] - Time_Service_Ends_6[i - 1]
    else:
        System_idle_6[i] = 0

'''
from prettytable import PrettyTable

x = PrettyTable()

column_names = ['AT','ST','TSB','TCWQ','TSE','TCSS','System Idle']
data = [arrival_time_2,service_time_2, Time_Service_Begin_2, Time_Customer_Waiting_in_Queue_2, Time_Service_Ends_2, Time_Customer_Spend_in_System_2, System_idle_2]

length = len(column_names)

for i in range(length):
  x.add_column(column_names[i],data[i])
  
print(x)
'''

print()
print("avg.service time at the whole system (6-QUEUE): " + str(
    (sum(service_time_1) + sum(service_time_2) + sum(service_time_3) +
     sum(service_time_4) + sum(service_time_5) + sum(service_time_6)) / (
                len(service_time_1) + len(service_time_2) + len(service_time_3) + len(service_time_4) + len(
            service_time_5) + len(service_time_6))))

avg_queue_1 = sum(Time_Customer_Waiting_in_Queue_1) / len(Time_Customer_Waiting_in_Queue_1)

avg_queue_2 = sum(Time_Customer_Waiting_in_Queue_2) / len(Time_Customer_Waiting_in_Queue_2)

avg_queue_3 = sum(Time_Customer_Waiting_in_Queue_3) / len(Time_Customer_Waiting_in_Queue_3)

avg_queue_4 = sum(Time_Customer_Waiting_in_Queue_4) / len(Time_Customer_Waiting_in_Queue_4)

avg_queue_5 = sum(Time_Customer_Waiting_in_Queue_5) / len(Time_Customer_Waiting_in_Queue_5)

avg_queue_6 = sum(Time_Customer_Waiting_in_Queue_6) / len(Time_Customer_Waiting_in_Queue_6)

avg_queue = (avg_queue_1 + avg_queue_2 + avg_queue_3 + avg_queue_4 + avg_queue_5 + avg_queue_6) / 6

print("avg.time customer spent in the queue (6-QUEUE): " + str(avg_queue))

avg_system_1 = sum(Time_Customer_Spend_in_System_1) / len(Time_Customer_Spend_in_System_1)

avg_system_2 = sum(Time_Customer_Spend_in_System_2) / len(Time_Customer_Spend_in_System_2)

avg_system_3 = sum(Time_Customer_Spend_in_System_3) / len(Time_Customer_Spend_in_System_3)

avg_system_4 = sum(Time_Customer_Spend_in_System_4) / len(Time_Customer_Spend_in_System_4)

avg_system_5 = sum(Time_Customer_Spend_in_System_5) / len(Time_Customer_Spend_in_System_5)

avg_system_6 = sum(Time_Customer_Spend_in_System_6) / len(Time_Customer_Spend_in_System_6)

avg_sys = (avg_system_1 + avg_system_2 + avg_system_3 + avg_system_4 + avg_system_5 + avg_system_6) / 6

print("avg.time customer spent in the system (6-QUEUE): " + str(avg_sys))

print("The total time spent by the system (6-QUEUE): " +
      str(max(Time_Service_Ends_1[-1], Time_Service_Ends_2[-1], Time_Service_Ends_3[-1], Time_Service_Ends_4[-1],
              Time_Service_Ends_5[-1], Time_Service_Ends_6[-1])))

# The code below is used to write all data into a single Excel file.
# data_dict1_6 = {
#     'AT': arrival_time_1,
#     'ST': service_time_1,
#     'TSB': Time_Service_Begin_1,
#     'TCWQ': Time_Customer_Waiting_in_Queue_1,
#     'TSE': Time_Service_Ends_1,
#     'TCSS': Time_Customer_Spend_in_System_1,
#     'System Idle': System_idle_1
# }
#
# data_dict2_6 = {
#     'AT': arrival_time_2,
#     'ST': service_time_2,
#     'TSB': Time_Service_Begin_2,
#     'TCWQ': Time_Customer_Waiting_in_Queue_2,
#     'TSE': Time_Service_Ends_2,
#     'TCSS': Time_Customer_Spend_in_System_2,
#     'System Idle': System_idle_2
# }
#
# data_dict3_6 = {
#     'AT': arrival_time_3,
#     'ST': service_time_3,
#     'TSB': Time_Service_Begin_3,
#     'TCWQ': Time_Customer_Waiting_in_Queue_3,
#     'TSE': Time_Service_Ends_3,
#     'TCSS': Time_Customer_Spend_in_System_3,
#     'System Idle': System_idle_3
# }
#
# data_dict4_6 = {
#     'AT': arrival_time_4,
#     'ST': service_time_4,
#     'TSB': Time_Service_Begin_4,
#     'TCWQ': Time_Customer_Waiting_in_Queue_4,
#     'TSE': Time_Service_Ends_4,
#     'TCSS': Time_Customer_Spend_in_System_4,
#     'System Idle': System_idle_4
# }
#
# data_dict5_6 = {
#     'AT': arrival_time_5,
#     'ST': service_time_5,
#     'TSB': Time_Service_Begin_5,
#     'TCWQ': Time_Customer_Waiting_in_Queue_5,
#     'TSE': Time_Service_Ends_5,
#     'TCSS': Time_Customer_Spend_in_System_5,
#     'System Idle': System_idle_5
# }
# data_dict6_6 = {
#     'AT': arrival_time_6,
#     'ST': service_time_6,
#     'TSB': Time_Service_Begin_6,
#     'TCWQ': Time_Customer_Waiting_in_Queue_6,
#     'TSE': Time_Service_Ends_6,
#     'TCSS': Time_Customer_Spend_in_System_6,
#     'System Idle': System_idle_6
# }
# file_name = 'merged_test_data_6.xlsx'
# test_data_6 = [data_dict1_6,data_dict2_6,data_dict3_6,data_dict4_6,data_dict5_6,data_dict6_6]
# data_frames = [pd.DataFrame(data_dict) for data_dict in test_data_6]
# merged_data = pd.concat(data_frames, ignore_index=True)
# with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
#     merged_data.to_excel(writer, sheet_name='All Data', index=False)
