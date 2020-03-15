#----------------------------------
# This code gives us the information of conncetions between users in different categories (rumor tweeter, anti rumor tweeter, antirumor retweeter, antirumor retweeter)
# This information includes the rates of connection (both in terms of followings and followers) for nodes of each category with nodes of other categories
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
    Connections_Between_Categories (G_Directed_with_Attributes,path_output)
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
#-------------------------------------------------------------------
# This function gives the fraction of connections between nodes of each 4 main categories
def Connections_Between_Categories (G_Directed_with_Attributes,path_output) :
    import numpy as np
    import ast
    

    TotalNumberOfTweeterRumorNodes = 0
    TotalNumberOfRetweeterRumorNodes = 0
    TotalNumberOfTweeterAntiRumorNodes = 0
    TotalNumberOfRetweeterAntiRumorNodes = 0        

    for nid in G_Directed_with_Attributes.Nodes ():
        if G_Directed_with_Attributes.GetStrAttrDatN(nid, "State_of_User"):
            SU = G_Directed_with_Attributes.GetStrAttrDatN(nid, "State_of_User")
            SU = ast.literal_eval(SU)
            if SU[0] == 'RT' :
                TotalNumberOfTweeterRumorNodes += 1
            elif SU[0] == 'RR' :
                TotalNumberOfRetweeterRumorNodes += 1
            elif SU[0] == 'AT' :
                TotalNumberOfTweeterAntiRumorNodes += 1
            elif SU[0] == 'AR' :
                TotalNumberOfRetweeterAntiRumorNodes += 1
            else :
                None


    Tweeter_Rumor_Follow_Tweeter_Rumor = []
    Tweeter_Rumor_Follow_Tweeter_Rumor_f = []
    Tweeter_Rumor_Follow_Retweeter_Rumor = []
    Tweeter_Rumor_Follow_Retweeter_Rumor_f = []
    Tweeter_Rumor_Follow_Tweeter_AntiRumor = []
    Tweeter_Rumor_Follow_Tweeter_AntiRumor_f = []
    Tweeter_Rumor_Follow_Retweeter_AntiRumor = []
    Tweeter_Rumor_Follow_Retweeter_AntiRumor_f = []
    Tweeter_Rumor_Followed_by_Tweeter_Rumor = []
    Tweeter_Rumor_Followed_by_Tweeter_Rumor_f = []
    Tweeter_Rumor_Followed_by_Retweeter_Rumor = []
    Tweeter_Rumor_Followed_by_Retweeter_Rumor_f = []
    Tweeter_Rumor_Followed_by_Tweeter_AntiRumor = []
    Tweeter_Rumor_Followed_by_Tweeter_AntiRumor_f = []
    Tweeter_Rumor_Followed_by_Retweeter_AntiRumor = []
    Tweeter_Rumor_Followed_by_Retweeter_AntiRumor_f = []
    
    Retweeter_Rumor_Follow_Tweeter_Rumor = []
    Retweeter_Rumor_Follow_Tweeter_Rumor_f = []
    Retweeter_Rumor_Follow_Retweeter_Rumor = []
    Retweeter_Rumor_Follow_Retweeter_Rumor_f = []
    Retweeter_Rumor_Follow_Tweeter_AntiRumor = []
    Retweeter_Rumor_Follow_Tweeter_AntiRumor_f = []
    Retweeter_Rumor_Follow_Retweeter_AntiRumor = []
    Retweeter_Rumor_Follow_Retweeter_AntiRumor_f = []
    Retweeter_Rumor_Followed_by_Tweeter_Rumor = []
    Retweeter_Rumor_Followed_by_Tweeter_Rumor_f = []
    Retweeter_Rumor_Followed_by_Retweeter_Rumor = []
    Retweeter_Rumor_Followed_by_Retweeter_Rumor_f = []
    Retweeter_Rumor_Followed_by_Tweeter_AntiRumor = []
    Retweeter_Rumor_Followed_by_Tweeter_AntiRumor_f = []
    Retweeter_Rumor_Followed_by_Retweeter_AntiRumor = []
    Retweeter_Rumor_Followed_by_Retweeter_AntiRumor_f = []
    

    Tweeter_AntiRumor_Follow_Tweeter_Rumor = []
    Tweeter_AntiRumor_Follow_Tweeter_Rumor_f = []
    Tweeter_AntiRumor_Follow_Retweeter_Rumor = []
    Tweeter_AntiRumor_Follow_Retweeter_Rumor_f = []
    Tweeter_AntiRumor_Follow_Tweeter_AntiRumor = []
    Tweeter_AntiRumor_Follow_Tweeter_AntiRumor_f = []
    Tweeter_AntiRumor_Follow_Retweeter_AntiRumor = []
    Tweeter_AntiRumor_Follow_Retweeter_AntiRumor_f = []
    Tweeter_AntiRumor_Followed_by_Tweeter_Rumor = []
    Tweeter_AntiRumor_Followed_by_Tweeter_Rumor_f = []
    Tweeter_AntiRumor_Followed_by_Retweeter_Rumor = []
    Tweeter_AntiRumor_Followed_by_Retweeter_Rumor_f = []
    Tweeter_AntiRumor_Followed_by_Tweeter_AntiRumor = []
    Tweeter_AntiRumor_Followed_by_Tweeter_AntiRumor_f = []
    Tweeter_AntiRumor_Followed_by_Retweeter_AntiRumor = []
    Tweeter_AntiRumor_Followed_by_Retweeter_AntiRumor_f = []

    Retweeter_AntiRumor_Follow_Tweeter_Rumor = []
    Retweeter_AntiRumor_Follow_Tweeter_Rumor_f = []
    Retweeter_AntiRumor_Follow_Retweeter_Rumor = []
    Retweeter_AntiRumor_Follow_Retweeter_Rumor_f = []
    Retweeter_AntiRumor_Follow_Tweeter_AntiRumor = []
    Retweeter_AntiRumor_Follow_Tweeter_AntiRumor_f = []
    Retweeter_AntiRumor_Follow_Retweeter_AntiRumor = []
    Retweeter_AntiRumor_Follow_Retweeter_AntiRumor_f = []
    Retweeter_AntiRumor_Followed_by_Tweeter_Rumor = []
    Retweeter_AntiRumor_Followed_by_Tweeter_Rumor_f = []
    Retweeter_AntiRumor_Followed_by_Retweeter_Rumor = []
    Retweeter_AntiRumor_Followed_by_Retweeter_Rumor_f = []
    Retweeter_AntiRumor_Followed_by_Tweeter_AntiRumor = []
    Retweeter_AntiRumor_Followed_by_Tweeter_AntiRumor_f = []
    Retweeter_AntiRumor_Followed_by_Retweeter_AntiRumor = []
    Retweeter_AntiRumor_Followed_by_Retweeter_AntiRumor_f = []
    
    j = 0
    for NI in G_Directed_with_Attributes.Nodes():
        if G_Directed_with_Attributes.GetStrAttrDatN(NI, "State_of_User"):
            SU = G_Directed_with_Attributes.GetStrAttrDatN(NI, "State_of_User")
            SU = ast.literal_eval(SU)
            if SU[0] == 'RT' :
                OutDeg = NI.GetOutDeg()
                InDeg = NI.GetInDeg()
                OutDeg_indx = 0
                InDeg_indx = 0
                Number_out_neighbors = []
                Number_In_neighbors = []
                while OutDeg_indx < OutDeg:
                    Number_out_neighbors.append (NI.GetOutNId(OutDeg_indx))
                    OutDeg_indx += 1
                while InDeg_indx < InDeg:
                    Number_In_neighbors.append (NI.GetInNId(InDeg_indx))
                    InDeg_indx += 1
                

                # Counting the connections of Tweeter Rumor and Other 3 Categories
                # Out neighbors (those nodes who are followed by Tweeter Rumor nodes)
                no_to_tr = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RT' :
                            no_to_tr += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_tr)/float (OutDeg_indx)), 'FOTR')
                if TotalNumberOfTweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_tr)/float (TotalNumberOfTweeterRumorNodes)), 'FTRaO')

                no_to_rr = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RR':
                            no_to_rr += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_rr)/float (OutDeg_indx)), 'FORR')
                if TotalNumberOfRetweeterRumorNodes != 0 : 
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_rr)/float (TotalNumberOfRetweeterRumorNodes)), 'FRRaO')
                
                no_to_ta = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AT':
                            no_to_ta += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ta)/float (OutDeg_indx)), 'FOTA')
                if TotalNumberOfTweeterAntiRumorNodes != 0 : 
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ta)/float (TotalNumberOfTweeterAntiRumorNodes)), 'FTAaO')

                
                no_to_ra = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AR':
                            no_to_ra += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ra)/float (OutDeg_indx)), 'FORA')
                if TotalNumberOfRetweeterAntiRumorNodes != 0 : 
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ra)/float (TotalNumberOfRetweeterAntiRumorNodes)), 'FRAaO')
                
                # In neighbors (those nodes who follow the Tweeter Rumor nodes)
                ni_to_tr = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RT' :
                            ni_to_tr += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_tr)/float (InDeg_indx)), 'FITR')
                if TotalNumberOfTweeterRumorNodes != 0 : 
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_tr)/float (TotalNumberOfTweeterRumorNodes)), 'FTRaI')


                ni_to_rr = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RR':
                            ni_to_rr += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_rr)/float (InDeg_indx)), 'FIRR')
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_rr)/float (TotalNumberOfRetweeterRumorNodes)), 'FRRaI')

                
                ni_to_ta = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AT':
                            ni_to_ta += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ta)/float (InDeg_indx)), 'FITA')
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ta)/float (TotalNumberOfTweeterAntiRumorNodes)), 'FTAaI')
                
                ni_to_ra = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AR':
                            ni_to_ra += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ra)/float (InDeg_indx)), 'FIRA')
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ra)/float (TotalNumberOfRetweeterAntiRumorNodes)), 'FRAaI')

                    
            elif SU[0] == 'RR' :
                OutDeg = NI.GetOutDeg()
                InDeg = NI.GetInDeg()
                OutDeg_indx = 0
                InDeg_indx = 0
                Number_out_neighbors = []
                Number_In_neighbors = []
                while OutDeg_indx < OutDeg:
                    Number_out_neighbors.append (NI.GetOutNId(OutDeg_indx))
                    OutDeg_indx += 1
                while InDeg_indx < InDeg:
                    Number_In_neighbors.append (NI.GetInNId(InDeg_indx))
                    InDeg_indx += 1

                        
                # Counting the connections of Retweeter_Rumor and Other 3 Categories
                # Out neighbors (those nodes who are followed by Retweeter Rumor nodes)
                no_to_tr = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RT' :
                            no_to_tr += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_tr)/float (OutDeg_indx)), 'FOTR')
                if TotalNumberOfTweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_tr)/float (TotalNumberOfTweeterRumorNodes)), 'FTRaO')
                

                no_to_rr = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RR' :
                            no_to_rr += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_rr)/float (OutDeg_indx)), 'FORR')
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_rr)/float (TotalNumberOfRetweeterRumorNodes)), 'FRRaO')


                no_to_ta = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AT' :
                            no_to_ta += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ta)/float (OutDeg_indx)), 'FOTA')
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ta)/float (TotalNumberOfTweeterAntiRumorNodes)), 'FTAaO')

                
                no_to_ra = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AR' :
                            no_to_ra += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ra)/float (OutDeg_indx)), 'FORA')
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ra)/float (TotalNumberOfRetweeterAntiRumorNodes)), 'FRAaO')
                
                # In neighbors (those nodes who follow the Retweeter Rumor nodes)
                ni_to_tr = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RT' :
                            ni_to_tr += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_tr)/float (InDeg_indx)), 'FITR')
                if TotalNumberOfTweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_tr)/float (TotalNumberOfTweeterRumorNodes)), 'FTRaI')
                

                ni_to_rr = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RR' :
                            ni_to_rr += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_rr)/float (InDeg_indx)), 'FIRR')
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_rr)/float (TotalNumberOfRetweeterRumorNodes)), 'FRRaI')

                ni_to_ta = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AT' :
                            ni_to_ta += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ta)/float (InDeg_indx)), 'FITA')
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ta)/float (TotalNumberOfTweeterAntiRumorNodes)), 'FTAaI')
                
                ni_to_ra = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AR' :
                            ni_to_ra += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ra)/float (InDeg_indx)), 'FIRA')
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ra)/float (TotalNumberOfRetweeterAntiRumorNodes)), 'FRAaI')

                    
            elif SU[0] == 'AT' :
                OutDeg = NI.GetOutDeg()
                InDeg = NI.GetInDeg()
                OutDeg_indx = 0
                InDeg_indx = 0
                Number_out_neighbors = []
                Number_In_neighbors = []
                while OutDeg_indx < OutDeg:
                    Number_out_neighbors.append (NI.GetOutNId(OutDeg_indx))
                    OutDeg_indx += 1
                while InDeg_indx < InDeg:
                    Number_In_neighbors.append (NI.GetInNId(InDeg_indx))
                    InDeg_indx += 1


                # Counting the connections of Tweeter_AntiRumor and Other 3 Categories
                # Out neighbors (those nodes who are followed by Tweeter AntiRumor nodes)
                no_to_tr = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RT' :
                            no_to_tr += 1

                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_tr)/float (OutDeg_indx)), 'FOTR')
                if TotalNumberOfTweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_tr)/float (TotalNumberOfTweeterRumorNodes)), 'FTRaO')

                
                no_to_rr = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RR' :
                            no_to_rr += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_rr)/float (OutDeg_indx)), 'FORR')
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_rr)/float (TotalNumberOfRetweeterRumorNodes)), 'FRRaO')
                

                no_to_ta = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AT' :
                            no_to_ta += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ta)/float (OutDeg_indx)), 'FOTA')
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ta)/float (TotalNumberOfTweeterAntiRumorNodes)), 'FTAaO')


                no_to_ra = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AR' :
                            no_to_ra += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ra)/float (OutDeg_indx)), 'FORA')
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ra)/float (TotalNumberOfRetweeterAntiRumorNodes)), 'FRAaO')
                
                
                # In neighbors (those nodes who follow the Tweeter AntiRumor nodes)
                ni_to_tr = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RT' :
                            ni_to_tr += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_tr)/float (InDeg_indx)), 'FITR')
                if TotalNumberOfTweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_tr)/float (TotalNumberOfTweeterRumorNodes)), 'FTRaI')
                
                ni_to_rr = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RR' :
                            ni_to_rr += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_rr)/float (InDeg_indx)), 'FIRR')
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_rr)/float (TotalNumberOfRetweeterRumorNodes)), 'FRRaI')
                
                ni_to_ta = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AT' :
                            ni_to_ta += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ta)/float (InDeg_indx)), 'FITA')
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ta)/float (TotalNumberOfTweeterAntiRumorNodes)), 'FTAaI')

                ni_to_ra = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AR' :
                            ni_to_ra += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ra)/float (InDeg_indx)), 'FIRA')
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ra)/float (TotalNumberOfRetweeterAntiRumorNodes)), 'FRAaI')
                           
            elif SU[0] == 'AR' :
                OutDeg = NI.GetOutDeg()
                InDeg = NI.GetInDeg()
                OutDeg_indx = 0
                InDeg_indx = 0
                Number_out_neighbors = []
                Number_In_neighbors = []
                while OutDeg_indx < OutDeg:
                    Number_out_neighbors.append (NI.GetOutNId(OutDeg_indx))
                    OutDeg_indx += 1
                while InDeg_indx < InDeg:
                    Number_In_neighbors.append (NI.GetInNId(InDeg_indx))
                    InDeg_indx += 1
                

                # Counting the connections of Tweeter_AntiRumor and Other 3 Categories
                # Out neighbors (those nodes who are followed by Tweeter AntiRumor nodes)
                no_to_tr = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RT' :
                            no_to_tr += 1

                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_tr)/float (OutDeg_indx)), 'FOTR')
                if TotalNumberOfTweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_tr)/float (TotalNumberOfTweeterRumorNodes)), 'FTRaO')
                
                no_to_rr = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RR' :
                            no_to_tr += 1


                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_rr)/float (OutDeg_indx)), 'FORR')
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_rr)/float (TotalNumberOfRetweeterRumorNodes)), 'FRRaO')
                                        
                no_to_ta = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AT' :
                            no_to_ta += 1

                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ta)/float (OutDeg_indx)), 'FOTA')
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ta)/float (TotalNumberOfTweeterAntiRumorNodes)), 'FTAaO')

                no_to_ra = 0        
                for no in Number_out_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(no, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AR' :
                            no_to_ra += 1
                if OutDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ra)/float (OutDeg_indx)), 'FORA')
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (no_to_ra)/float (TotalNumberOfRetweeterAntiRumorNodes)), 'FRAaO')
                
                # In neighbors (those nodes who follow the Tweeter AntiRumor nodes)
                ni_to_tr = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RT' :
                            ni_to_tr += 1
                
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_tr)/float (InDeg_indx)), 'FITR')
                if TotalNumberOfTweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_tr)/float (TotalNumberOfTweeterRumorNodes)), 'FTRaI')
                
                ni_to_rr = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'RR' :
                            ni_to_rr += 1

                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_rr)/float (InDeg_indx)), 'FIRR')
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_rr)/float (TotalNumberOfRetweeterRumorNodes)), 'FRRaI')
                
                ni_to_ta = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AT' :
                            ni_to_ta += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ta)/float (InDeg_indx)), 'FITA')
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ta)/float (TotalNumberOfTweeterAntiRumorNodes)), 'FTAaI')

                ni_to_ra = 0        
                for ni in Number_In_neighbors:
                    if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                        SUN = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                        SUN = ast.literal_eval(SUN)
                        if SUN[0] == 'AR' :
                            ni_to_ra += 1
                if InDeg_indx !=0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ra)/float (InDeg_indx)), 'FIRA')
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    G_Directed_with_Attributes.AddFltAttrDatN(NI, (float (ni_to_ra)/float (TotalNumberOfRetweeterAntiRumorNodes)), 'FRAaI')
                                            
                    
            j+=1


    for NI in G_Directed_with_Attributes.Nodes ():
        OutDeg = NI.GetOutDeg()
        InDeg = NI.GetInDeg()
        if G_Directed_with_Attributes.GetStrAttrDatN(NI, "State_of_User"):
            SU = G_Directed_with_Attributes.GetStrAttrDatN(NI, "State_of_User")
            SU = ast.literal_eval(SU)
            if SU[0] == 'RT' :
                if OutDeg !=0 :
                    Tweeter_Rumor_Follow_Tweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FOTR'))
                    Tweeter_Rumor_Follow_Retweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FORR'))
                    Tweeter_Rumor_Follow_Tweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FOTA'))
                    Tweeter_Rumor_Follow_Retweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FORA'))
                if InDeg !=0 :
                    Tweeter_Rumor_Followed_by_Tweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FITR'))
                    Tweeter_Rumor_Followed_by_Retweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FIRR'))
                    Tweeter_Rumor_Followed_by_Tweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FITA'))
                    Tweeter_Rumor_Followed_by_Retweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FIRA'))
                if TotalNumberOfTweeterRumorNodes != 0 :
                    Tweeter_Rumor_Follow_Tweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTRaO'))
                    Tweeter_Rumor_Followed_by_Tweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTRaI'))
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    Tweeter_Rumor_Follow_Retweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRRaO'))
                    Tweeter_Rumor_Followed_by_Retweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRRaI'))
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    Tweeter_Rumor_Follow_Tweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTAaO'))
                    Tweeter_Rumor_Followed_by_Tweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTAaI'))
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    Tweeter_Rumor_Follow_Retweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRAaO'))
                    Tweeter_Rumor_Followed_by_Retweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRAaI'))

            elif SU[0] == 'RR' :
                if OutDeg !=0 :
                    Retweeter_Rumor_Follow_Tweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FOTR'))
                    Retweeter_Rumor_Follow_Retweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FORR'))
                    Retweeter_Rumor_Follow_Tweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FOTA'))
                    Retweeter_Rumor_Follow_Retweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FORA'))
                if InDeg !=0 :
                    Retweeter_Rumor_Followed_by_Tweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FITR'))
                    Retweeter_Rumor_Followed_by_Retweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FIRR'))
                    Retweeter_Rumor_Followed_by_Tweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FITA'))
                    Retweeter_Rumor_Followed_by_Retweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FIRA'))
                if TotalNumberOfTweeterRumorNodes != 0 : 
                    Retweeter_Rumor_Follow_Tweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTRaO'))
                    Retweeter_Rumor_Followed_by_Tweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTRaI'))
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    Retweeter_Rumor_Follow_Retweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRRaO'))
                    Retweeter_Rumor_Followed_by_Retweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRRaI'))
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    Retweeter_Rumor_Follow_Tweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTAaO'))
                    Retweeter_Rumor_Followed_by_Tweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTAaI'))
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    Retweeter_Rumor_Follow_Retweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRAaO'))
                    Retweeter_Rumor_Followed_by_Retweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRAaI'))
                    
            elif SU[0] == 'AT' :
                if OutDeg !=0 :
                    Tweeter_AntiRumor_Follow_Tweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FOTR'))
                    Tweeter_AntiRumor_Follow_Retweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FORR'))
                    Tweeter_AntiRumor_Follow_Tweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FOTA'))
                    Tweeter_AntiRumor_Follow_Retweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FORA'))
                if InDeg !=0 :
                    Tweeter_AntiRumor_Followed_by_Tweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FITR'))
                    Tweeter_AntiRumor_Followed_by_Retweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FIRR'))
                    Tweeter_AntiRumor_Followed_by_Tweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FITA'))
                    Tweeter_AntiRumor_Followed_by_Retweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FIRA'))
                if TotalNumberOfTweeterRumorNodes != 0 : 
                    Tweeter_AntiRumor_Follow_Tweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTRaO'))
                    Tweeter_AntiRumor_Followed_by_Tweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTRaI'))
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    Tweeter_AntiRumor_Follow_Retweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRRaO'))
                    Tweeter_AntiRumor_Followed_by_Retweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRRaI'))
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    Tweeter_AntiRumor_Follow_Tweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTAaO'))
                    Tweeter_AntiRumor_Followed_by_Tweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTAaI'))
                if TotalNumberOfRetweeterAntiRumorNodes != 0 : 
                    Tweeter_AntiRumor_Follow_Retweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRAaO'))
                    Tweeter_AntiRumor_Followed_by_Retweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRAaI'))
                    
            elif SU[0] == 'AR' :
                if OutDeg !=0 :
                    Retweeter_AntiRumor_Follow_Tweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FOTR'))
                    Retweeter_AntiRumor_Follow_Retweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FORR'))
                    Retweeter_AntiRumor_Follow_Tweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FOTA'))
                    Retweeter_AntiRumor_Follow_Retweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FORA'))
                if InDeg !=0 :
                    Retweeter_AntiRumor_Followed_by_Tweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FITR'))
                    Retweeter_AntiRumor_Followed_by_Retweeter_Rumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FIRR'))
                    Retweeter_AntiRumor_Followed_by_Tweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FITA'))
                    Retweeter_AntiRumor_Followed_by_Retweeter_AntiRumor.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FIRA'))
                if TotalNumberOfTweeterRumorNodes != 0 :
                    Retweeter_AntiRumor_Follow_Tweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTRaO'))
                    Retweeter_AntiRumor_Followed_by_Tweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTRaI'))
                if TotalNumberOfRetweeterRumorNodes != 0 :
                    Retweeter_AntiRumor_Follow_Retweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRRaO'))
                    Retweeter_AntiRumor_Followed_by_Retweeter_Rumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRRaI'))
                if TotalNumberOfTweeterAntiRumorNodes != 0 :
                    Retweeter_AntiRumor_Follow_Tweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTAaO'))
                    Retweeter_AntiRumor_Followed_by_Tweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FTAaI'))
                if TotalNumberOfRetweeterAntiRumorNodes != 0 :
                    Retweeter_AntiRumor_Follow_Retweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRAaO'))
                    Retweeter_AntiRumor_Followed_by_Retweeter_AntiRumor_f.append (G_Directed_with_Attributes.GetFltAttrDatN(NI, 'FRAaI'))
         
            else :
                None

    text_file = open(path_output + "S18_4_Output.txt", "a")
    text_file.write('######################################' "\n")
    text_file.write('Connections of Tweeter Rumor Nodes to Other Categories' "\n")
    text_file.write("Each Tweeter Rumor Node has this fraction of its followings devoted to Tweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_Rumor_Follow_Tweeter_Rumor)) , float(np.std (Tweeter_Rumor_Follow_Tweeter_Rumor))))
    text_file.write("Each Tweeter Rumor Node has this fraction of Tweeter Rumor Nodes as its followings (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_Rumor_Follow_Tweeter_Rumor_f)) , float(np.std (Tweeter_Rumor_Follow_Tweeter_Rumor_f))))       

    text_file.write("Each Tweeter Rumor Node has this fraction of its followings devoted to Retweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_Rumor_Follow_Retweeter_Rumor)) , float(np.std (Tweeter_Rumor_Follow_Retweeter_Rumor))))
    text_file.write("Each Tweeter Rumor Node has this fraction of Retweeter Rumor Nodes as its followings (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_Rumor_Follow_Retweeter_Rumor_f)) , float(np.std (Tweeter_Rumor_Follow_Retweeter_Rumor_f))))       

    text_file.write("Each Tweeter Rumor Node has this fraction of its followings devoted to Tweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_Rumor_Follow_Tweeter_AntiRumor)) , float(np.std (Tweeter_Rumor_Follow_Tweeter_AntiRumor))))
    text_file.write("Each Tweeter Rumor Node has this fraction of Tweeter AntiRumor Nodes as its followings (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_Rumor_Follow_Tweeter_AntiRumor_f)) , float(np.std (Tweeter_Rumor_Follow_Tweeter_AntiRumor_f))))       

    text_file.write("Each Tweeter Rumor Node has this fraction of its followings devoted to Retweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_Rumor_Follow_Retweeter_AntiRumor)) , float(np.std (Tweeter_Rumor_Follow_Retweeter_AntiRumor))))
    text_file.write("Each Tweeter Rumor Node has this fraction of Retweeter AntiRumor Nodes as its followings (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_Rumor_Follow_Retweeter_AntiRumor_f)) , float(np.std (Tweeter_Rumor_Follow_Retweeter_AntiRumor_f))))       
                                                                                          
    text_file.write("Each Tweeter Rumor Node has this fraction of its followers devoted to Tweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_Rumor_Followed_by_Tweeter_Rumor)) , float(np.std (Tweeter_Rumor_Followed_by_Tweeter_Rumor))))
    text_file.write("Each Tweeter Rumor Node has this fraction of Tweeter Rumor Nodes as its followers (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_Rumor_Followed_by_Tweeter_Rumor_f)) , float(np.std (Tweeter_Rumor_Followed_by_Tweeter_Rumor_f))))       

    text_file.write("Each Tweeter Rumor Node has this fraction of its followers devoted to Retweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_Rumor_Followed_by_Retweeter_Rumor)) , float(np.std (Tweeter_Rumor_Followed_by_Retweeter_Rumor))))
    text_file.write("Each Tweeter Rumor Node has this fraction of Retweeter Rumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_Rumor_Followed_by_Retweeter_Rumor_f)) , float(np.std (Tweeter_Rumor_Followed_by_Retweeter_Rumor_f))))

    text_file.write("Each Tweeter Rumor Node has this fraction of its followers devoted to Tweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_Rumor_Followed_by_Tweeter_AntiRumor)) , float(np.std (Tweeter_Rumor_Followed_by_Tweeter_AntiRumor))))
    text_file.write("Each Tweeter Rumor Node has this fraction of Tweeter AntiRumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_Rumor_Followed_by_Tweeter_AntiRumor_f)) , float(np.std (Tweeter_Rumor_Followed_by_Tweeter_AntiRumor_f))))
                                                                                                                                                                                                
    text_file.write("Each Tweeter Rumor Node has this fraction of its followers devoted to Retweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_Rumor_Followed_by_Retweeter_AntiRumor)) , float(np.std (Tweeter_Rumor_Followed_by_Retweeter_AntiRumor))))
    text_file.write("Each Tweeter Rumor Node has this fraction of Retweeter AntiRumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_Rumor_Followed_by_Retweeter_AntiRumor_f)) , float(np.std (Tweeter_Rumor_Followed_by_Retweeter_AntiRumor_f))))
    
    text_file.write('====================================================================' "\n")
    text_file.write('Connections of Retweeter Rumor Node to Other Categories' "\n")

    text_file.write("Each Retweeter Rumor Node has this fraction of its followings devoted to Tweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_Rumor_Follow_Tweeter_Rumor)) , float(np.std (Retweeter_Rumor_Follow_Tweeter_Rumor))))
    text_file.write("Each Retweeter Rumor Node has this fraction of Tweeter Rumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_Rumor_Follow_Tweeter_Rumor_f)) , float(np.std (Retweeter_Rumor_Follow_Tweeter_Rumor_f))))

    text_file.write("Each Retweeter Rumor Node has this fraction of its followings devoted to Retweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_Rumor_Follow_Retweeter_Rumor)) , float(np.std (Retweeter_Rumor_Follow_Retweeter_Rumor))))
    text_file.write("Each Retweeter Rumor Node has this fraction of Retweeter Rumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_Rumor_Follow_Retweeter_Rumor_f)) , float(np.std (Retweeter_Rumor_Follow_Retweeter_Rumor_f))))
                                                                                          
    text_file.write("Each Retweeter Rumor Node has this fraction of its followings devoted to Tweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_Rumor_Follow_Tweeter_AntiRumor)) , float(np.std (Retweeter_Rumor_Follow_Tweeter_AntiRumor))))
    text_file.write("Each Retweeter Rumor Node has this fraction of Tweeter AntiRumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_Rumor_Follow_Tweeter_AntiRumor_f)) , float(np.std (Retweeter_Rumor_Follow_Tweeter_AntiRumor_f))))

    text_file.write("Each Retweeter Rumor Node has this fraction of its followings devoted to Retweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_Rumor_Follow_Retweeter_AntiRumor)) , float(np.std (Retweeter_Rumor_Follow_Retweeter_AntiRumor))))
    text_file.write("Each Retweeter Rumor Node has this fraction of Retweeter AntiRumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_Rumor_Follow_Retweeter_AntiRumor_f)) , float(np.std (Retweeter_Rumor_Follow_Retweeter_AntiRumor_f))))
            
    text_file.write("Each Retweeter Rumor Node has this fraction of its followers devoted to Tweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_Rumor_Followed_by_Tweeter_Rumor)) , float(np.std (Retweeter_Rumor_Followed_by_Tweeter_Rumor))))
    text_file.write("Each Retweeter Rumor Node has this fraction of Tweeter Rumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_Rumor_Followed_by_Tweeter_Rumor_f)) , float(np.std (Retweeter_Rumor_Followed_by_Tweeter_Rumor_f))))
                                                                                          
    text_file.write("Each Retweeter Rumor Node has this fraction of its followers devoted to Retweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_Rumor_Followed_by_Retweeter_Rumor)) , float(np.std (Retweeter_Rumor_Followed_by_Retweeter_Rumor))))
    text_file.write("Each Retweeter Rumor Node has this fraction of Retweeter Rumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_Rumor_Followed_by_Retweeter_Rumor_f)) , float(np.std (Retweeter_Rumor_Followed_by_Retweeter_Rumor_f))))
                                                                                          
    text_file.write("Each Retweeter Rumor Node has this fraction of its followers devoted to Tweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_Rumor_Followed_by_Tweeter_AntiRumor)) , float(np.std (Retweeter_Rumor_Followed_by_Tweeter_AntiRumor))))
    text_file.write("Each Retweeter Rumor Node has this fraction of Tweeter AntiRumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_Rumor_Followed_by_Tweeter_AntiRumor_f)) , float(np.std (Retweeter_Rumor_Followed_by_Tweeter_AntiRumor_f))))

    text_file.write("Each Retweeter Rumor Node has this fraction of its followers devoted to Retweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_Rumor_Followed_by_Retweeter_AntiRumor)) , float(np.std (Retweeter_Rumor_Followed_by_Retweeter_AntiRumor))))
    text_file.write("Each Retweeter Rumor Node has this fraction of Retweeter AntiRumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_Rumor_Followed_by_Retweeter_AntiRumor_f)) , float(np.std (Retweeter_Rumor_Followed_by_Retweeter_AntiRumor_f))))

    text_file.write('====================================================================' "\n")
    text_file.write('Connections of Tweeter AntiRumor Node to Other Categories' "\n")

    text_file.write("Each Tweeter AntiRumor Node has this fraction of its followings devoted to Tweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Follow_Tweeter_Rumor)) , float(np.std (Tweeter_AntiRumor_Follow_Tweeter_Rumor))))
    text_file.write("Each Tweeter AntiRumor Node has this fraction of Tweeter Rumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Follow_Tweeter_Rumor_f)) , float(np.std (Tweeter_AntiRumor_Follow_Tweeter_Rumor_f))))

    text_file.write("Each Tweeter AntiRumor Node has this fraction of its followings devoted to Retweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Follow_Retweeter_Rumor)) , float(np.std (Tweeter_AntiRumor_Follow_Retweeter_Rumor))))
    text_file.write("Each Tweeter AntiRumor Node has this fraction of Retweeter Rumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Follow_Retweeter_Rumor_f)) , float(np.std (Tweeter_AntiRumor_Follow_Retweeter_Rumor_f))))
                                                                                          
    text_file.write("Each Tweeter AntiRumor Node has this fraction of its followings devoted to Tweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Follow_Tweeter_AntiRumor)) , float(np.std (Tweeter_AntiRumor_Follow_Tweeter_AntiRumor))))
    text_file.write("Each Tweeter AntiRumor Node has this fraction of Tweeter AntiRumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Follow_Tweeter_AntiRumor_f)) , float(np.std (Tweeter_AntiRumor_Follow_Tweeter_AntiRumor_f))))

    text_file.write("Each Tweeter AntiRumor Node has this fraction of its followings devoted to Retweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Follow_Retweeter_AntiRumor)) , float(np.std (Tweeter_AntiRumor_Follow_Retweeter_AntiRumor))))
    text_file.write("Each Tweeter AntiRumor Node has this fraction of Retweeter AntiRumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Follow_Retweeter_AntiRumor_f)) , float(np.std (Tweeter_AntiRumor_Follow_Retweeter_AntiRumor_f))))
                                                                                          
    text_file.write("Each Tweeter AntiRumor Node has this fraction of its followers devoted to Tweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Followed_by_Tweeter_Rumor)) , float(np.std (Tweeter_AntiRumor_Followed_by_Tweeter_Rumor))))
    text_file.write("Each Tweeter AntiRumor Node has this fraction of Tweeter Rumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Followed_by_Tweeter_Rumor_f)) , float(np.std (Tweeter_AntiRumor_Followed_by_Tweeter_Rumor_f))))
                                                                                          
    text_file.write("Each Tweeter AntiRumor Node has this fraction of its followers devoted to Retweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Followed_by_Retweeter_Rumor)) , float(np.std (Tweeter_AntiRumor_Followed_by_Retweeter_Rumor))))
    text_file.write("Each Tweeter AntiRumor Node has this fraction of Retweeter Rumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Followed_by_Retweeter_Rumor_f)) , float(np.std (Tweeter_AntiRumor_Followed_by_Retweeter_Rumor_f))))
                                                                                          
    text_file.write("Each Tweeter AntiRumor Node has this fraction of its followers devoted to Tweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Followed_by_Tweeter_AntiRumor)) , float(np.std (Tweeter_AntiRumor_Followed_by_Tweeter_AntiRumor))))
    text_file.write("Each Tweeter AntiRumor Node has this fraction of Tweeter Rumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Followed_by_Tweeter_AntiRumor_f)) , float(np.std (Tweeter_AntiRumor_Followed_by_Tweeter_AntiRumor_f))))

    text_file.write("Each Tweeter AntiRumor Node has this fraction of its followers devoted to Retweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Followed_by_Retweeter_AntiRumor)) , float(np.std (Tweeter_AntiRumor_Followed_by_Retweeter_AntiRumor))))
    text_file.write("Each Tweeter AntiRumor Node has this fraction of Retweeter AntiRumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Tweeter_AntiRumor_Followed_by_Retweeter_AntiRumor_f)) , float(np.std (Tweeter_AntiRumor_Followed_by_Retweeter_AntiRumor_f))))

    text_file.write('====================================================================' "\n")
    text_file.write('Connections of Retweeter AntiRumor Node to Other Categories' "\n")
    
    text_file.write("Each Retweeter AntiRumor Node has this fraction of its followings devoted to Tweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Follow_Tweeter_Rumor)) , float(np.std (Retweeter_AntiRumor_Follow_Tweeter_Rumor))))
    text_file.write("Each Retweeter AntiRumor Node has this fraction of Tweeter Rumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Follow_Tweeter_Rumor_f)) , float(np.std (Retweeter_AntiRumor_Follow_Tweeter_Rumor_f))))

    text_file.write("Each Retweeter AntiRumor Node has this fraction of its followings devoted to Retweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Follow_Retweeter_Rumor)) , float(np.std (Retweeter_AntiRumor_Follow_Retweeter_Rumor))))
    text_file.write("Each Retweeter AntiRumor Node has this fraction of Retweeter Rumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Follow_Retweeter_Rumor_f)) , float(np.std (Retweeter_AntiRumor_Follow_Retweeter_Rumor_f))))

    text_file.write("Each Retweeter AntiRumor Node has this fraction of its followings devoted to Tweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Follow_Tweeter_AntiRumor)) , float(np.std (Retweeter_AntiRumor_Follow_Tweeter_AntiRumor))))
    text_file.write("Each Retweeter AntiRumor Node has this fraction of Tweeter AntiRumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Follow_Tweeter_AntiRumor_f)) , float(np.std (Retweeter_AntiRumor_Follow_Tweeter_AntiRumor_f))))
                                                                                          
    text_file.write("Each Retweeter AntiRumor Node has this fraction of its followings devoted to Retweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Follow_Retweeter_AntiRumor)) , float(np.std (Retweeter_AntiRumor_Follow_Retweeter_AntiRumor))))
    text_file.write("Each Retweeter AntiRumor Node has this fraction of Retweeter AntiRumor Nodes as its followings  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Follow_Retweeter_AntiRumor_f)) , float(np.std (Retweeter_AntiRumor_Follow_Retweeter_AntiRumor_f))))

    text_file.write("Each Retweeter AntiRumor Node has this fraction of its followers devoted to Tweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Followed_by_Tweeter_Rumor)) , float(np.std (Retweeter_AntiRumor_Followed_by_Tweeter_Rumor))))
    text_file.write("Each Retweeter AntiRumor Node has this fraction of Tweeter Rumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Followed_by_Tweeter_Rumor_f)) , float(np.std (Retweeter_AntiRumor_Followed_by_Tweeter_Rumor_f))))
                                                                                          
    text_file.write("Each Retweeter AntiRumor Node has this fraction of its followers devoted to Retweeter Rumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Followed_by_Retweeter_Rumor)) , float(np.std (Retweeter_AntiRumor_Followed_by_Retweeter_Rumor))))
    text_file.write("Each Retweeter AntiRumor Node has this fraction of Retweeter Rumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Followed_by_Retweeter_Rumor_f)) , float(np.std (Retweeter_AntiRumor_Followed_by_Retweeter_Rumor_f))))

    text_file.write("Each Retweeter AntiRumor Node has this fraction of its followers devoted to Tweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Followed_by_Tweeter_AntiRumor)) , float(np.std (Retweeter_AntiRumor_Followed_by_Tweeter_AntiRumor))))
    text_file.write("Each Retweeter AntiRumor Node has this fraction of Tweeter AntiRumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Followed_by_Tweeter_AntiRumor_f)) , float(np.std (Retweeter_AntiRumor_Followed_by_Tweeter_AntiRumor_f))))

    text_file.write("Each Retweeter AntiRumor Node has this fraction of its followers devoted to Retweeter AntiRumor Nodes (Mean , SD) : " "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Followed_by_Retweeter_AntiRumor)) , float(np.std (Retweeter_AntiRumor_Followed_by_Retweeter_AntiRumor))))
    text_file.write("Each Retweeter AntiRumor Node has this fraction of Retweeter AntiRumor Nodes as its followers  (Mean , SD) : "  "%s %s\n" % (float(np.mean (Retweeter_AntiRumor_Followed_by_Retweeter_AntiRumor_f)) , float(np.std (Retweeter_AntiRumor_Followed_by_Retweeter_AntiRumor_f))))

    text_file.write('====================================================================' "\n")
    text_file.close()

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
