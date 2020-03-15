#----------------------------------
# This code gives the general information about the graph 
#----------------------------------
def main ():
    import json
    import snap
    import graphviz
    import matplotlib.pyplot as plt
    import numpy as np
    import xlrd
    #-----------------
    #The common area
    rumor_number = "21"

    path_input = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 18\\Rumor_'+ rumor_number +'\\Input\\'
    workbook_input1_D = xlrd.open_workbook(path_input + 'DATASET.xlsx', on_demand = True)
    
    path_jsonl = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 18\\Rumor_'+ rumor_number +'\\Input\\Rumor_' + rumor_number + '.jsonl'
    path_graph = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 18\\Rumor_'+ rumor_number +'\\Input\\Rumor_' + rumor_number + '.graph'

    path_output  = 'D:\\Papers\\Social Network Mining\\Analysis_of_Rumor_Dataset\\Step 18\\Rumor_'+ rumor_number +'\\Output\\'

    FIn = snap.TFIn(path_graph)
    G_Directed = snap.TNGraph.Load(FIn)        
    G_Directed_with_Attributes = snap.ConvertGraph(snap.PNEANet, G_Directed) #Convert Directed Graph to Directed Graph with attributes: it means now we can assign attributes to the graph nodes
    G_Directed_with_Attributes = Get_Graph_with_Attributes_New (path_jsonl, G_Directed_with_Attributes, workbook_input1_D)
    #-----------------
    #The specific area
    snap.PrintInfo(G_Directed_with_Attributes, "Python type PNEANet", path_output + "S18_5_Output.txt", False)
