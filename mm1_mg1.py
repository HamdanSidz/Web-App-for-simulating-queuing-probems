import streamlit as st
import pandas as pd
import math as mt
import random as rd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns


class Server:
    def __init__(self):
        self.time_slots = []


def assign_patient(arrival_time, service_time, servers):
    earliest_server = None
    earliest_finish_time = float('inf')

    for server in servers:
        if len(server.time_slots) == 0 or server.time_slots[-1][1] <= arrival_time:
            return server

        last_slot = server.time_slots[-1]
        if last_slot[1] < earliest_finish_time:
            earliest_finish_time = last_slot[1]
            earliest_server = server

    return earliest_server


def simulate_servers(arrival, service, num_servers):
    servers = [Server() for _ in range(num_servers)]

    for i in range(len(arrival)):
        server = assign_patient(arrival[i], service[i], servers)
        if server is None:
            print(f"Patient {i+1}: No available server.")
        else:
            start_time = max(
                server.time_slots[-1][1], arrival[i]) if len(server.time_slots) > 0 else arrival[i]
            end_time = start_time + service[i]
            server.time_slots.append([start_time, end_time])

    server_data = [[] for _ in range(num_servers)]

    for i, server in enumerate(servers):
        for slot in server.time_slots:
            server_data[i].append([slot[0], slot[1]])

    start = []

    for sublist in server_data:
        start.extend([item[0] for item in sublist])

    start.sort()

    end = [start[i] + service[i] for i in range(len(arrival))]

    return start, end


def mm1(lam, mu, server_count):

    cumulative = []
    lookup = []
    sum_prob = 0  # Initialize the sum of probabilities
    i = 0  # Initialize the loop variable

    while (sum_prob < 0.999):  # Continue the loop until the sum reaches or exceeds 1

        poisson = (mt.exp(-lam) * (lam) ** i) / mt.factorial(i)

        if i == 0:
            cumulative.append(poisson)
            lookup.append(0)
            sum_prob += poisson
        elif (i != 0):
            if (cumulative[-1] != 1):
                cumulative.append(poisson + cumulative[i - 1])
                sum_prob += poisson
                lookup.append(cumulative[i - 1])

            else:
                break

        i += 1  # Increment the loop variable

    customer_count = len(cumulative)

    check = 0

    for i in range(len(cumulative)):
        if (cumulative[i] > 1) or (cumulative[i] < 0):
            st.write(
                "Cumulative probability can only be between 0 and 1. Please try another valid input")
            check = 1
            break

    if check == 0:
       
        interarrival = [0]

        for i in range(1, customer_count):
            random_value = rd.random()

            for j in range(customer_count):

                if (lookup[j] <= random_value) and (cumulative[j] >= random_value):
                    interarrival.append(j+1)
        arrival = [0]

        for i in range(1, customer_count):
            arrival.append(arrival[i-1]+interarrival[i])

        service = []

        for i in range(customer_count):
            a = -mu*(mt.log(rd.random()))
            service.append(mt.ceil(a))

        start = [arrival[0]]

        end = [service[0]]

        for i in range(1, customer_count):

            if end[i-1] >= arrival[i]:
                start.append(end[i-1])
                end.append(start[i]+service[i])

            elif end[i-1] < arrival[i]:
                start.append(arrival[i])
                end.append(start[i]+service[i])

        turnaround = [end[i] - arrival[i] for i in range(customer_count)]
        waittime = [turnaround[i] - service[i]
                    for i in range(customer_count)]
        responsetime = [start[i] - arrival[i]
                        for i in range(customer_count)]

        df = pd.DataFrame({'Customers': [i+1 for i in range(customer_count)], 'Arrival': arrival,
                            'Service': service, 'Start': start, 'End': end, 'TurnAround': turnaround, 'WaitTime': waittime, 'ResponseTime': responsetime})
        st.dataframe(df)

        st.text(f"Average Service Time: {round((sum(service)/customer_count), 2)}")
        st.text(f"Average Turn Around Time: {round((sum(turnaround)/customer_count), 2)}")
        st.text(f"Average Wait Time: {round((sum(waittime)/customer_count), 2)}")
        st.text(f"Average Response Time: {round((sum(responsetime)/customer_count), 2)}")

##############################################################################################
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    def plot_individual_gantt_chart(server_data, server_labels, server_num):
        fig, ax = plt.subplots(figsize=(10, 6))

        for i, (s, e) in enumerate(server_data):
            ax.barh(i, e - s, left=s, height=0.6,
                    align='center', color='blue')

        ax.set_xlabel('Time')
        ax.set_ylabel('Customers')
        ax.set_yticks(range(len(server_data)))
        ax.set_yticklabels(server_labels)
        ax.set_title(f'Gantt Chart - Server {server_num}')

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()

        return fig

    start_times, end_times = simulate_servers(
        arrival, service, server_count)

   
    # Plotting individual Gantt charts for each server
    for i in range(server_count):
        server_i_data = [(start_times[j], end_times[j])
                            for j in range(len(arrival)) if j % server_count == i]
        server_i_labels = [f'Customer {j+1}' for j in range(len(arrival)) if j % server_count == i]

        fig = plot_individual_gantt_chart(
            server_i_data, server_i_labels, i + 1)
        st.pyplot(fig)

