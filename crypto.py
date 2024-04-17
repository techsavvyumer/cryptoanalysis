import streamlit as st
import yfinance as yf
import datetime
import plotly.graph_objects as go

# Function to fetch crypto data with error handling
def get_crypto_data(symbol, start_date=None, end_date=None):
    try:
        # Download data for the given symbol
        crypto_data = yf.download(symbol, start=start_date, end=end_date)
        return crypto_data
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {e}")
        return None
    
# Function to create logout button
def logout_button(session_state):
    if st.button("Logout", key="logout_sidebar"):
        session_state.logged_in = False

# Main function
def app(session_state):
    st.title("Crypto Price Chart")

    # Sidebar for symbol selection and date range
    # st.sidebar.header("Select Crypto")
    # symbol = st.sidebar.selectbox("Choose Crypto", ["BTC-USD", "ETH-USD", "ADA-USD"])

    # default_start_date = (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
    # default_end_date = datetime.date.today().strftime('%Y-%m-%d')
    # start_date_str = st.sidebar.text_input("Start Date (YYYY-MM-DD)", default_start_date)
    # end_date_str = st.sidebar.text_input("End Date (YYYY-MM-DD)", default_end_date)

    # Streamlit date input
    td = datetime.datetime.now()
    this_year = td.year
    jan_1 = datetime.date(this_year, 1, 1)
    dec_31 = datetime.date(this_year, 12, 31)
    
    
    with st.sidebar:
        symbol = st.sidebar.selectbox("Choose Crypto", ["BTC-USD", "ETH-USD", "ADA-USD"])
        d = st.date_input("Select Crypto Period:", (datetime.date(td.year, td.month, td.day-7), datetime.date(td.year, td.month, td.day)), jan_1, dec_31, format="YYYY.MM.DD")
        logout_button(session_state)

    # Validate and convert date strings
    # try:
    #     start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
    #     end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None
    # except ValueError:
    #     st.error("Invalid date format. Please use YYYY-MM-DD.")
    #     return
    start_date = d[0]
    end_date = d[1]
    # symbol = "BTC-USD"
    # Fetch crypto data
    crypto_data = get_crypto_data(symbol, start_date, end_date)

    # Check if data was fetched successfully
    if crypto_data is not None:
        st.subheader(f"{symbol} Price Data")
        st.dataframe(crypto_data)  # Display all data points

        # Create line chart with flexibility for other chart types
        st.subheader(f"{symbol} Price Line Chart")
        st.line_chart(crypto_data[["Open", "High", "Low", "Close"]])

        # Create candlestick chart
        st.subheader(f"{symbol} Price Candlestick Chart")
        fig = go.Figure(data=[go.Candlestick(x=crypto_data.index,
                                             open=crypto_data['Open'],
                                             high=crypto_data['High'],
                                             low=crypto_data['Low'],
                                             close=crypto_data['Close'])])
        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)
        
        # Create animation of price line chart
        st.subheader(f"{symbol} Price Animation")
        fig_animation = go.Figure()
        fig_animation.add_trace(go.Scatter(x=crypto_data.index, y=crypto_data['Close'], mode='lines', name='Price'))
        fig_animation.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig_animation, use_container_width=True)
        
        # create another plot for the volume of the crypto
        st.subheader(f"{symbol} Volume")
        st.line_chart(crypto_data['Volume'])
        
        # create another plot for the volume of the crypto
        
        # show all time high and all time low price of the selected crypto
        st.subheader(f"All Time High and Low Price")
        st.write(f"All Time High Price: {crypto_data['High'].max()}")
        st.write(
            
            f"All Time Low Price: {crypto_data['Low'].min()}")
        # also show the maximum percentage increase and decrease in the price
        st.subheader(f"Maximum Percentage Increase and Decrease")
        st.write(f"Maximum Percentage Increase: {((crypto_data['High'].max() - crypto_data['Low'].min()) / crypto_data['Low'].min()) * 100}%")
        
# if __name__ == "__main__":
#     main()