#--------------------------------
def Get_Graph_with_Attributes_New (path_jsonl, G_Directed_with_Attributes, workbook_input1_D) :
        #---------------------------------
        # Reading Excel File
        worksheet1_input_D = workbook_input1_D.sheet_by_name('Sheet1')
        
        ID_USERS = worksheet1_input_D.col_values(0)
        NAME_USERS = worksheet1_input_D.col_values(1)
        N_Tweets = worksheet1_input_D.col_values(3)
        Date_time_creation_account = worksheet1_input_D.col_values(4)
        Timezone = worksheet1_input_D.col_values(6)
        N_Followers = worksheet1_input_D.col_values(8)
        N_Friends = worksheet1_input_D.col_values(9)
        Date_Time = worksheet1_input_D.col_values(10)
        N_Favorite = worksheet1_input_D.col_values(11)
        Retweeted_Screen_Name = worksheet1_input_D.col_values(12)
        N_Retweet = worksheet1_input_D.col_values(13)
        Tweet_ID = worksheet1_input_D.col_values(21)
        Retweet_ID = worksheet1_input_D.col_values(23)
        Frequency_of_Tweet_Occurance = worksheet1_input_D.col_values(27)
        State_of_Tweet = worksheet1_input_D.col_values(28)


        del ID_USERS[0]
        del NAME_USERS[0]
        del N_Tweets [0]
        del Date_time_creation_account [0]
        del Timezone [0]
        del N_Followers [0]
        del N_Friends [0]
        del Date_Time [0]
        del N_Favorite [0]
        del Retweeted_Screen_Name [0]
        del N_Retweet [0]
        del Tweet_ID [0]
        del Retweet_ID [0]
        del Frequency_of_Tweet_Occurance [0]
        del State_of_Tweet [0]

        # Reading Jsonl File
        All_ID = []
        with open(path_jsonl, 'r') as f:
            for line in f :
                    x = len(line)  
                    All_ID.append (int(line[0:x-1])) #if we just simply use  All_ID.append (line) then we would have each element of All_ID as an ID + an empty line, so to delete that empty line we wrote the code like this

        del All_ID[0] #B.E C.A.R.E.F.U.L.L  the first line only says the number of nodes and I.S N.O.T A N.O.D.E  I.D , so the number of nodes is x-1
        #---------------------------------
        #---------------------------------
        # Giving the attributes (User_ID and User_Category) to the graph nodes
        h = 0
        base_time = Date_Time [-1]
        for ni in G_Directed_with_Attributes.Nodes():
                Tweet_ID_All = []
                Retweet_ID_All = []
                N_Retweet_All = []
                Retweeted_Screen_Name_All = []
                Date_Time_All = []
                State_of_User_All = []
                N_of_Tweet_Occurance_All = []

                G_Directed_with_Attributes.AddStrAttrDatN(ni, str (All_ID[h]), "User_ID")
                if int (All_ID[h]) in ID_USERS:
                        indx = ID_USERS.index(int (All_ID[h]))
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, NAME_USERS[indx], "NAME_USERS")
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(int(N_Tweets[indx])), "N_Tweets")
                        DTCA = Date_time_creation_account[indx]
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, DTCA[:4], "Date_Creation_Account")
                        if Timezone[indx] :
                                G_Directed_with_Attributes.AddStrAttrDatN(ni, Timezone[indx], "Timezone")
                        else :
                                G_Directed_with_Attributes.AddStrAttrDatN(ni, 'NoTimeZone', "Timezone")
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(int(N_Followers[indx])), "N_Followers")
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(int(N_Friends[indx])), "N_Friends")                     
                        N_occurrence_user_in_dataset = [index for index, value in enumerate(ID_USERS) if value == (int (All_ID[h]))]
                        N_o = len (N_occurrence_user_in_dataset)
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(N_o), "N_Occurrence_user_in_dataset")
                        f = 1
                        
                        for i in N_occurrence_user_in_dataset:
                                Tweet_ID_All.append (str(int(float(Tweet_ID[i]))))                                
                                
                                if Retweet_ID[i] != 'Not a Retweet' :
                                        Retweet_ID_All.append (str(int(float(Retweet_ID[i]))))
                                else :
                                        Retweet_ID_All.append ("NoRetID")

                                N_Retweet_All.append (str(int(float(N_Retweet[i])))) 

                                if Retweeted_Screen_Name[i] :
                                        Retweeted_Screen_Name_All.append (str(Retweeted_Screen_Name[i]))
                                else :
                                        Retweeted_Screen_Name_All.append ("NoRetName")

                                tdf = count_the_time_difference_with_the_base_time (Date_Time[i], base_time)
                                Date_Time_All.append (str(tdf))

                                FTO = Frequency_of_Tweet_Occurance[i]
                                if State_of_Tweet[i] == 'r' :
                                        if Retweet_ID[i] != 'Not a Retweet' :
                                                State_of_User = 'RR' # RR = Rumor Retweeter
                                                State_of_User_All.append(State_of_User)
                                                N_of_Tweet_Occurance_All.append (str(int(float(Frequency_of_Tweet_Occurance[i]))))

                                        elif FTO[0] == 'T' :
                                                State_of_User = 'RT' # RT = Rumor Tweeter
                                                State_of_User_All.append(State_of_User)
                                                N_of_Tweet_Occurance_All.append (str(int(float(Frequency_of_Tweet_Occurance[i][24:-7]))))

                                        else :
                                                State_of_User = 'RT' # RT = Rumor Tweeter
                                                State_of_User_All.append(State_of_User)
                                                N_of_Tweet_Occurance_All.append (str(1))
                                                
             
                                elif State_of_Tweet[i] == 'a' :
                                        if Retweet_ID[i] != 'Not a Retweet' :
                                                State_of_User = 'AR' # AR = AntiRumor Retweeter
                                                State_of_User_All.append(State_of_User)
                                                N_of_Tweet_Occurance_All.append (str(int(float(Frequency_of_Tweet_Occurance[i]))))

                                        elif FTO[0] == 'T' :
                                                State_of_User = 'AT' # AT = AntiRumor Tweeter
                                                State_of_User_All.append(State_of_User)
                                                N_of_Tweet_Occurance_All.append (str(int(float(Frequency_of_Tweet_Occurance[i][24:-7]))))

                                        else :
                                                State_of_User = 'AT' # AT = AntiRumor Tweeter
                                                State_of_User_All.append(State_of_User)
                                                N_of_Tweet_Occurance_All.append (str(1))
                                                


                                elif State_of_Tweet[i] == 'q' : 
                                        State_of_User = 'Q' #For questioner we don't care about their status of being Tweeter or Retweeter 
                                        State_of_User_All.append(State_of_User)

                                        if Retweet_ID[i] != 'Not a Retweet' :
                                                N_of_Tweet_Occurance_All.append (str(int(float(Frequency_of_Tweet_Occurance[i]))))

                                        elif FTO[0] == 'T' :
                                                N_of_Tweet_Occurance_All.append (str(int(float(Frequency_of_Tweet_Occurance[i][24:-7]))))

                                        else :
                                                N_of_Tweet_Occurance_All.append (str(1))
                                                

                                else :
                                        State_of_User = 'N' #For not-related users (those whose posts had nothing to do with the rumor story and were captured only by mistake) we don't care about their status of being Tweeter or Retweeter 
                                        State_of_User_All.append(State_of_User)
                                        if Retweet_ID[i] != 'Not a Retweet' :
                                                N_of_Tweet_Occurance_All.append (str(int(float(Frequency_of_Tweet_Occurance[i]))))

                                        elif FTO[0] == 'T' :
                                                N_of_Tweet_Occurance_All.append (str(int(float(Frequency_of_Tweet_Occurance[i][24:-7]))))

                                        else :
                                                N_of_Tweet_Occurance_All.append (str(1))

                                f += 1

                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(Tweet_ID_All), "Tweet_ID")
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(Retweet_ID_All), "Retweet_ID")
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(N_Retweet_All), "N_Retweet")
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(Retweeted_Screen_Name_All), "Retweeted Screen Name")
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(Date_Time_All), "Date_Time")                                                         
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(State_of_User_All), "State_of_User")
                        G_Directed_with_Attributes.AddStrAttrDatN(ni, str(N_of_Tweet_Occurance_All), "N_of_Tweet_Occurance")                                                         

                h+=1
                
        return G_Directed_with_Attributes