###################################################################################

    total_service_time = sum(service)
    list1 = []
    for i in range(server_count):
        server_i_data = [end_times[j]-start_times[j]
                            for j in range(len(arrival)) if j % server_count == i]
        list1.append(server_i_data)

    list2 = []
    for i in range(len(list1)):
        a = sum(list1[i])
        list2.append(round(a/total_service_time, 2))

    st.subheader("Utilization Rate Calculation")

    for i in range(server_count):
        st.text(f'Server {i+1} Utilization rate: {list2[i]}')
    st.text(f'Total Utilization rate: {sum(list2)}')

#########################################################################
    # Calculate total time
    total_service_time = sum(service)

    server = []

    for i in range(len(start)):
        server.append([start[i], end[i]])

    server_utilization_rate = sum(
        [interval[1] - interval[0] for interval in server]) / total_service_time

    # Calculate server idle rate
    server_idle_rate = 1 - server_utilization_rate

    st.text(f"Server Utilization Rate: {round(server_utilization_rate, 2)}")
    st.text(f"Server Idle Rate: {round(server_idle_rate, 2)}")

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (s, e) in enumerate(zip(start, end)):
        ax.barh(i, e - s, left=s, height=0.6,
                align='center', color='blue')

    ax.set_xlabel('Time')
    ax.set_ylabel('Customers')
    ax.set_yticks(range(len(start)))
    ax.set_yticklabels([f'Customer {i+1}' for i in range(len(start))])
    ax.set_title('Gantt Chart')

    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()

    st.pyplot(fig)

    customer_count_list = []

    for i in range(1, customer_count+1):
        customer_count_list.append(i)

    # Bar chart for Turn Around
    fig, ax = plt.subplots()
    ax.bar(customer_count_list, turnaround,
            align='center', alpha=0.7, color='seagreen')

    # Adding labels to the chart
    ax.set_title('Customer vs Turnaround Time')
    ax.set_xlabel('Customers')
    ax.set_ylabel('Turnaround Time')

    # Set x-axis ticks to display all customer numbers
    ax.set_xticks(customer_count_list)

    # Display the bar chart using Streamlit
    st.pyplot(fig)

    # Bar chart for wait Time
    fig, ax = plt.subplots()
    ax.bar(customer_count_list, waittime,
            align='center', alpha=0.7, color='blue')

    # Adding labels to the chart
    ax.set_title('Customer vs Wait Time')
    ax.set_xlabel('Customers')
    ax.set_ylabel('Wait Time')

    # Set x-axis ticks to display all customer numbers
    ax.set_xticks(customer_count_list)

    # Display the bar chart using Streamlit
    st.pyplot(fig)

    # Bar chart for Response time
    fig, ax = plt.subplots()
    ax.bar(customer_count_list, responsetime,
            align='center', alpha=0.7, color='purple')

    # Adding labels to the chart
    ax.set_title('Customer vs Response Time')
    ax.set_xlabel('Customers')
    ax.set_ylabel('Response Time')

    # Set x-axis ticks to display all customer numbers
    ax.set_xticks(customer_count_list)

    # Display the bar chart using Streamlit
    st.pyplot(fig)

    # Bar chart for Interarrival Time
    fig, ax = plt.subplots()
    ax.bar(customer_count_list, interarrival,
            align='center', alpha=0.7, color='forestgreen')

    # Adding labels to the chart
    ax.set_title('Customer vs Interarrival Time')
    ax.set_xlabel('Customers')
    ax.set_ylabel('Interarrival Time')

    # Set x-axis ticks to display all customer numbers
    ax.set_xticks(customer_count_list)

    # Display the bar chart using Streamlit
    st.pyplot(fig)

    # Create a figure and axis
    fig, ax1 = plt.subplots()

    # Plotting the first dataset (arrival time) as a bar chart on the first y-axis
    ax1.bar(customer_count_list, arrival, color='blue',
            alpha=0.7, label='Arrival Time')
    ax1.set_xlabel('Customers')
    ax1.set_ylabel('Arrival Time', color='blue')

    # Create a second y-axis and plot the second dataset (service time) as a line chart on it
    ax2 = ax1.twinx()
    ax2.plot(customer_count_list, service, marker='o',
                linestyle='-', color='red', label='Service Time')
    ax2.set_ylabel('Service Time', color='red')

    # Set x-axis ticks to display all customer numbers
    ax1.set_xticks(customer_count_list)

    # Display the legend
    fig.legend(loc='upper center')

    # Display the plot using Streamlit
    st.pyplot(fig)
# -------------------------------------------------------------------------------------------

