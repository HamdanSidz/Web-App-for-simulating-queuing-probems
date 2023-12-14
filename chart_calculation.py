
def processData(arrival,service,priority1,total_simulated):
    process_data = []

    for i in range(total_simulated):
        temporary = []

        #process_id = int(input("Enter Process ID: "))
        #arrival_time = int(input(f"Enter Arrival Time for Process {process_id}: "))
        #burst_time = int(input(f"Enter Burst Time for Process {process_id}: "))
        #priority = int(input(f"Enter Priority for Process {process_id}: "))
     
        process_id = i+1
        arrival_time = arrival[i]
        burst_time = service[i]
        priority = priority1[i]
        #print(process_id,arrival_time,burst_time,priority,"\n")

        temporary.extend([process_id, arrival_time, burst_time, priority, 0, burst_time])

        '''
        '0' is the state of the process. 0 means not executed and 1 means execution complete
        '''
        process_data.append(temporary)

    #print(process_data)

    arrival, start_time_list, turnaround_time_list, end_time_list, waiting_time_list, response_time_list, avg_turnaround_time, avg_waiting_time, avg_res_time, gant_chart = schedulingProcess(process_data,arrival,total_simulated)

    return arrival, start_time_list, turnaround_time_list, end_time_list, waiting_time_list, response_time_list, avg_turnaround_time, avg_waiting_time, avg_res_time, gant_chart

