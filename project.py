import pandas as pd
import psycopg2
import streamlit as st
import time
from configparser import ConfigParser

"# Welcome to KMisha - Our Travel Agency Portal for Employees and Customers!"
#//
@st.cache
def get_config(filename="database.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    for k, v in parser.items(section):
        print(k + "=" + v)
    return {k: v for k, v in parser.items(section)}

@st.cache
def query_db(sql: str):
    # print(f"Running query_db(): {sql}")

    db_info = get_config()
    #st.set_page_config()


    # Connect to an existing database
    conn = psycopg2.connect(**db_info)

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute(sql)

    # Obtain data
    data = cur.fetchall()

    column_names = [desc[0] for desc in cur.description]

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    df = pd.DataFrame(data=data, columns=column_names)

    return df

def insert_db(sql: str):
    db_info = get_config()
    conn = psycopg2.connect(**db_info)

    cur = conn.cursor()
    #st.write(cur)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()


'## Things Our Travel Agency Offers'
'Hello fellow Traveler:) Are you ready for your next adventure?'
''
"Look no further than KMisha Travel Agency! Our team of experienced travel experts will help you plan the perfect vacation, no matter your budget or travel preferences."
''

"""Whether you\'re looking for a romantic getaway, a thrilling adventure, or a relaxing beach trip, we have something for everyone. We offer personalized itineraries, competitive prices, and top-notch customer service to ensure that your trip is everything you've dreamed of and more.
            Don\'t spend hours scouring the internet for the best deals – let us do the work for you. From booking flights and hotels to arranging activities and transportation, we\'ll take care of all the details. All you have to do is sit back, relax, and start packing!
            Don\'t miss out on your dream vacation."""

'######  Contact KMisha Travel Agency today and start planning the trip of a lifetime. Book now and get ready to make memories that will last a lifetime!'
''

#First section---------------------------------------------------------------------------------------------
"### ------------------------------------------------------------------------------"
"### Please select your role at KMisha"
page_names1=['Employee', 'Customer']
page1=st.radio('Are you an Employee or a Customer', page_names1)
#Employee section-----------------------------------------------------------------------------------------
if page1 == 'Employee':

    #Question_1-----------------------------------------------------------------------------------------------

    # "Everything you need to know about our popular agency is here!"
    # sql_all_table_names = "SELECT relname FROM pg_class WHERE relkind='r' AND relname !~ '^(pg_|sql_)';"
    # try:
    #     all_table_names = query_db(sql_all_table_names)["relname"].tolist()
    #     table_name = st.selectbox("What are you here for today", all_table_names)
    # except Exception as e:
    #     st.write("Sorry! Something went wrong with your query, please try again.")
    #
    # if table_name:
    #     f"Here you go!"
    #
    #     sql_table = f"SELECT * FROM {table_name};"
    #     try:
    #         df = query_db(sql_table)
    #         st.dataframe(df)
    #     except:
    #         st.write(
    #             "Sorry! Something went wrong with your query, please try again."
    #         )

#Popular employee representation through radio buttons--------------------------------------------------------------------------------------------

    "## Appreciation Time!!"
    page_names_1=['Most popular agent among our customers', 'Marketing team rep who brought most business to KMisha']
    page_1=st.radio('Here are KMisha\'s top performers', page_names_1)
    if page_1 == 'Most popular agent among our customers':
        try:
            Var11=f"""select A.name, count(O.Agent_SSN) as Highest_booking_count 
                      from Makes_Travel_order O, Agent_Works_with A 
                      where O.Agent_SSN=A.SSN 
                      group by A.Name 
                      order by Highest_booking_count desc limit 1;"""
            df = query_db(Var11)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)
    elif page_1 == 'Marketing team rep who brought most business to KMisha':
        try:
            Var22=f"""select M.Name, count(Order_id) as Customer_association_count
                      from Marketing_team M, Agent_Works_with WW, Makes_Travel_order MTO
                      where M.SSN = WW.Marketing_team_SSN
                      and WW.SSN = MTO.Agent_SSN 
                      group by M.Name
                      order by Customer_association_count desc limit 1;"""
            df = query_db(Var22)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)
