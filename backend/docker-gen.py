import streamlit as st

def generate_dockerfile(base_image, dependencies, port, command, env_vars, steps_order):
    dockerfile_content = f"FROM {base_image}\n\n"
    
    for step in steps_order:
        if step == "Set WORKDIR":
            dockerfile_content += "WORKDIR /app\n"
        elif step == "Copy Files":
            dockerfile_content += "COPY . /app\n"
        elif step == "Install Dependencies":
            for dependency in dependencies:
                dockerfile_content += f"RUN pip install {dependency}\n"
        elif step == "Expose Port":
            dockerfile_content += f"EXPOSE {port}\n"
        elif step == "Set Environment Variables":
            for var_name, var_value in env_vars.items():
                dockerfile_content += f"ENV {var_name}={var_value}\n"
        elif step == "Run Command":
            dockerfile_content += f'CMD ["{command}"]\n'
    
    return dockerfile_content

def main():
    st.title("Dockerfile Generator")
    
    base_image = st.text_input("Enter the base image (e.g., python:3.9-slim): ")
    port = st.text_input("Enter the port your application uses (default is 5000): ", value="5000")
    command = st.text_input("Enter the command to run your application (e.g., 'python app.py'): ")

    # Initialize session state if not already present
    if 'dependencies' not in st.session_state:
        st.session_state['dependencies'] = []
    
    if 'env_vars' not in st.session_state:
        st.session_state['env_vars'] = {}
    
    if 'steps_order' not in st.session_state:
        st.session_state['steps_order'] = ["Set WORKDIR", "Copy Files", "Install Dependencies", "Expose Port", "Set Environment Variables", "Run Command"]

    # Dependency Management
    def add_dependency():
        st.session_state['dependencies'].append('')
    
    def remove_dependency():
        if st.session_state['dependencies']:
            st.session_state['dependencies'].pop()
            
    col1 , col2 = st.columns(2)
    with col1:
        st.button("Add Dependency", on_click=add_dependency)
    with col2:
        st.button("Remove Dependency", on_click=remove_dependency)
    
    for i, dependency in enumerate(st.session_state['dependencies']):
        st.session_state['dependencies'][i] = st.text_input(f"Dependency {i+1}", value=dependency, key=f"dependency_{i}")
    
    # Environment Variables Management
    def add_env_var():
        st.session_state['env_vars'][f'ENV_VAR_{len(st.session_state["env_vars"]) + 1}'] = ''

    def remove_env_var():
        if st.session_state['env_vars']:
            last_key = list(st.session_state['env_vars'].keys())[-1]
            st.session_state['env_vars'].pop(last_key)
    col1 , col2 = st.columns(2)
    with col1:
        st.button("Add Environment Variable", on_click=add_env_var)
    with col2:
        st.button("Remove Environment Variable", on_click=remove_env_var)
    
    for var_name in list(st.session_state['env_vars'].keys()):
        var_value = st.session_state['env_vars'][var_name]
        st.session_state['env_vars'][var_name] = st.text_input(f"{var_name}", value=var_value, key=f"env_var_{var_name}")

    # Step Reordering
    st.write("### Reorder Dockerfile Instructions")
    st.session_state['steps_order'] = st.multiselect(
        "Order the steps as you want them to appear in the Dockerfile",
        ["Set WORKDIR", "Copy Files", "Install Dependencies", "Expose Port", "Set Environment Variables", "Run Command"],
        default=st.session_state['steps_order']
    )

    # Generate Dockerfile
    if st.button("Generate Dockerfile"):
        dockerfile_content = generate_dockerfile(base_image, st.session_state['dependencies'], port, command, st.session_state['env_vars'], st.session_state['steps_order'])
        
        # Display the Dockerfile content in a text area
        st.text_area("Generated Dockerfile", value=dockerfile_content, height=400)
        
        # Allow the user to download the Dockerfile
        st.download_button(label="Download Dockerfile", data=dockerfile_content, file_name="Dockerfile", mime="text/plain")

if __name__ == "__main__":
    main()