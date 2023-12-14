import work
import streamlit as st
import perf_measure


def performance_measures(service_con, turnaround_con, waiting_con, response_con):
    total_avg_ser_time = 0
    total_avg_turnaround_time = 0
    total_avg_waiting_time = 0
    total_avg_res_time = 0

    for i in range(len(service_con)):
        total_avg_ser_time += service_con[i]
        total_avg_turnaround_time += turnaround_con[i]
        total_avg_waiting_time += waiting_con[i]
        total_avg_res_time += response_con[i]

    total_avg_ser_time = round(total_avg_ser_time/len(service_con), 2)
    total_avg_turnaround_time = round(
        total_avg_turnaround_time/len(service_con), 2)
    total_avg_waiting_time = round(total_avg_waiting_time/len(service_con), 2)
    total_avg_res_time = round(total_avg_res_time/len(service_con), 2)

    st.subheader("Performance Measures: ")
    st.write("(note that performance measure given here is the average of last, and current performance measures rates, if any of above parameters are not changed)")

    st.text(f"Average Service Time: {total_avg_ser_time}")
    st.text(f"Average Turn Around Time: {total_avg_turnaround_time}")
    st.text(f"Average Waiting Time: {total_avg_waiting_time}")
    st.text(f"Average Response Time: {total_avg_res_time}")


# PAGE STARTS FROM HERE...

def main():

    st.subheader("Mean Arrival Number")
    arr_mean = st.number_input('Enter Poisson Arrival Mean', value=2.25)

    st.subheader("Mean Service Number ")
    exp_mean = st.number_input('Enter Exponential Service Mean', value=1.98)

    st.subheader("Customers Priority Numbers")
    A = st.number_input('Enter Constant A value', value=55)
    B = st.number_input('Enter Constant B value', value=9)
    M = st.number_input('Enter Constant M value', value=1994)
    Xo = st.number_input('Enter Initial seed Xo value', value=10112166)
    a = st.number_input("Specifies lowest critical value:", value=1)
    b = st.number_input("Specifies highest critical value:", value=3)


    result = st.button("Simulate or Evaluate")

    if result:
        st.subheader("Simulation of MM1 Priority Queuing Model")
        perf_measure.checker(arr_mean, exp_mean, A, B, M, Xo, a, b)
        work.arrival_input(arr_mean)
        work.service_input(exp_mean)
        work.main()
        work.priority_generator(A, B, M, Xo, a, b)
        avg_turnaround_time, avg_waiting_time, avg_res_time, avg_ser_time = work.dataframe()

        service_con, turnaround_con, waiting_con, response_con = perf_measure.checker2(
            avg_ser_time, avg_turnaround_time, avg_waiting_time, avg_res_time)

        performance_measures(service_con, turnaround_con,
                            waiting_con, response_con)






# Whenever you modify your app's source code.
# Whenever a user interacts with widgets in the app. For example, when dragging a slider, entering text in an input box, or clicking a button.
# The whole app is reruns
# Only main file "given in command of streamlit run _____ " is reruns
