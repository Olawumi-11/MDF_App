import streamlit as st
from modeci_mdf import *
import matplotlib.pyplot as plt
from modeci_mdf.utils import load_mdf_json
from modeci_mdf.utils import load_mdf


#function to simulate the model

def simulate_model(uploaded_file, dt, duration):
    #load the model and graph from an mdf file
    model = load_mdf(uploaded_file)
    graph = model.graphs[0]   
    #initialize the evaluablegraph with the graph
    eg = EvaluableGraph(graph)
    #initialize lists to record simulation results

    times = []
    velocities = []

    #simulation loop
    t = 0
    while t <= duration:
        eg.evaluate(time_increment=dt)
        velocities.append(eg.enodes["velocity"].evaluable_outputs["output"].curr_value)
        #increment time
        t += dt
        return times, velocities
    

    #simulate the model 
    times, velocities = simulate_model(model_file, dt, duration)

    #plot results
    plt.plot(times, velocities, label="velocity")
    plt.xlabel("Time")
    plt.ylabel("value")
    plt.legend()
    plt.show()

# Streamlit  GRAPHIC UI

st.markdown("<h1 style ='text-align:center;'> MDF Model Simulation Web App </h1>", unsafe_allow_html=True)

# Project Description 
st.markdown("<h2 style ='text-align:center;'> Project Description </h2>", unsafe_allow_html=True)

st.markdown("""
<p style='text-align :left;'>This is a simple web application that allows users to upload standard MDF files containing model descriptions. After uploading an MDF file, the application reads the model description and display a graphical summary to the user. This application also allow  Users to modify some input parameters of the model, such as initial conditions, simulation settings, or other relevant parameters. The appplication then executes the model based on the user-specified parameters and displays the simulation results to the user.</p>
""", unsafe_allow_html=True)


st.markdown("***", unsafe_allow_html=True)


# File upload 
st.markdown("<h3 style ='text-align:center;'> Upload MDF File </h3>", unsafe_allow_html=True)
uploaded_files = st.file_uploader("choose one or more files", accept_multiple_files=True,type=["ipynb", "json", "yaml"])

if uploaded_files is not None:
    for uploaded_file in uploaded_files:
        st.write("file uploaded")
        file_name = uploaded_file.name
        file_content = uploaded_file.read()
        st.subheader("Uploaded File Summary")
        st.write("file_content", file_content)
        st.write("uploaded file type:", type(uploaded_file))
        st.write("File Name:", uploaded_file.name)
        st.write("File size:", uploaded_file.size, "bytes")



        def load_mdf_from_json(uploaded_file):
             
             model = load_mdf_json(uploaded_file)
             return model
        

        
        
       

        
        
        
        def display_model_summary(model):
            st.subheader("Model Summary")


            #number of nodes
            num_nodes = len(model.graphs[0].nodes)
            st.write(f"Number of nodes: {num_nodes}")


            num_parameters = sum(len(node.parameters) for node in model.graphs[0].nodes)
            st.write(f"Number of inputs: {num_inputs}")



            num_ouputs = sum(len(node.outputs) for node in model.graphs[0].nodes)
            st.write(f"Number of Outputs: {num_outputs}")



            num_connections = sum(len(node.connections) for node in model.graphs[0].nodes)
            st.write(f"Number of Connections: {num_connections}")


            model = load_mdf_from_json(uploaded_file)
            display_model_summary(model)
else:
     st.write("You need to upload a file to proceed")
         




st.markdown("***", unsafe_allow_html=True)  

#Allow users to modify parameters

st.markdown("<h3 style ='text-align:center;'>Modify Simulation Parameters </h3>", unsafe_allow_html=True)



st.markdown("""<p style='text-align :left;'>The slider below allows you to modify simulation parameters such as the time derivative and the duration, use the slider to select new values for time derivative and duration for the simulation process.</p>
""", unsafe_allow_html=True)

#Define default values for parameters

default_parameters_values = {
    "dt" : 0.01,
    "duration" :1
}


#create sliders for each parameter
user_parameters = {}
for param_name, default_value in default_parameters_values.items():
        default_value = float(default_value)
        user_input = st.slider(param_name, min_value=0.1, max_value=10.0,value=default_value,step=0.1)
        user_parameters[param_name] = user_input

    
        

st.markdown("***", unsafe_allow_html=True)

st.markdown("""<p style='text-align :left;'>Click on the <strong>Run Simulation</strong> button below to execute the model with the new set of parameters you specified.</p>""",unsafe_allow_html=True)
# Create Simulation button

if st.button("**Run Simulation**"):
        st.write("Simulation running....")
        #extract dt and duration from user parameters

        dt = user_parameters.get("dt", 0.01) #default value of 0.1 if not found
        duration = user_parameters.get("duration", 1) #default value of 1 if not found


        simulation_results =simulate_model(uploaded_file, dt,  duration)

        #display simulation results
        st.subheaderheader("Simulation Results")
        #Extract simulation results
        times, velocities = simulation_results

         #plot simulation results
        
        fig.ax = plt.subplots()
        ax.plot(times, velocities)
        ax.set_xlabel("Time")
        ax.set_ylabel("velocity")
        ax.set_titles("Simulation Results: Time vs Velocity")
        #Display plot to the user
        st.pyplot(fig)



        

    

       
        
       
        
        
       

       

        
        
        
    