#Org structure-------------------------------------------------------------------------------------------------------------------------------------
    "## Information about ORG structure, Commissions and Company revenue"

    page_names_11=['Hierarchical structure of our organisation', 'Know about all Agents\' commissions', 'Know about Supervisors\' additional commissions','Total Revenue of the company']
    page_11=st.radio('Choose an option-', page_names_11)
    #Organisation structure-----------------------------------------------
    if page_11 == 'Hierarchical structure of our organisation':
        try:
            "See the organisation structure here"
            Var12=f"""select WW2.Name as Supervisor, WW1.Name as Subordinate
                      from Report_to RT, Agent_Works_with WW1, Agent_Works_with WW2
                      where RT.Supervisor_SSN = WW2.SSN
                      and RT.Subordinate_SSN = WW1.SSN
                      order by WW2.Name;"""
            df = query_db(Var12)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)
    #Our agents commissions-------------------------------------------
    if page_11 == 'Know about all Agents\' commissions':
        try:
            """Here are the commission details-- Agent's commission is based on Hotel price for each booking and its corresponding rating. 
            For eg. if rating is above average, commission is 5% of the room price.
            If rating is below average, the commission is 3% of the booking price."""

            Var13=f"""Create view A_commission as
                      (select WW.Name, WW.SSN, (Price_in_usd * 5)/100 as Agent_commission_in_usd 
                      from Agent_Works_with WW, Makes_Travel_order MTO, Travel_order_consists_of_Trip_details TD, Hotel H1
                      where H1.rating >= (select avg(H2.rating) from Hotel H2)
                      and MTO.Agent_SSN = WW.SSN
                      and TD.Travel_order_Order_id = MTO.Order_id
                      and TD.Hotel_Registration_no = H1.Registration_no
                      
                      UNION
                        
                      select WW.Name, WW.SSN, (Price_in_usd * 3)/100 as Agent_commission_in_usd
                      from Agent_Works_with WW, Makes_Travel_order MTO, Travel_order_consists_of_Trip_details TD, Hotel H1
                      where H1.rating < (select avg(H2.rating) from Hotel H2)
                      and MTO.Agent_SSN = WW.SSN
                      and TD.Travel_order_Order_id = MTO.Order_id
                      and TD.Hotel_Registration_no = H1.Registration_no);"""

            Var14=f""" select name, ssn, sum(Agent_commission_in_usd) as Total_Commission
                        from A_commission
                        group by name, ssn
                        order by Total_Commission desc;"""

            df = query_db(Var14)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)
    # Supervisors' Commission----------------------------------------------
    if page_11 == 'Know about Supervisors\' additional commissions':
        try:
            "Supervisors get additional 15% commission on their subordinates' commission value."
            Var16 = f"""create view A_total_commission as
                        (select name, ssn, sum(Agent_commission_in_usd) as Total_Commission
                        from A_commission
                        group by name, ssn
                        order by Total_Commission desc);"""


            Var171= f"""select OS.supervisor, (sum(AC.total_commission)*15)/100 as Supervisor_Commission
                        from Org_struct OS, A_total_commission AC
                        where OS.subordinate_ssn = AC.ssn 
                        group by OS.supervisor
                        order by OS.supervisor;"""
            df = query_db(Var171)
            st.write(f"{df.loc[0]}")
            st.dataframe(df.style.format({"supervisor_commission":"{:.2f}"}))
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)
    #Company revenue---------------------------------------------------

    if page_11 == 'Total Revenue of the company':
        try:
            "Our total revenue is calculated as-- 20% (Transport cost + Hotel cost) per booking + Agency's fee per booking which is 100 usd."
            Var14=f"""select ((select sum(T1.Fare_in_usd)* 20/100 from Transport T1) + (select sum(H1.Price_in_usd) * 20/100 from Hotel H1) 
                      + (select count(T1.Fare_in_usd) * 100 from Transport T1))
                        as Revenue;"""

            df = query_db(Var14)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)

    #BEST DEALS:--------------------
    "## Some budget friendly options for your customer"
    # page_names_100=['See if you can get better deals than this']
    # page_100=st.radio('Popular deals', page_names_100)
    # if page_100 == 'See if you can get better deals than this':
    "Here is the comparison of some best deals our talented agents landed before-- We are showing a comparison between our various partner Hotels and their Room_type pairs, where first pair's rating higher than or equal to the other but the price is lower, hence making it as better deal for our customers."
    Var15=f"""select H1.Name as Hotel1_Name, H1.Room_type as Room1_type, H1.rating as Rating1, 
             H1.Price_in_usd as Price1, H2.Name as Hotel2_Name, H2.Room_type as Room2_type, H2.Rating as Rating2, H2.Price_in_usd as Price2
             from Hotel H1, Hotel H2
             where H1.Room_type = H2.Room_type
             and H1.Name != H2.Name
             and H1.Rating > H2.Rating
             and H1.Price_in_usd < H2.Price_in_usd
             order by Price1;"""

    df = query_db(Var15)
    st.dataframe(df)
        # except Exception as e:
        #     st.write(
        #         "Sorry! Something went wrong with your query, please try again."
        #     )
        #     st.write(e)

