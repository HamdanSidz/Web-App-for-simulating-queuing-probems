
continous_pm = False
service_con = []
turnaround_con = []
waiting_con = []
response_con = []

arr_mean1 = 2.25
exp_mean1 = 1.98
A1 = 55
B1 = 9
M1 = 1994
Xo1 = 10112166
a1 = 1
b1 = 3

# print(service_con,turnaround_con,waiting_con,response_con,0)


def checker(arr_mean, exp_mean, A, B, M, Xo, a, b):

    global arr_mean1, exp_mean1, A1, B1, M1, Xo1, a1, b1, continous_pm

    # print("############")
    #print(arr_mean, exp_mean, A, B, M, Xo, a, b)
    #print(arr_mean1 ,exp_mean1 , A1 ,B1 ,M1, Xo1, a1, b1)

    if arr_mean == arr_mean1 and exp_mean == exp_mean1 and A == A1 and B == B1 and M == M1 and Xo == Xo1 and a == a1 and b == b1:
        continous_pm = True
    else:
        arr_mean1 = arr_mean
        exp_mean1 = exp_mean
        A1 = A
        B1 = B
        M1 = M
        Xo1 = Xo
        a1 = a
        b1 = b
        continous_pm = False


def checker2(avg_ser_time, avg_turnaround_time, avg_waiting_time, avg_res_time):
    global service_con, turnaround_con, waiting_con, response_con

    if continous_pm == True:
        service_con.append(avg_ser_time)
        turnaround_con.append(avg_turnaround_time)
        waiting_con.append(avg_waiting_time)
        response_con.append(avg_res_time)
        #print(service_con,turnaround_con,waiting_con,response_con, "TRUE")

    elif continous_pm == False:
        service_con = []
        turnaround_con = []
        waiting_con = []
        response_con = []
        # print(service_con,turnaround_con,waiting_con,response_con,"FALSE")
        service_con.append(avg_ser_time)
        turnaround_con.append(avg_turnaround_time)
        waiting_con.append(avg_waiting_time)
        response_con.append(avg_res_time)
        # print(service_con,turnaround_con,waiting_con,response_con,22)

    return service_con, turnaround_con, waiting_con, response_con
