#----------------------------------
# This Code gives us the information of those two tweets with most number of retweets in the graph. Indeed one most popular rumor tweet and the other most popular antirumor tweet
# for these two most populart tweets the following information would be given:
# 1- The information about the spreader of the tweet (source node)
# 2- The inoformation about those users who retweeted this tweet and are follower of the source node (C1 Category)
# 3- The inoformation about those users who retweeted this tweet and are follower of the followers of source node (C2 Category)
# 4- The inoformation about those users who retweeted this tweet and in no way have any path (directed) to the source node in the graph (C-MINUS-1 Category)
# 5- The inoformation about those users who retweeted this tweet and are follower of the source node and also are following of at least one node in C2 Category (C12 Category)
# 6- The inoformation about those users who retweeted this tweet and are follower of the source node and also are not following of any node in C2 Category (C11 Category)
# for the above categories we calculate the following informations:
# ratio of following/follower (mean, stdv)
# Number of antecedents (mean, stdv)
# time delay of spreading with source node (mean, stdv)
# time delay with the first antecedent (mean, stdv)
# number of published tweets per year (mean, stdv)
# Number of antecedents on the opposit side (mean, stdv)
# Correlations (spearman & pearson) between the above characteristics 
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
    rumor_number = "5"

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
    All_Retweeted_Tweets_Data = all_retweeted_tweets (G_Directed_with_Attributes)
    all_retweeter_data (G_Directed_with_Attributes,All_Retweeted_Tweets_Data,path_output)
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
def all_retweeter_data (G_Directed_with_Attributes,All_Retweeted_Tweets_Data,path_output) :
        from scipy.stats import pearsonr
        from scipy.stats import spearmanr
        import statistics 
        from ast import literal_eval
        import snap
        for Retweeted_Tweet_data in All_Retweeted_Tweets_Data :
                C1 = []
                C2 = []
                C_minus_1 = []
                for NI in G_Directed_with_Attributes.Nodes():
                        being_follower_of_source_node = 0
                        being_following_of_source_node = 0
                        being_mutal_friend_of_source_node = 0
                        if G_Directed_with_Attributes.GetStrAttrDatN(NI, "Retweet_ID"):
                                RIList = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(NI, "Retweet_ID"))
                                for RI in RIList :
                                        if RI == Retweeted_Tweet_data[0] :
                                                Retweeter_User_NAME = G_Directed_with_Attributes.GetStrAttrDatN(NI, "NAME_USERS")
                                                RI_index = RIList.index (RI)
                                                Retweeter_Distance_with_Source_Node = snap.GetShortPath(G_Directed_with_Attributes, NI.GetId(), Retweeted_Tweet_data[5], True) #the short distance from the current node to the destination node (the source node of publishing retweet)
                                                TIList = literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(NI, "Tweet_ID"))
                                                Retweeter_Tweet_ID = TIList [RI_index]
                                                Retweeter_User_ID = G_Directed_with_Attributes.GetStrAttrDatN(NI, "User_ID") 
                                                Retweeter_User_NAME = G_Directed_with_Attributes.GetStrAttrDatN(NI, "NAME_USERS")
                                                Retweeter_Date_Creation_Account = G_Directed_with_Attributes.GetStrAttrDatN(NI, "Date_Creation_Account")
                                                Retweeter_N_Posts = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Tweets")
                                                Retweeter_N_Posts_per_Year = (int (Retweeter_N_Posts))/(2019 - int (Retweeter_Date_Creation_Account))
                                                Retweeter_N_Followers = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Followers")
                                                Retweeter_N_Friends = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Friends")
                                                Retweeter_N_Friends_To_N_Followers = (float (Retweeter_N_Friends))/(float (Retweeter_N_Followers))
                                                Retweeter_ID_in_Graph = NI.GetId()
                                                MUTUAL = 0
                                                for NIN in G_Directed_with_Attributes.Nodes():  
                                                        if (NIN.IsOutNId(Retweeter_ID_in_Graph)) and (NIN.IsInNId(Retweeter_ID_in_Graph)) :
                                                                MUTUAL += 1
                                                if float (NI.GetOutDeg()) != 0 :
                                                        Retweeter_Mutal_To_N_Friends = (float (MUTUAL)) / (float (NI.GetOutDeg()))
                                                else:
                                                        Retweeter_Mutal_To_N_Friends = None
                                                DateTimeList = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(NI, "Date_Time"))
                                                Retweeter_Date_Time = DateTimeList [RI_index]
                                                Retweeter_Time_Delay_with_the_Source = int (Retweeter_Date_Time) - int (Retweeted_Tweet_data[7])

                                                Retweeter_number_of_antecedent_spreaders = 0            
                                                Retweeter_time_of_antecedent_spreaders = []
                                                Retweeter_name_of_antecedent_spreaders = []
                                                Retweeter_number_of_antecedent_spreaders_in_the_opposit_state = 0
                                                Retweeter_time_of_antecedent_spreaders_in_the_opposit_state = []
                                                Retweeter_name_of_antecedent_spreaders_in_the_opposit_state = []
                                                NodeVec = snap.TIntV() 
                                                snap.GetNodesAtHop(G_Directed_with_Attributes, NI.GetId(), 1, NodeVec, True) #gives us the followings of the current node                
                                                for item in NodeVec:
                                                        if G_Directed_with_Attributes.GetStrAttrDatN(item, "Retweet_ID") :                                                
                                                                i = 0
                                                                while i < len (literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(item, "Retweet_ID"))) :
                                                                        if literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(item, "Retweet_ID"))[i] == Retweeted_Tweet_data[0] :
                                                                                Date_Time_item = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(item, "Date_Time"))[i]
                                                                                if int (Date_Time_item) < int (Retweeter_Date_Time) :
                                                                                        Retweeter_number_of_antecedent_spreaders += 1
                                                                                        Retweeter_time_of_antecedent_spreaders.append (int (Date_Time_item))
                                                                                        Retweeter_name_of_antecedent_spreaders.append (G_Directed_with_Attributes.GetStrAttrDatN(item, "NAME_USERS"))
                                                                                break
                                                                        i += 1

                                                        if Retweeted_Tweet_data[8][0] == 'R' :
                                                                if G_Directed_with_Attributes.GetStrAttrDatN(item, "State_of_User"):
                                                                        i = 0
                                                                        while i < len (literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(item, "State_of_User"))):
                                                                                if literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(item, "State_of_User"))[i][0] == 'A':
                                                                                        Date_Time_item = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(item, "Date_Time"))[i]
                                                                                        if int (Date_Time_item) < int (Retweeter_Date_Time) :
                                                                                                Retweeter_number_of_antecedent_spreaders_in_the_opposit_state += 1
                                                                                                Retweeter_time_of_antecedent_spreaders_in_the_opposit_state.append (int (Date_Time_item))
                                                                                                Retweeter_name_of_antecedent_spreaders_in_the_opposit_state.append (G_Directed_with_Attributes.GetStrAttrDatN(item, "NAME_USERS"))
                                                                                        break
                                                                                i += 1
                                                                                
                                                        if Retweeted_Tweet_data[8][0] == 'A' :
                                                                if G_Directed_with_Attributes.GetStrAttrDatN(item, "State_of_User"):
                                                                        i = 0
                                                                        while i < len (literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(item, "State_of_User"))):
                                                                                if literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(item, "State_of_User"))[i][0] == 'R':
                                                                                        Date_Time_item = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(item, "Date_Time"))[i]
                                                                                        if int (Date_Time_item) < int (Retweeter_Date_Time) :
                                                                                                Retweeter_number_of_antecedent_spreaders_in_the_opposit_state += 1
                                                                                                Retweeter_time_of_antecedent_spreaders_in_the_opposit_state.append (int (Date_Time_item))
                                                                                                Retweeter_name_of_antecedent_spreaders_in_the_opposit_state.append (G_Directed_with_Attributes.GetStrAttrDatN(item, "NAME_USERS"))
                                                                                        break
                                                                                i += 1


                                                Distances_from_source_which_have_source_node_as_their_first_antecedent = [1,-1,0]
                                                if (int (Retweeter_Distance_with_Source_Node) in Distances_from_source_which_have_source_node_as_their_first_antecedent) or (not Retweeter_time_of_antecedent_spreaders):
                                                        Retweeter_Time_Delay_with_the_First_Antecedent = Retweeter_Time_Delay_with_the_Source
                                                else :
                                                        Retweeter_Time_Delay_with_the_First_Antecedent = int (Retweeter_Date_Time) - int (min(Retweeter_time_of_antecedent_spreaders))


                                                if Retweeter_Mutal_To_N_Friends:
                                                        Retweeter_Time_Delay_with_the_First_Antecedent_Match_with_Mutal = Retweeter_Time_Delay_with_the_First_Antecedent
                                                else :
                                                        Retweeter_Time_Delay_with_the_First_Antecedent_Match_with_Mutal = None
                                                        
                                                UnitData = []
                                                UnitData.append (Retweeter_User_NAME) 
                                                UnitData.append (Retweeter_N_Posts_per_Year) 
                                                UnitData.append (Retweeter_N_Friends_To_N_Followers) 
                                                UnitData.append (Retweeter_Mutal_To_N_Friends) 
                                                UnitData.append (Retweeter_Time_Delay_with_the_Source) 
                                                UnitData.append (Retweeter_Time_Delay_with_the_First_Antecedent) 
                                                UnitData.append (Retweeter_number_of_antecedent_spreaders) 
                                                UnitData.append (Retweeter_name_of_antecedent_spreaders) 
                                                UnitData.append (Retweeter_number_of_antecedent_spreaders_in_the_opposit_state) 
                                                UnitData.append (Retweeter_Time_Delay_with_the_First_Antecedent_Match_with_Mutal) 
                                                


                                                UnitData = tuple (UnitData)
                                                if Retweeter_Distance_with_Source_Node == -1 :
                                                        C_minus_1.append (UnitData)
                                                elif Retweeter_Distance_with_Source_Node == 1 :
                                                        C1.append (UnitData)
                                                elif Retweeter_Distance_with_Source_Node == 2 :
                                                        C2.append (UnitData)
                                                else :
                                                        None


                                                        

                C_minus_1 = tuple (C_minus_1)
                C1 = tuple (C1)
                C2 = tuple (C2)

                C1Names =  []
                C12Names = []
                C12 = []
                C11 = []
                for UNIT in C1:
                        C1Names.append (UNIT[0])  
                for UNIT in C2:
                        for name in UNIT[7] :
                                if name in C1Names:
                                        C12Names.append (name)
                
                for UNIT in C1:
                        if UNIT[0] in C12Names :
                                C12.append (UNIT)
                        else :
                                C11.append (UNIT)

                C11 = tuple (C11)
                C12 = tuple (C12)

                
                text_file = open(path_output + "S18_1_Output.txt", "a")
                text_file.write('######################################' "\n")
                text_file.write("Source : " "%s\n" %  str (Retweeted_Tweet_data))
                text_file.write('\n'"===========")
                text_file.write('\n'"C_minus_1 Characteristics " '\n')            
                if [float (i[2]) for i in C_minus_1] :
                        text_file.write("mean_fw_to_fr : " "%s\n" %  statistics.mean([float (i[2]) for i in C_minus_1]))
                        if len ([float (i[2]) for i in C_minus_1]) > 1 :
                                text_file.write("stdev_fw_to_fr : " "%s\n" %  statistics.stdev([float (i[2]) for i in C_minus_1]))
                if [float (i[3]) for i in C_minus_1 if i[3]] :
                        text_file.write("mean_mutal_to_fw : " "%s\n" %  statistics.mean([float (i[3]) for i in C_minus_1 if i[3]]))
                        if len ([float (i[3]) for i in C_minus_1 if i[3]]) > 1 :
                                text_file.write("stdv_mutal_to_fw : " "%s\n" %  statistics.stdev([float (i[3]) for i in C_minus_1 if i[3]]))
                if [float (i[6]) for i in C_minus_1] :
                        text_file.write("mean_n_antecedents : " "%s\n" % statistics.mean([float (i[6]) for i in C_minus_1]))
                        if len ([float (i[6]) for i in C_minus_1]) > 1 :
                                text_file.write("stdv_n_antecedents : " "%s\n" % statistics.stdev([float (i[6]) for i in C_minus_1]))
                if [float (i[4]) for i in C_minus_1] :
                        text_file.write("mean_time_delay_with_source : " "%s\n" % statistics.mean([float (i[4]) for i in C_minus_1]))
                        if len ([float (i[4]) for i in C_minus_1]) > 1 :
                                text_file.write("stdv_time_delay_with_source : " "%s\n" % statistics.stdev([float (i[4]) for i in C_minus_1]))
                if [float (i[5]) for i in C_minus_1] :
                        text_file.write("mean_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.mean([float (i[5]) for i in C_minus_1]))
                        if len ([float (i[5]) for i in C_minus_1]) > 1 :
                                text_file.write("stdv_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.stdev([float (i[5]) for i in C_minus_1]))
                if [float (i[1]) for i in C_minus_1] :
                        text_file.write("mean N_Tweets/Year : " "%s\n" % statistics.mean([float (i[1]) for i in C_minus_1]))
                        if len ([float (i[1]) for i in C_minus_1]) > 1 :
                                text_file.write("stdv N_Tweets/Year : " "%s\n" % statistics.stdev([float (i[1]) for i in C_minus_1]))
                if [float (i[8]) for i in C_minus_1] :
                        text_file.write("mean N_Antecedents_Opposit : " "%s\n" % statistics.mean([float (i[8]) for i in C_minus_1]))
                        if len ([float (i[8]) for i in C_minus_1]) > 1 :
                                text_file.write("stdv N_Antecedents_Opposit : " "%s\n" % statistics.stdev([float (i[8]) for i in C_minus_1])) 
                if [float (i[2]) for i in C_minus_1] and [float (i[5]) for i in C_minus_1] :
                        text_file.write("Corr Spearman fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[2]) for i in C_minus_1], [float (i[5]) for i in C_minus_1])))
                        text_file.write("Corr Pearson fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[2]) for i in C_minus_1], [float (i[5]) for i in C_minus_1])))
                if [float (i[3]) for i in C_minus_1 if i[3]] and [float (i[9]) for i in C_minus_1 if i[9]] :
                        text_file.write("Corr Spearman Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[3]) for i in C_minus_1 if i[3]], [float (i[9]) for i in C_minus_1 if i[9]])))
                        text_file.write("Corr Pearson Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[3]) for i in C_minus_1 if i[3]], [float (i[9]) for i in C_minus_1 if i[9]])))
                if [float (i[1]) for i in C_minus_1] and [float (i[5]) for i in C_minus_1] :
                        text_file.write("Corr Spearman N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[1]) for i in C_minus_1], [float (i[5]) for i in C_minus_1])))
                        text_file.write("Corr Pearson N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[1]) for i in C_minus_1], [float (i[5]) for i in C_minus_1])))
                text_file.write('\n'"===========")
                text_file.write('\n'"C1 Characteristics " '\n')
                if [float (i[2]) for i in C1] :
                        text_file.write("mean_fw_to_fr : " "%s\n" % statistics.mean([float (i[2]) for i in C1]))
                        if len ([float (i[2]) for i in C1]) > 1 :
                                text_file.write("stdv_fw_to_fr : " "%s\n" % statistics.stdev([float (i[2]) for i in C1]))
                if [float (i[3]) for i in C1 if i[3]] :
                        text_file.write("mean_mutal_to_fw : " "%s\n" % statistics.mean([float (i[3]) for i in C1 if i[3]]))
                        if len ([float (i[3]) for i in C1 if i[3]]) > 1 :
                                text_file.write("stdv_mutal_to_fw : " "%s\n" % statistics.stdev([float (i[3]) for i in C1 if i[3]]))
                if [float (i[6]) for i in C1] :
                        text_file.write("mean_n_antecedents : " "%s\n" % statistics.mean([float (i[6]) for i in C1]))
                        if len ([float (i[6]) for i in C1]) > 1 :
                                text_file.write("stdv_n_antecedents : " "%s\n" % statistics.stdev([float (i[6]) for i in C1]))
                if [float (i[4]) for i in C1] :
                        text_file.write("mean_time_delay_with_source : " "%s\n" % statistics.mean([float (i[4]) for i in C1]))
                        if len ([float (i[4]) for i in C1]) > 1:
                                text_file.write("stdv_time_delay_with_source : " "%s\n" % statistics.stdev([float (i[4]) for i in C1]))
                if [float (i[5]) for i in C1] :
                        text_file.write("mean_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.mean([float (i[5]) for i in C1]))
                        if len ([float (i[5]) for i in C1]) > 1 :
                                text_file.write("stdv_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.stdev([float (i[5]) for i in C1]))
                if [float (i[1]) for i in C1] :
                        text_file.write("mean N_Tweets/Year : " "%s\n" % statistics.mean([float (i[1]) for i in C1]))
                        if len ([float (i[1]) for i in C1]) > 1 :
                                text_file.write("stdv N_Tweets/Year : " "%s\n" % statistics.stdev([float (i[1]) for i in C1]))
                if [float (i[8]) for i in C1] :
                        text_file.write("mean N_Antecedents_Opposit : " "%s\n" % statistics.mean([float (i[8]) for i in C1]))
                        if len ([float (i[8]) for i in C1]) > 1 :
                                text_file.write("stdv N_Antecedents_Opposit : " "%s\n" % statistics.stdev([float (i[8]) for i in C1])) 
                if [float (i[2]) for i in C1] and [float (i[5]) for i in C1] :
                        text_file.write("Corr Spearman fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[2]) for i in C1], [float (i[5]) for i in C1])))
                        text_file.write("Corr Pearson fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[2]) for i in C1], [float (i[5]) for i in C1])))
                if [float (i[3]) for i in C1 if i[3]] and [float (i[9]) for i in C1 if i[9]] :
                        text_file.write("Corr Spearman Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[3]) for i in C1 if i[3]], [float (i[9]) for i in C1 if i[9]])))
                        text_file.write("Corr Pearson Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[3]) for i in C1 if i[3]], [float (i[9]) for i in C1 if i[9]])))
                if [float (i[1]) for i in C1] and [float (i[5]) for i in C1] :
                        text_file.write("Corr Spearman N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[1]) for i in C1], [float (i[5]) for i in C1])))
                        text_file.write("Corr Pearson N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[1]) for i in C1], [float (i[5]) for i in C1])))
                if [float (i[6]) for i in C1] and [float (i[5]) for i in C1] :
                        text_file.write("Corr Spearman N_Antecedents to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[6]) for i in C1], [float (i[5]) for i in C1])))
                        text_file.write("Corr Pearson N_Antecedents to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[6]) for i in C1], [float (i[5]) for i in C1])))
                if [float (i[8]) for i in C1] and [float (i[5]) for i in C1] :
                        text_file.write("Corr Spearman N_Antecedents_Opposit to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[8]) for i in C1], [float (i[5]) for i in C1])))
                        text_file.write("Corr Pearson N_Antecedents_Opposit to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[8]) for i in C1], [float (i[5]) for i in C1])))
                text_file.write('\n'"===========")
                text_file.write('\n'"C2 Characteristics " '\n')
                if [float (i[2]) for i in C2] :
                        text_file.write("mean_fw_to_fr : " "%s\n" % statistics.mean([float (i[2]) for i in C2]))
                        if len ([float (i[2]) for i in C2]) > 1 :
                                text_file.write("stdv_fw_to_fr : " "%s\n" % statistics.stdev([float (i[2]) for i in C2]))
                if [float (i[3]) for i in C2 if i[3]] :
                        text_file.write("mean_mutal_to_fw : " "%s\n" % statistics.mean([float (i[3]) for i in C2 if i[3]]))
                        if len ([float (i[3]) for i in C2 if i[3]]) > 1 :
                                text_file.write("stdv_mutal_to_fw : " "%s\n" % statistics.stdev([float (i[3]) for i in C2 if i[3]]))
                if [float (i[6]) for i in C2] :
                        text_file.write("mean_n_antecedents : " "%s\n" % statistics.mean([float (i[6]) for i in C2]))
                        if len ([float (i[6]) for i in C2]) > 1 :
                                text_file.write("stdv_n_antecedents : " "%s\n" % statistics.stdev([float (i[6]) for i in C2]))
                if [float (i[4]) for i in C2] :
                        text_file.write("mean_time_delay_with_source : " "%s\n" % statistics.mean([float (i[4]) for i in C2]))
                        if len ([float (i[4]) for i in C2]) > 1:
                                text_file.write("stdv_time_delay_with_source : " "%s\n" % statistics.stdev([float (i[4]) for i in C2]))
                if [float (i[5]) for i in C2] :
                        text_file.write("mean_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.mean([float (i[5]) for i in C2]))
                        if len ([float (i[5]) for i in C2]) > 1 :
                                text_file.write("stdv_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.stdev([float (i[5]) for i in C2]))
                if [float (i[1]) for i in C2] :
                        text_file.write("mean N_Tweets/Year : " "%s\n" % statistics.mean([float (i[1]) for i in C2]))
                        if len ([float (i[1]) for i in C2]) > 1 :
                                text_file.write("stdv N_Tweets/Year : " "%s\n" % statistics.stdev([float (i[1]) for i in C2]))
                if [float (i[8]) for i in C2] :
                        text_file.write("mean N_Antecedents_Opposit : " "%s\n" % statistics.mean([float (i[8]) for i in C2]))
                        if len ([float (i[8]) for i in C2]) > 1 :
                                text_file.write("stdv N_Antecedents_Opposit : " "%s\n" % statistics.stdev([float (i[8]) for i in C2]))                        
                if [float (i[2]) for i in C2] and [float (i[5]) for i in C2] :
                        text_file.write("Corr Spearman fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[2]) for i in C2], [float (i[5]) for i in C2])))
                        text_file.write("Corr Pearson fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[2]) for i in C2], [float (i[5]) for i in C2])))
                if [float (i[3]) for i in C2 if i[3]] and [float (i[9]) for i in C2 if i[9]] :
                        text_file.write("Corr Spearman Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[3]) for i in C2 if i[3]], [float (i[9]) for i in C2 if i[9]])))
                        text_file.write("Corr Pearson Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[3]) for i in C2 if i[3]], [float (i[9]) for i in C2 if i[9]])))
                if [float (i[1]) for i in C2] and [float (i[5]) for i in C2] :
                        text_file.write("Corr Spearman N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[1]) for i in C2], [float (i[5]) for i in C2])))
                        text_file.write("Corr Pearson N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[1]) for i in C2], [float (i[5]) for i in C2])))
                if [float (i[6]) for i in C2] and [float (i[5]) for i in C2] :
                        text_file.write("Corr Spearman N_Antecedents to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[6]) for i in C2], [float (i[5]) for i in C2])))
                        text_file.write("Corr Pearson N_Antecedents to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[6]) for i in C2], [float (i[5]) for i in C2])))
                if [float (i[8]) for i in C2] and [float (i[5]) for i in C2] :
                        text_file.write("Corr Spearman N_Antecedents_Opposit to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[8]) for i in C2], [float (i[5]) for i in C2])))
                        text_file.write("Corr Pearson N_Antecedents_Opposit to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[8]) for i in C2], [float (i[5]) for i in C2])))
                text_file.write('\n'"===========")
                text_file.write('\n'"C11 Characteristics " '\n')
                if [float (i[2]) for i in C11] :
                        text_file.write("mean_fw_to_fr : " "%s\n" % statistics.mean([float (i[2]) for i in C11]))
                        if len ([float (i[2]) for i in C11]) > 1 :
                                text_file.write("stdv_fw_to_fr : " "%s\n" % statistics.stdev([float (i[2]) for i in C11]))
                if [float (i[3]) for i in C11 if i[3]] :
                        text_file.write("mean_mutal_to_fw : " "%s\n" % statistics.mean([float (i[3]) for i in C11 if i[3]]))
                        if len ([float (i[3]) for i in C11 if i[3]]) > 1 :
                                text_file.write("stdv_mutal_to_fw : " "%s\n" % statistics.stdev([float (i[3]) for i in C11 if i[3]]))
                if [float (i[6]) for i in C11] :
                        text_file.write("mean_n_antecedents : " "%s\n" % statistics.mean([float (i[6]) for i in C11]))
                        if len ([float (i[6]) for i in C11]) > 1 :
                                text_file.write("stdv_n_antecedents : " "%s\n" % statistics.stdev([float (i[6]) for i in C11]))
                if [float (i[4]) for i in C11] :
                        text_file.write("mean_time_delay_with_source : " "%s\n" % statistics.mean([float (i[4]) for i in C11]))
                        if len ([float (i[4]) for i in C11]) > 1:
                                text_file.write("stdv_time_delay_with_source : " "%s\n" % statistics.stdev([float (i[4]) for i in C11]))
                if [float (i[5]) for i in C11] :
                        text_file.write("mean_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.mean([float (i[5]) for i in C11]))
                        if len ([float (i[5]) for i in C11]) > 1 :
                                text_file.write("stdv_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.stdev([float (i[5]) for i in C11]))
                if [float (i[1]) for i in C11] :
                        text_file.write("mean N_Tweets/Year : " "%s\n" % statistics.mean([float (i[1]) for i in C11]))
                        if len ([float (i[1]) for i in C11]) > 1 :
                                text_file.write("stdv N_Tweets/Year : " "%s\n" % statistics.stdev([float (i[1]) for i in C11]))
                if [float (i[8]) for i in C11] :
                        text_file.write("mean N_Antecedents_Opposit : " "%s\n" % statistics.mean([float (i[8]) for i in C11]))
                        if len ([float (i[8]) for i in C11]) > 1 :
                                text_file.write("stdv N_Antecedents_Opposit : " "%s\n" % statistics.stdev([float (i[8]) for i in C11])) 
                if [float (i[2]) for i in C11] and [float (i[5]) for i in C11] :
                        text_file.write("Corr Spearman fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[2]) for i in C11], [float (i[5]) for i in C11])))
                        text_file.write("Corr Pearson fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[2]) for i in C11], [float (i[5]) for i in C11])))
                if [float (i[3]) for i in C11 if i[3]] and [float (i[9]) for i in C11 if i[9]] :
                        text_file.write("Corr Spearman Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[3]) for i in C11 if i[3]], [float (i[9]) for i in C11 if i[9]])))
                        text_file.write("Corr Pearson Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[3]) for i in C11 if i[3]], [float (i[9]) for i in C11 if i[9]])))
                if [float (i[1]) for i in C11] and [float (i[5]) for i in C11] :
                        text_file.write("Corr Spearman N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[1]) for i in C11], [float (i[5]) for i in C11])))
                        text_file.write("Corr Pearson N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[1]) for i in C11], [float (i[5]) for i in C11])))
                if [float (i[6]) for i in C11] and [float (i[5]) for i in C11] :
                        text_file.write("Corr Spearman N_Antecedents to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[6]) for i in C11], [float (i[5]) for i in C11])))
                        text_file.write("Corr Pearson N_Antecedents to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[6]) for i in C11], [float (i[5]) for i in C11])))
                if [float (i[8]) for i in C11] and [float (i[5]) for i in C11] :
                        text_file.write("Corr Spearman N_Antecedents_Opposit to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[8]) for i in C11], [float (i[5]) for i in C11])))
                        text_file.write("Corr Pearson N_Antecedents_Opposit to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[8]) for i in C11], [float (i[5]) for i in C11])))
                text_file.write('\n'"===========")
                text_file.write('\n'"C12 Characteristics " '\n')
                if [float (i[2]) for i in C12] :
                        text_file.write("mean_fw_to_fr : " "%s\n" % statistics.mean([float (i[2]) for i in C12]))
                        if len ([float (i[2]) for i in C12]) > 1 :
                                text_file.write("stdv_fw_to_fr : " "%s\n" % statistics.stdev([float (i[2]) for i in C12]))
                if [float (i[3]) for i in C12 if i[3]] :
                        text_file.write("mean_mutal_to_fw : " "%s\n" % statistics.mean([float (i[3]) for i in C12 if i[3]]))
                        if len ([float (i[3]) for i in C12 if i[3]]) > 1 :
                                text_file.write("stdv_mutal_to_fw : " "%s\n" % statistics.stdev([float (i[3]) for i in C12 if i[3]]))
                if [float (i[6]) for i in C12] :
                        text_file.write("mean_n_antecedents : " "%s\n" % statistics.mean([float (i[6]) for i in C12]))
                        if len ([float (i[6]) for i in C12]) > 1 :
                                text_file.write("stdv_n_antecedents : " "%s\n" % statistics.stdev([float (i[6]) for i in C12]))
                if [float (i[4]) for i in C12] :
                        text_file.write("mean_time_delay_with_source : " "%s\n" % statistics.mean([float (i[4]) for i in C12]))
                        if len ([float (i[4]) for i in C12]) > 1:
                                text_file.write("stdv_time_delay_with_source : " "%s\n" % statistics.stdev([float (i[4]) for i in C12]))
                if [float (i[5]) for i in C12] :
                        text_file.write("mean_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.mean([float (i[5]) for i in C12]))
                        if len ([float (i[5]) for i in C12]) > 1 :
                                text_file.write("stdv_time_delay_with_the_first_antecedent_spreader : " "%s\n" % statistics.stdev([float (i[5]) for i in C12]))
                if [float (i[1]) for i in C12] :
                        text_file.write("mean N_Tweets/Year : " "%s\n" % statistics.mean([float (i[1]) for i in C12]))
                        if len ([float (i[1]) for i in C12]) > 1 :
                                text_file.write("stdv N_Tweets/Year : " "%s\n" % statistics.stdev([float (i[1]) for i in C12]))
                if [float (i[8]) for i in C12] :
                        text_file.write("mean N_Antecedents_Opposit : " "%s\n" % statistics.mean([float (i[8]) for i in C12]))
                        if len ([float (i[8]) for i in C12]) > 1 :
                                text_file.write("stdv N_Antecedents_Opposit : " "%s\n" % statistics.stdev([float (i[8]) for i in C12])) 
                if [float (i[2]) for i in C12] and [float (i[5]) for i in C12] :
                        text_file.write("Corr Spearman fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[2]) for i in C12], [float (i[5]) for i in C12])))
                        text_file.write("Corr Pearson fw/fr to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[2]) for i in C12], [float (i[5]) for i in C12])))
                if [float (i[3]) for i in C12 if i[3]] and [float (i[9]) for i in C12 if i[9]] :
                        text_file.write("Corr Spearman Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[3]) for i in C12 if i[3]], [float (i[9]) for i in C12 if i[9]])))
                        text_file.write("Corr Pearson Mutal/fw to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[3]) for i in C12 if i[3]], [float (i[9]) for i in C12 if i[9]])))
                if [float (i[1]) for i in C12] and [float (i[5]) for i in C12] :
                        text_file.write("Corr Spearman N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[1]) for i in C12], [float (i[5]) for i in C12])))
                        text_file.write("Corr Pearson N_Tweets/Year to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[1]) for i in C12], [float (i[5]) for i in C12])))
                if [float (i[6]) for i in C12] and [float (i[5]) for i in C12] :
                        text_file.write("Corr Spearman N_Antecedents to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[6]) for i in C12], [float (i[5]) for i in C12])))
                        text_file.write("Corr Pearson N_Antecedents to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[6]) for i in C12], [float (i[5]) for i in C12])))
                if [float (i[8]) for i in C12] and [float (i[5]) for i in C12] :
                        text_file.write("Corr Spearman N_Antecedents_Opposit to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (spearmanr ([float (i[8]) for i in C12], [float (i[5]) for i in C12])))
                        text_file.write("Corr Pearson N_Antecedents_Opposit to time_delay_with_the_first_antecedent_spreader : " "%s\n" % str (pearsonr ([float (i[8]) for i in C12], [float (i[5]) for i in C12])))
                text_file.write('\n'"===========")
                text_file.write('\n'"######################################")
   
#-------------------------------------------------------------------
def all_retweeted_tweets (G_Directed_with_Attributes):
        import snap
        All_Retweeted_Tweets_Data = []
        All_Retweeted_ID = []
        popular_retweeted_ID_sorted = []
        ALL_UNIT_DATA = []
        from ast import literal_eval
        for NI in G_Directed_with_Attributes.Nodes():
                if G_Directed_with_Attributes.GetStrAttrDatN(NI, "Retweet_ID") :                        
                        data = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(NI, "Retweet_ID"))
                        for rid in data:
                                if rid != "NoRetID" :
                                        All_Retweeted_ID.append (rid)
        popular_retweeted_ID = [(element,All_Retweeted_ID.count(element)) for element in set(All_Retweeted_ID)]
        popular_retweeted_ID_sorted = sorted (popular_retweeted_ID, key=lambda x: x[1], reverse=True) #by this code we would have a list of tuples [(retweeted_ID, frequency), .... ] from most frequent ID to least frequent ID
        popular_retweeted_ID = []
        popular_retweeted_ID_sorted = tuple (popular_retweeted_ID_sorted)

        The_most_retweeted_Rumor_captured = 0
        The_most_retweeted_Antirumor_captured = 0
        keep_continue = True
        for popular_ID in popular_retweeted_ID_sorted :
                if keep_continue :                        
                        for NI in G_Directed_with_Attributes.Nodes():
                                if keep_continue :                                        
                                        if G_Directed_with_Attributes.GetStrAttrDatN(NI, "Tweet_ID"):
                                                TIList = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(NI, "Tweet_ID"))
                                                for TI in TIList :
                                                        if keep_continue :
                                                                if TI == popular_ID[0] :
                                                                        TI_index = TIList.index (TI)
                                                                        StateList = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(NI, "State_of_User"))
                                                                        Source_State = StateList [TI_index]
                                                                        if (Source_State[0] == 'R') and (The_most_retweeted_Rumor_captured == 0) :
                                                                                Source_Tweet_ID = popular_ID[0]
                                                                                Source_User_ID = G_Directed_with_Attributes.GetStrAttrDatN(NI, "User_ID") 
                                                                                Source_User_NAME = G_Directed_with_Attributes.GetStrAttrDatN(NI, "NAME_USERS")
                                                                                Source_Date_Creation_Account = G_Directed_with_Attributes.GetStrAttrDatN(NI, "Date_Creation_Account")
                                                                                Source_N_Posts = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Tweets")
                                                                                Source_N_Posts_per_Year = (int (Source_N_Posts))/(2019 - int (Source_Date_Creation_Account))
                                                                                Source_N_Followers = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Followers")
                                                                                Source_N_Friends = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Friends")
                                                                                Source_N_Friends_To_N_Followers = (float (Source_N_Friends))/(float (Source_N_Followers))
                                                                                Source_ID_in_Graph = NI.GetId()
                                                                                MUTUAL = 0
                                                                                for NIN in G_Directed_with_Attributes.Nodes():  
                                                                                        if (NIN.IsOutNId(Source_ID_in_Graph)) and (NIN.IsInNId(Source_ID_in_Graph)) :
                                                                                                MUTUAL += 1
                                                                                if float (NI.GetOutDeg()) != 0 :
                                                                                          Source_Mutal_To_N_Friends = (float (MUTUAL)) / (float (NI.GetOutDeg()))
                                                                                else:
                                                                                    Source_Mutal_To_N_Friends = 'N/A'
                                                                                DateTimeList = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(NI, "Date_Time"))
                                                                                Source_Date_Time = DateTimeList [TI_index]
                                                                                Source_N_Retweets_for_this_Popular_Tweet = popular_ID[1]
                                                                                Distance_from_Source = []
                                                                                for NIN in G_Directed_with_Attributes.Nodes():
                                                                                        if G_Directed_with_Attributes.GetStrAttrDatN(NIN, "Retweet_ID") :  
                                                                                                RTIList = literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(NIN, "Retweet_ID"))
                                                                                                for RTI in RTIList :
                                                                                                        if RTI == popular_ID[0] :
                                                                                                                Distance_from_Source.append (snap.GetShortPath(G_Directed_with_Attributes, NIN.GetId(), Source_ID_in_Graph, True)) #the short distance from the current node to the destination node (the source node of publishing retweet)
                                                                                                                
                                                                                Distances_with_Retweeters = [(element,Distance_from_Source.count(element)) for element in set(Distance_from_Source)]
                                                                                Source_Distances_with_Retweeters_sorted = sorted (Distances_with_Retweeters, key=lambda x: x[1], reverse=True) 
                                                                                Source_Distances_with_Retweeters_sorted = tuple (Source_Distances_with_Retweeters_sorted)
                                                                                Retweeted_Tweet_Data = []
                                                                                Retweeted_Tweet_Data.append(Source_Tweet_ID)  
                                                                                Retweeted_Tweet_Data.append(Source_User_ID) 
                                                                                Retweeted_Tweet_Data.append(Source_User_NAME) 
                                                                                Retweeted_Tweet_Data.append(Source_N_Posts_per_Year)                                 
                                                                                Retweeted_Tweet_Data.append(Source_N_Friends_To_N_Followers) 
                                                                                Retweeted_Tweet_Data.append(Source_ID_in_Graph) 
                                                                                Retweeted_Tweet_Data.append(Source_Mutal_To_N_Friends) 
                                                                                Retweeted_Tweet_Data.append(Source_Date_Time) 
                                                                                Retweeted_Tweet_Data.append(Source_State) 
                                                                                Retweeted_Tweet_Data.append(Source_N_Retweets_for_this_Popular_Tweet) 
                                                                                Retweeted_Tweet_Data.append(Source_Distances_with_Retweeters_sorted) 
                                                                                Retweeted_Tweet_Data = tuple (Retweeted_Tweet_Data) #converting list to tuple saves memory
                                                                                All_Retweeted_Tweets_Data.append (Retweeted_Tweet_Data)
                                                                                The_most_retweeted_Rumor_captured = 1
                                                                                break
                                                                                
                                                                        elif (Source_State[0] == 'A') and (The_most_retweeted_Antirumor_captured == 0) :
                                                                                Source_Tweet_ID = popular_ID[0]
                                                                                Source_User_ID = G_Directed_with_Attributes.GetStrAttrDatN(NI, "User_ID") 
                                                                                Source_User_NAME = G_Directed_with_Attributes.GetStrAttrDatN(NI, "NAME_USERS")
                                                                                Source_Date_Creation_Account = G_Directed_with_Attributes.GetStrAttrDatN(NI, "Date_Creation_Account")
                                                                                Source_N_Posts = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Tweets")
                                                                                Source_N_Posts_per_Year = (int (Source_N_Posts))/(2019 - int (Source_Date_Creation_Account))
                                                                                Source_N_Followers = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Followers")
                                                                                Source_N_Friends = G_Directed_with_Attributes.GetStrAttrDatN(NI, "N_Friends")
                                                                                Source_N_Friends_To_N_Followers = (float (Source_N_Friends))/(float (Source_N_Followers))
                                                                                Source_ID_in_Graph = NI.GetId()
                                                                                MUTUAL = 0
                                                                                for NIN in G_Directed_with_Attributes.Nodes():  
                                                                                        if (NIN.IsOutNId(Source_ID_in_Graph)) and (NIN.IsInNId(Source_ID_in_Graph)) :
                                                                                                MUTUAL += 1
                                                                                if float (NI.GetOutDeg()) != 0 :
                                                                                          Source_Mutal_To_N_Friends = (float (MUTUAL)) / (float (NI.GetOutDeg()))
                                                                                else:
                                                                                    Source_Mutal_To_N_Friends = 'N/A'
                                                                                DateTimeList = literal_eval(G_Directed_with_Attributes.GetStrAttrDatN(NI, "Date_Time"))
                                                                                Source_Date_Time = DateTimeList [TI_index]
                                                                                Source_N_Retweets_for_this_Popular_Tweet = popular_ID[1]
                                                                                Distance_from_Source = []
                                                                                for NIN in G_Directed_with_Attributes.Nodes():
                                                                                        if G_Directed_with_Attributes.GetStrAttrDatN(NIN, "Retweet_ID") :  
                                                                                                RTIList = literal_eval (G_Directed_with_Attributes.GetStrAttrDatN(NIN, "Retweet_ID"))
                                                                                                for RTI in RTIList :
                                                                                                        if RTI == popular_ID[0] :
                                                                                                                Distance_from_Source.append (snap.GetShortPath(G_Directed_with_Attributes, NIN.GetId(), Source_ID_in_Graph, True)) #the short distance from the current node to the destination node (the source node of publishing retweet)
             
                                                                                Distances_with_Retweeters = [(element,Distance_from_Source.count(element)) for element in set(Distance_from_Source)]
                                                                                Source_Distances_with_Retweeters_sorted = sorted (Distances_with_Retweeters, key=lambda x: x[1], reverse=True) 
                                                                                Source_Distances_with_Retweeters_sorted = tuple (Source_Distances_with_Retweeters_sorted)
                                                                                Retweeted_Tweet_Data = []
                                                                                Retweeted_Tweet_Data.append(Source_Tweet_ID)  
                                                                                Retweeted_Tweet_Data.append(Source_User_ID) 
                                                                                Retweeted_Tweet_Data.append(Source_User_NAME) 
                                                                                Retweeted_Tweet_Data.append(Source_N_Posts_per_Year)                                 
                                                                                Retweeted_Tweet_Data.append(Source_N_Friends_To_N_Followers) 
                                                                                Retweeted_Tweet_Data.append(Source_ID_in_Graph) 
                                                                                Retweeted_Tweet_Data.append(Source_Mutal_To_N_Friends) 
                                                                                Retweeted_Tweet_Data.append(Source_Date_Time) 
                                                                                Retweeted_Tweet_Data.append(Source_State) 
                                                                                Retweeted_Tweet_Data.append(Source_N_Retweets_for_this_Popular_Tweet) 
                                                                                Retweeted_Tweet_Data.append(Source_Distances_with_Retweeters_sorted) 
                                                                                Retweeted_Tweet_Data = tuple (Retweeted_Tweet_Data) #converting list to tuple saves memory
                                                                                All_Retweeted_Tweets_Data.append (Retweeted_Tweet_Data)
                                                                                The_most_retweeted_Antirumor_captured = 1
                                                                                break
                                                                                
                                                                        if (The_most_retweeted_Rumor_captured + The_most_retweeted_Antirumor_captured == 2):
                                                                                keep_continue = False


                                                                        break
                                                        else :
                                                                break
                                else :
                                        break
                else :
                        break
                
        All_Retweeted_Tweets_Data = tuple (All_Retweeted_Tweets_Data)
        return All_Retweeted_Tweets_Data                        
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
