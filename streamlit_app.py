import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go

# Function to post the data to the API endpoint and get the response


def get_api_response(data):
    api_url = "https://api.andrewireland.co.uk/heatpumpest"
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=data, headers=headers)
    return response.json()


# Map region names to their corresponding index values
region_mapping = {
    "Thames Valley (Heathrow)": 1,
    "South-eastern (Gatwick)": 2,
    "Southern (Hurn)": 3,
    "South-western (Plymouth)": 4,
    "Severn Valley (Filton)": 5,
    "Midland (Elmdon)": 6,
    "W Pennines (Ringway)": 7,
    "North-western (Carlisle)": 8,
    "Borders (Boulmer)": 9,
    "North-eastern (Leeming)": 10,
    "E Pennines (Finningley)": 11,
    "E Anglia (Honington)": 12,
    "W Scotland (Abbotsinch)": 13,
    "E Scotland (Leuchars)": 14,
    "NE Scotland (Dyce)": 15,
    "Wales (Aberporth)": 16,
    "N Ireland (Aldergrove)": 17,
    "NW Scotland (Stornoway)": 18,
}

# Streamlit app


def main():
    st.title("Heat Pump | Rule of Thumb Calculator")

    st.write("Please input the following variables:")

    # Input fields with dropdowns
    insulation_options = [
        "No improvement to insulation",
        "UPVC/Wood Double glazing + loft insulation",
        "UPVC/Wood Double glazing + loft insulation + cavity wall insulation",
    ]
    insulation = st.selectbox("Insulation", insulation_options)

    age_options = [
        "Older than 1970",
        "1970-1995",
        "1996-2005",
        "2006-2010",
        "2010+",
    ]
    age = st.selectbox("Age", age_options)

    region_options = list(region_mapping.keys())
    region = st.selectbox("Region", region_options)

    floor_area = st.number_input("Floor Area (sqm)", value=120)
    indoor_temp = st.number_input("Indoor Temperature (°C)", value=21)
    outdoor_temp = st.number_input("Outdoor Temperature (°C)", value=-1.9)
    hp_scop = st.number_input("Heat Pump SCOP", value=3.69)
    electricity_cost = st.number_input(
        "Electricity Cost (per kWh)", value=0.34)

    # Map the selected region to its corresponding index value
    region_index = region_mapping[region]

    # Create a JSON object with the user-input data
    data = {
        "insulation": insulation,
        "age": age,
        "floorArea": floor_area,
        "region": region_index,
        "indoorTemperature": indoor_temp,
        "outdoorTemperature": outdoor_temp,
        "hpScop": hp_scop,
        "electricityCost": electricity_cost,
    }

    if st.button("Submit"):
        # Get the API response
        api_response = get_api_response(data)

        # Display the annual figures and Heat Pump kW in a card
        st.subheader("Annual Figures")
        st.write(f"Annual kWh: {api_response['annualKWh']:.2f}")
        st.write(f"Annual Cost: £{api_response['annualCost']:.2f}")
        st.write(f"Heat Pump kW: {api_response['heatPumpKw']:.2f}")

        # Create DataFrame for monthly data
        months = [
            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
        ]
        monthly_data = {
            'Month': months,
            'Monthly kWh': api_response['monthlyKWh'],
            'Monthly Cost': api_response['monthlyCost']
        }
        df = pd.DataFrame(monthly_data)

        # Plot interactive graphs using Plotly
        st.subheader("Monthly kWh and Cost")
        fig = go.Figure()
        fig.add_trace(go.Bar(x=df['Month'], y=df['Monthly kWh'], name='kWh'))
        fig.add_trace(
            go.Bar(x=df['Month'], y=df['Monthly Cost'], name='Cost £', marker_color='orange'))

        fig.update_layout(
            title='Monthly kWh and Cost',
            xaxis_title='Month',
            yaxis_title='',
            barmode='group'
        )

        st.plotly_chart(fig)


if __name__ == "__main__":
    main()