#Question_3-------------------------------------------------------------------------------------------------------------------------------

    "## Agent Info based on their Names"
    a_names = "select Name from Agent_Works_with;"
    try:
        agent_names = query_db(a_names)["name"].tolist()
        agent_name = st.selectbox("Choose an Agent to see the booking they have worked on..", agent_names)
    except Exception as e:
        st.write("Sorry! Something went wrong with your query, please try again.")
        st.write(e)

    if agent_name:
        sql_q = f"""
                select TD.Travel_order_Order_id, TD.Location_city, TD.Location_country 
                from Travel_order_consists_of_Trip_details TD, Makes_Travel_order MTO, Agent_Works_with WI 
                where WI.Name = '{agent_name}' and TD.Travel_order_Order_id = MTO.Order_id and MTO.Agent_SSN = WI.SSN 
                group by TD.Travel_order_Order_id, TD.Location_city, TD.Location_country 
                order by TD.Travel_order_Order_id;"""
        #print(sql_q)
        try:
            agent_info_all = query_db(sql_q)
            #print(agent_info_all)
            agent_info = agent_info_all.loc[0]
            #print(agent_info)
            Order_id, City_loc, Country_loc  = (
                agent_info["travel_order_order_id"],
                agent_info["location_city"],
                agent_info["location_country"],
            )
            st.write(f" Order Number: {Order_id} is booked for {City_loc}, {Country_loc}")
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)

#Traveler section of page------------------------------------------------------------------------------------------------

elif page1 == 'Customer':
    name=st.text_input('Name:')
    contact=st.text_input('Contact Number:')
    ssn= st.text_input('Social Security Number:')
    if st.button("SIGN UP"):

        Var200=f"INSERT INTO traveler_advise VALUES ('{ssn}', '{name}', '{contact}' ,'821318681');"

        Var300 = f"Select * from traveler_advise;"

        insert_db(Var200)
        df3 = query_db(Var300)
        #ax.text(color="b", ha="center", va="center", fontweight="bold",fontsize='25')
        st.write('Thank you for signing up with KMisha, your Information is safe with us. Our travel agent will get back to you shortly!')
    ''
    "We would like to show you some of the most popular packages opted by our beloved customers"
    page_names=['Most booked destinations by our customers each year', 'World famous festivals which you can be a part of', 'Our customers\' top favourite Hotels in each country', 'Looking for a road trip? Here are some customized plans made for our customers, we can make one for you as well!!']
    page=st.radio('Explore the packages here..', page_names)
    if page == 'Most booked destinations by our customers each year':
        try:
            Var3=f"""select TD.Location_country, MTO.Travel_year 
                     from Makes_Travel_order MTO, Travel_order_consists_of_Trip_details TD 
                     where MTO.Order_id = TD.Travel_order_Order_id 
                     group by MTO.Travel_year, TD.Location_country 
                     order by count(TD.Location_country), MTO.Travel_year desc;"""
            df = query_db(Var3)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)
    if page == 'World famous festivals which you can be a part of':
        try:
            Var1=f"""select festival as Festival_name, country, city, festival_month 
                     from Offers_Travel_plans 
                     where festival is not null group by festival, country, city, Festival_month 
                     order by Country;"""
            df = query_db(Var1)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)

    if page == 'Our customers\' top favourite Hotels in each country':
        try:
            Var4=f"select Name as Hotel_Name, Country from Hotel group by Name, Country;"
            df = query_db(Var4)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)

    if page == 'Looking for a road trip? Here are some customized plans made for our customers, we can make one for you as well!!':
        try:
            Var5=f"""select Transportation_mode, Travelling_from_country, Travelling_from_city, Travelling_to_country, Travelling_to_city 
                     from Transport 
                     where Transportation_mode = 'Train' or  Transportation_mode = 'Road' 
                     order by Transportation_mode; """
            df = query_db(Var5)
            st.dataframe(df)
        except Exception as e:
            st.write(
                "Sorry! Something went wrong with your query, please try again."
            )
            st.write(e)


