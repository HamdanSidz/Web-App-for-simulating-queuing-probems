import math
import random
import pandas as pd
import chart_calculation
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

np.bool = np.bool_


total_simulated = 0        # main s update horaha
arr_mean = 0           # arrival_input fun s update horaha
ser_mean = 0      # service_input fun s update horaha

cumulative = []
lookup_cp = []
time_bw_inter_arrival = []
inter_arrival = []
s_no = []
arrival = []
service = []
priority = []


def arrival_input(arr_mean1):
    global arr_mean
    arr_mean = arr_mean1


def service_input(ser_mean1):
    global ser_mean
    ser_mean = ser_mean1


def main():

    check = False
    value = 0

    for i in range(50):               # Cumulative work here
        if check == True:
            break
        if i == 0:
            pass
        else:
            value = round(value, 4)
            cumulative.append(value)
            value = 0

        for j in range(i+1):
            value += (arr_mean**j * math.exp(-arr_mean)) / math.factorial(j)
            if round(value, 4) == 1.0:
                cumulative.append(round(value, 4))
                check = True
                # yhn total_simulated as a treat hoga local variable without gobal agr krenga
                global total_simulated
                total_simulated = i+1

    for i in range(total_simulated):       # Lookup C.P work here
        if i == 0:
            lookup_cp.append(0)
        else:
            lookup_cp.append(cumulative[i-1])

    for i in range(total_simulated):       # Time_bw_inter_arrival work here
        time_bw_inter_arrival.append(i)

    for i in range(total_simulated):       # s_no work here
        s_no.append(i+1)

    for i in range(total_simulated):       # Arrival work here
        if i == 0:
            inter_arrival.append(0)
        else:
            ran_value = round(random.random(), 4)
            for j in range(total_simulated):
                if ran_value > lookup_cp[j] and ran_value < cumulative[j]:
                    inter_arrival.append(time_bw_inter_arrival[j])
                    break
                elif ran_value == lookup_cp[j] or ran_value == cumulative[j]:
                    inter_arrival.append(time_bw_inter_arrival[j])
                    break

    for i in range(total_simulated):    # Arrival work here
        if i == 0:
            arrival.append(i)
        else:
            arrival.append(inter_arrival[i]+arrival[i-1])

    for i in range(total_simulated):     # exponential work here
        ser_value = -ser_mean*math.log(random.random())

        if round(ser_value, 0) == 0:
            ser_value += 1
            service.append(round(ser_value, 0))
            #print(round(ser_value, 0))
        else:
            service.append(round(ser_value, 0))
            #print(round(ser_value, 0))


def priority_generator(A1, B1, M1, Xo1, a1, b1):
    A = A1
    B = B1
    M = M1
    Xo = Xo1
    a = a1
    b = b1

    R_lis = []
    random_number = []

    for i in range(total_simulated):
        R = (A*Xo+B) % M
        # print(R)
        R_lis.append(R)
        Xo = R

    for i in range(total_simulated):
        random_number.append(round(R_lis[i]/M, 4))
        # print(round(R_lis[i]/M,4))

    for i in range(total_simulated):
        y = round((b-a)*random_number[i]+a, 0)
        # print(y)
        priority.append(y)


def draw_gantt_chart(gantt_chart):
    fig, ax = plt.subplots(figsize=(8, 4))  # w,h
    # Create a dictionary to store the color for each process
    colors = {}
    process_ids = list(set(gantt_chart))  # get unique process ids
    process_ids = [i for i in process_ids if i is not None]  # None from list
    process_ids.sort(key=lambda x: int(x[1:]))  # sort the process ids

    for i in range(len(gantt_chart)):
        if gantt_chart[i] is not None:
            # If the process is not in the colors dictionary, add it with a new color
            if gantt_chart[i] not in colors:
                colors[gantt_chart[i]] = (
                    np.random.random(), np.random.random(), np.random.random())

            ax.broken_barh(
                [(i, 1)],
                (9*(process_ids.index(gantt_chart[i])+1), 9),
                facecolors=colors[gantt_chart[i]]
            )

    ax.set_ylim(5, 15*(len(process_ids)+1))
    ax.set_xlim(0, len(gantt_chart))
    ax.set_xlabel('Service Time')
    ax.set_yticklabels(["c"+str(i+1) for i in range(len(process_ids))])
    ax.set_xticks(np.arange(0, len(gantt_chart), 1))
    ax.set_yticks([9*(i+1)+5 for i in range(len(process_ids))])
  
    ax.grid(True)

    # plt.show()
  
    st.subheader("Gantt Chart: ")
    st.write("The services that is pre-emtive are showing with same color as before of pre-emption, they had color assigned.")
    st.pyplot(fig)


def dataframe():
    global cumulative, lookup_cp, time_bw_inter_arrival, inter_arrival, s_no, arrival, service, priority, total_simulated, arr_mean, ser_mean

    arrival, start_time_list, end_time_list, turnaround_time_list, waiting_time_list, response_time_list, avg_turnaround_time, avg_waiting_time, avg_res_time, avg_ser_time, gantt_chart = chart_calculation.main1(
        arrival, service, priority, total_simulated)
    #print(start_time_list,end_time_list,turnaround_time_list,waiting_time_list, response_time_list, avg_turnaround_time, avg_waiting_time, avg_res_time)

    table = {"Arrival": arrival, "Service": service, "Priority": priority, "Start Time": start_time_list,
             "End Time": end_time_list, "Turn Around Time": turnaround_time_list, "Waiting Time": waiting_time_list,
             "Response Time": response_time_list}

    df = pd.DataFrame(table, index=s_no)
    df.index.name = "Customer.no"
    st.dataframe(df)

    draw_gantt_chart(gantt_chart)

    # Generating customer numbers
    customers = list(range(1, total_simulated + 1))

    fig, ax1 = plt.subplots()

    # Graph 1: Customer vs Wait Time
    ax1.bar(customers, waiting_time_list, color='skyblue')
    ax1.set_xlabel('Customers')
    ax1.set_ylabel('Waiting Time', color='skyblue')
    ax1.tick_params(axis='y', labelcolor='skyblue')

    # Graph 2: Customer vs Turnaround Time
    ax2 = ax1.twinx()
    ax2.bar(customers, turnaround_time_list, color='salmon')
    ax2.set_ylabel('Turnaround Time', color='salmon')
    ax2.tick_params(axis='y', labelcolor='salmon')
    st.pyplot(fig)

    # Create a figure and axis
    fig, ax1 = plt.subplots()

    # Plotting the first dataset (arrival time) as a bar chart on the first y-axis
    ax1.bar(customers, arrival, color='blue',
            alpha=0.7, label='Arrival Time')
    ax1.set_xlabel('Customers')
    ax1.set_ylabel('Arrival Time', color='blue')

    # Create a second y-axis and plot the second dataset (service time) as a line chart on it
    ax2 = ax1.twinx()
    ax2.plot(customers, service, marker='o',
             linestyle='-', color='red', label='Service Time')
    ax2.set_ylabel('Service Time', color='red')

    # Set x-axis ticks to display all customer numbers
    ax1.set_xticks(customers)

    # Display the legend
    fig.legend(loc='upper center')

    # Display the plot using Streamlit
    st.pyplot(fig)

    cumulative = []
    lookup_cp = []
    time_bw_inter_arrival = []
    inter_arrival = []
    s_no = []
    arrival = []
    service = []
    priority = []

    return avg_turnaround_time, avg_waiting_time, avg_res_time, avg_ser_time
