import streamlit as st
import mm1_mg1
import mm2_mg2
import gg1
import gg2
import queuing_models
import main_of_priority


def mainInit():

    a = st.sidebar.selectbox("Selects From Following Pages", ["Simulator", "Queuing model"], index=0)

    if a == "Simulator":

        st.title("Simulation and Modelling")

        #choice_format = st.radio("Choose time unit:", ["minutes", "seconds"])

        model = st.selectbox("Selects Model", ["M/M/C", "M/G/C", "G/G/C", "M/M/1 Priority Model"], index=0)

        if model != "M/M/1 Priority Model":
            server_count = st.number_input('Enter Servers', value=1)

        if model == "M/M/1 Priority Model":

            main_of_priority.main()
    

        elif server_count == 1:

            if model == "M/M/C":

                st.subheader(f"Poisson and Exponential Distributions M/M/{server_count}")
                lam = st.number_input('Enter value of Lambda',value=2.65)
                mu = st.number_input('Enter value of mu',value=1.65)
                if st.button("Simulate"):
                    st.title("M/M/1")
                    mm1_mg1.mm1(lam, mu, server_count)

            elif model == "M/G/C":

                st.subheader(f"Poisson and Uniform Distributions M/G/{server_count}")              
                lam = st.number_input('Enter value of Lambda', value=2.65)
                max = st.number_input('Enter value of max', value=10)
                min = st.number_input('Enter value of min', value=5)
                mu = (max+min)/2
                if st.button("Simulate"):
                    st.title("M/G/1")
                    mm1_mg1.mm1(lam, mu, server_count)

            elif model == "G/G/C":
                
                st.subheader(f"Noraml and Uniform Distributions G/G/{server_count}")
                mean = st.number_input('Enter value of mean', value=9)
                variance = st.number_input('Enter value of variance', value=5)
                max = st.number_input('Enter value of max', value=10)
                min = st.number_input('Enter value of min', value=5)
                if st.button("Simulate"):
                    gg1.simulate_gg1(mean, variance, max, min,server_count)

        elif server_count > 1:

            if model == "M/M/C":
                st.subheader(f"Poisson and Exponential Distributions M/M/{server_count}")
                lam = st.number_input('Enter value of Lambda', value=2.65)
                mu = st.number_input('Enter value of mu', value=1.65)
                if st.button("Simulate"):
                    st.title("M/M/2")
                    mm2_mg2.mm2(lam, mu, server_count)

            elif model == "M/G/C":

                st.subheader(f"Poisson and Uniform Distributions M/G/{server_count}")

                lam = st.number_input('Enter value of Lambda', value=2.65)
                max = st.number_input('Enter value of max', value=10)
                min = st.number_input('Enter value of min', value=5)
                mu = (max+min)/2
                if st.button("Simulate"):
                    st.title("M/G/2")
                    mm2_mg2.mm2(lam, mu, server_count)

            elif model == "G/G/C":

                st.subheader(f"Noraml and Uniform Distributions G/G/{server_count}")
                mean = st.number_input('Enter value of mean', value=9)
                variance = st.number_input('Enter value of variance', value=5)
                max = st.number_input('Enter value of max', value=10)
                min = st.number_input('Enter value of min', value=5)
                if st.button("Simulate"):
                    gg2.simulate_gg2(mean, variance, max, min, server_count)

    elif a == "Queuing model":

        queuing_models.main()



mainInit()