#-----------------------------------------
def count_the_time_difference_with_the_base_time (time_of_spreading,base_time):
        from datetime import date
        import ast
        base_time = ast.literal_eval(base_time)
        time_of_spreading = ast.literal_eval(time_of_spreading)
        d1_year = base_time[0]
        if base_time[1] == 'Jan' :
                d1_month = 1
        elif base_time[1] == 'Feb' :
                d1_month = 2
        elif base_time[1] == 'Mar' :
                d1_month = 3
        elif base_time[1] == 'Apr' :
                d1_month = 4
        elif base_time[1] == 'May' :
                d1_month = 5
        elif base_time[1] == 'Jun' :
                d1_month = 6
        elif base_time[1] == 'Jul' :
                d1_month = 7
        elif base_time[1] == 'Aug' :
                d1_month = 8
        elif base_time[1] == 'Sep' :
                d1_month = 9
        elif base_time[1] == 'Oct' :
                d1_month = 10
        elif base_time[1] == 'Nov' :
                d1_month = 11
        elif base_time[1] == 'Dec' :
                d1_month = 12
        d1_day = base_time[2]
        d2_year = time_of_spreading[0]                       
        if time_of_spreading[1] == 'Jan' :
                d2_month = 1
        elif time_of_spreading[1] == 'Feb' :
                d2_month = 2
        elif time_of_spreading[1] == 'Mar' :
                d2_month = 3
        elif time_of_spreading[1] == 'Apr' :
                d2_month = 4
        elif time_of_spreading[1] == 'May' :
                d2_month = 5
        elif time_of_spreading[1] == 'Jun' :
                d2_month = 6
        elif time_of_spreading[1] == 'Jul' :
                d2_month = 7
        elif time_of_spreading[1] == 'Aug' :
                d2_month = 8
        elif time_of_spreading[1] == 'Sep' :
                d2_month = 9
        elif time_of_spreading[1] == 'Oct' :
                d2_month = 10
        elif time_of_spreading[1] == 'Nov' :
                d2_month = 11
        elif time_of_spreading[1] == 'Dec' :
                d2_month = 12                
        d2_day = time_of_spreading[2]
                    
        d1 = date(int(d1_year),int(d1_month),int(d1_day))
        d2 = date(int(d2_year),int(d2_month),int(d2_day))
        time_difference_with_the_base = (abs(d2-d1).days)*86400 + int(time_of_spreading[3][:2])*3600 + int(time_of_spreading[3][3:5])*60 + int(time_of_spreading[3][6:8]) - int(base_time[3][:2])*3600 - int(base_time[3][3:5])*60 - int(base_time[3][6:8]) 

        return time_difference_with_the_base                                                                                                                                                
#-----------------------------------------
main ()
print "################################"
raw_input('press enter key to exit...')