def schedulingProcess(process_data,arrival,total_simulated):
    start_time = []
    exit_time = []
    gant_chart = []
    start_time_list = []
    response_time_list = []
    end_time_list = []
    avg_res_time = 0
    total_res_time = 0
    s_time = 0
    sequence_of_process = []
    process_data.sort(key=lambda x: x[1])

    '''
    Sort processes according to the Arrival Time
    '''
    #print(process_data)
    while 1:
        ready_queue = []
        normal_queue = []
        temp = []

        for i in range(len(process_data)):
            if process_data[i][1] <= s_time and process_data[i][4] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][3],
                             process_data[i][5]])
                ready_queue.append(temp)
                temp = []
            elif process_data[i][4] == 0:
                temp.extend([process_data[i][0], process_data[i][1], process_data[i][2], process_data[i][4],
                             process_data[i][5]])
                normal_queue.append(temp)
                temp = []
        
        if len(ready_queue) == 0 and len(normal_queue) == 0:
            break
        if len(ready_queue) != 0:
            ready_queue.sort(key=lambda x: x[3], reverse=True)
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)
            sequence_of_process.append(ready_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == ready_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            # if burst time is zero, it means process is completed
            if process_data[k][2] == 0:
                process_data[k][4] = 1
                process_data[k].append(e_time)
        if len(ready_queue) == 0:
            normal_queue.sort(key=lambda x: x[1])
            if s_time < normal_queue[0][1]:
                s_time = normal_queue[0][1]
            start_time.append(s_time)
            s_time = s_time + 1
            e_time = s_time
            exit_time.append(e_time)
            sequence_of_process.append(normal_queue[0][0])
            for k in range(len(process_data)):
                if process_data[k][0] == normal_queue[0][0]:
                    break
            process_data[k][2] = process_data[k][2] - 1
            # if burst time is zero, it means process is completed
            if process_data[k][2] == 0:
                process_data[k][4] = 1
                process_data[k].append(e_time)

        #print(sequence_of_process)

    
    c = 1                     # start time calculate here's
    for i in range(len(process_data)):
        for j in range(len(sequence_of_process)):        
            if sequence_of_process[j] == c:
                start_time_list.append(j)
                c+=1
                break
                      
    index_map = {}                      # end time list generation
    for i, value in enumerate(sequence_of_process):
        if value in index_map:
            end_time_list[index_map[value]] = i+1
        else:
            index_map[value] = len(end_time_list)
            end_time_list.append(i+1)
    
    for i in range(len(end_time_list)):
        process_data[i][6] = end_time_list[i]

    for i in range(total_simulated):     # respose time list generate
        rt = start_time_list[i]-arrival[i]
        response_time_list.append(rt)

    for i in range(len(response_time_list)):   # synchronization problem b/w Arrival and S.S
        if response_time_list[i]<0:
            process_data[i][1] += response_time_list[i]
            arrival[i] += response_time_list[i]
            response_time_list[i] = -response_time_list[i]

    response_time_list = []
    for i in range(total_simulated):     # respose time list regenerate essential
        rt = start_time_list[i]-arrival[i]
        response_time_list.append(rt)
    
    for i in range(total_simulated):
        if response_time_list[i]<0:            #  total response time  
            total_res_time += -response_time_list[i]  
        else:
            total_res_time += response_time_list[i]  

    waiting_time_list = response_time_list        #  waiting time list 
    avg_res_time = round(total_res_time/total_simulated,2)   #avg res time
    avg_waiting_time = round(total_res_time/total_simulated,2)  # avg wait time

    gant_chart = ["P"+str(sequence_of_process[i]) for i in range(len(sequence_of_process))]

    avg_turnaround_time, turnaround_time_list = calculateTurnaroundTime(process_data)

    return arrival, start_time_list, turnaround_time_list, end_time_list, waiting_time_list,response_time_list, avg_turnaround_time, avg_waiting_time, avg_res_time, gant_chart


def calculateTurnaroundTime(process_data):
    total_turnaround_time = 0
    turnaround_time_list = []  # for dataframe

    for i in range(len(process_data)):
        turnaround_time = process_data[i][6] - process_data[i][1]
        turnaround_time_list.append(turnaround_time)
        '''
        turnaround_time = completion_time - arrival_time
        '''
        total_turnaround_time = total_turnaround_time + turnaround_time
        process_data[i].append(turnaround_time)

    # print(process_data)
    average_turnaround_time = total_turnaround_time / len(process_data)
    
    return average_turnaround_time, turnaround_time_list


def main1(arrival,service,priority,total_simulated):
    
    avg_res_time = 0
    avg_ser_time = 0
    total_ser_time = 0
    arrival, start_time_list, turnaround_time_list, end_time_list, waiting_time_list, response_time_list, avg_turnaround_time, avg_waiting_time, avg_res_time, gant_chart = processData(arrival,service,priority,total_simulated)
    
    for i in range(len(service)):  # avg service time
        total_ser_time+=service[i]

    avg_ser_time = round(total_ser_time/total_simulated,2)
    avg_turnaround_time = round(avg_turnaround_time,2)
    avg_waiting_time = round(avg_waiting_time,2)

    #print(arrival,start_time_list,end_time_list,turnaround_time_list,waiting_time_list, response_time_list, avg_turnaround_time, avg_waiting_time, avg_res_time, avg_ser_time, gantt_chart)
    
    return arrival, start_time_list, end_time_list, turnaround_time_list, waiting_time_list, response_time_list, avg_turnaround_time, avg_waiting_time, avg_res_time, avg_ser_time, gant_chart
   


""" arrival = [0,1,2,4,7,8,9,11,13,14]
service = [1,4,3,3,5,6,2,4,1,5]
priority = [2,2,1,1,3,1,2,1,2,3]
main1(arrival,service,priority,10)  """

""" arrival = [0,1,2,4]
service = [5,4,2,1]
priority = [1,2,3,4]
main1(arrival,service,priority,4)
 """

""" arrival = [0,1,2,3,4]
service = [4,3,1,5,2]
priority = [2,3,4,5,5]
main1(arrival,service,priority,5)  
"""

"""
arrival = [0,1,3,4,5,6,10]
service = [8,2,4,1,6,5,1]
priority = [3,4,4,5,2,6,1]
main1(arrival,service,priority,7)
"""

# index 5 -> burst time
# index 6 -> complete time
# index 7 -> turn around time
# index 8 -> waiting time

