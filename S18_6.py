#----------------------------------
# This codes give information about the centralities of nodes in each category (rumor tweeter, anti rumor tweeter, antirumor retweeter, antirumor retweeter)
# This information is like this:
# What fraction of following and followers of nodes in Category of X (one of the afromentioned categories) belongs to nodes in Category of Y (one of the afromentioned categories)
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
    All_Retweeted_Tweets_Data = all_retweeted_tweets (G_Directed_with_Attributes)
    Mutal_Friendship_Finder (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data)
    PRankH = PageRank_Finder (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data)
    NIdHubH , NIdAuthH = Hub_Authority_Score_Finder (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data)
    Farness_centrality (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data)
    Closeness_centrality (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data)
    Edges_In_Out (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data)
    Modularity (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data)
    Main_Source_Spreaders_Centralities (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data,PRankH,NIdHubH,NIdAuthH)
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
# This function gives the mean number of ratio of mutal friendships to followers for each of the 4 main categories
def Mutal_Friendship_Finder (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data) :
        import numpy as np
        import ast
        ratio_Mutal_Friends_to_Followers_Tweeter_Rumor = []
        ratio_Mutal_Friends_to_Followers_Retweeter_Rumor = []
        ratio_Mutal_Friends_to_Followers_Tweeter_AntiRumor = []
        ratio_Mutal_Friends_to_Followers_Retweeter_AntiRumor = []       
        for NI in G_Directed_with_Attributes.Nodes():
            if G_Directed_with_Attributes.GetStrAttrDatN(NI, "State_of_User"):
                SU = G_Directed_with_Attributes.GetStrAttrDatN(NI, "State_of_User")
                SU = ast.literal_eval(SU)
                if SU[0] == 'RT':
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
                         Number_Mutal_Friends = len(set(Number_out_neighbors) & set(Number_In_neighbors))
                         if InDeg != 0: #to avoid devide by zero
                                 ratio_Mutal_Friends_to_Followers = float(Number_Mutal_Friends)/float(InDeg)
                                 ratio_Mutal_Friends_to_Followers_Tweeter_Rumor.append (ratio_Mutal_Friends_to_Followers)

                                        
                elif SU[0] == 'RR':
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
                         Number_Mutal_Friends = len(set(Number_out_neighbors) & set(Number_In_neighbors))
                         if InDeg != 0: #to avoid devide by zero
                                 ratio_Mutal_Friends_to_Followers = float(Number_Mutal_Friends)/float(InDeg)
                                 ratio_Mutal_Friends_to_Followers_Retweeter_Rumor.append (ratio_Mutal_Friends_to_Followers)

                elif SU[0] == 'AT':
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
                         Number_Mutal_Friends = len(set(Number_out_neighbors) & set(Number_In_neighbors))
                         if InDeg != 0: #to avoid devide by zero
                                 ratio_Mutal_Friends_to_Followers = float(Number_Mutal_Friends)/float(InDeg)
                                 ratio_Mutal_Friends_to_Followers_Tweeter_AntiRumor.append (ratio_Mutal_Friends_to_Followers)



                elif SU[0] == 'AR':
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
                         Number_Mutal_Friends = len(set(Number_out_neighbors) & set(Number_In_neighbors))
                         if InDeg != 0: #to avoid devide by zero
                                 ratio_Mutal_Friends_to_Followers = float(Number_Mutal_Friends)/float(InDeg)
                                 ratio_Mutal_Friends_to_Followers_Retweeter_AntiRumor.append (ratio_Mutal_Friends_to_Followers)


                else :
                    None

        text_file = open(path_output + "S18_6_Output.txt", "a")
        text_file.write('====================================================================' "\n")
        text_file.write('Ratio of Mutal Friends to Followers' "\n")
        text_file.write("ratio_Mutal_Friends_to_Followers_Tweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(ratio_Mutal_Friends_to_Followers_Tweeter_Rumor)) , float(np.std (ratio_Mutal_Friends_to_Followers_Tweeter_Rumor))))
        text_file.write("ratio_Mutal_Friends_to_Followers_Retweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(ratio_Mutal_Friends_to_Followers_Retweeter_Rumor)) , float(np.std (ratio_Mutal_Friends_to_Followers_Retweeter_Rumor))))
        text_file.write("ratio_Mutal_Friends_to_Followers_Tweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(ratio_Mutal_Friends_to_Followers_Tweeter_AntiRumor)) , float(np.std (ratio_Mutal_Friends_to_Followers_Tweeter_AntiRumor))))
        text_file.write("ratio_Mutal_Friends_to_Followers_Retweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(ratio_Mutal_Friends_to_Followers_Retweeter_AntiRumor)) , float(np.std (ratio_Mutal_Friends_to_Followers_Retweeter_AntiRumor))))
        text_file.write('====================================================================' "\n")
        text_file.close()

#-----------------------------------------
# This function calculates PageRank
def PageRank_Finder (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data) :
    import numpy as np
    import snap
    import ast
    PRankH = snap.TIntFltH()
    snap.GetPageRank(G_Directed_with_Attributes, PRankH)
    RT_PRank = []
    RR_PRank = []
    AT_PRank = []
    AR_PRank = []
    for ni in G_Directed_with_Attributes.Nodes():
        if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                SU = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                SU = ast.literal_eval(SU)
                if SU[0] == 'RT':
                    for item in PRankH:
                        if ni.GetId() == item:
                            RT_PRank.append (PRankH[item])
                            break
                elif SU[0] == 'RR':
                    for item in PRankH:
                        if ni.GetId() == item:
                            RR_PRank.append (PRankH[item])
                        break
                elif SU[0] == 'AT':
                    for item in PRankH:
                        if ni.GetId() == item:
                            AT_PRank.append (PRankH[item])
                            break
                elif SU[0] == 'AR':
                    for item in PRankH:
                        if ni.GetId() == item:
                            AR_PRank.append (PRankH[item])
                            break
                else :
                    None
        


    text_file = open(path_output + "S18_6_Output.txt", "a")
    text_file.write('====================================================================' "\n")
    text_file.write('PageRank ' "\n")
    text_file.write("PageRank_Tweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RT_PRank)) , float(np.std (RT_PRank))))
    text_file.write("PageRank_Retweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RR_PRank)) , float(np.std (RR_PRank))))
    text_file.write("PageRank_Tweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AT_PRank)) , float(np.std (AT_PRank))))
    text_file.write("PageRank_Retweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AR_PRank)) , float(np.std (AR_PRank))))
    text_file.write('====================================================================' "\n")
    text_file.close()
    return PRankH

#-----------------------------------------
# This function calculates Hubs and Authorities score of every node
def Hub_Authority_Score_Finder (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data) :
    import numpy as np
    import snap
    import ast
    NIdHubH = snap.TIntFltH()
    NIdAuthH = snap.TIntFltH()
    snap.GetHits(G_Directed_with_Attributes, NIdHubH, NIdAuthH)
    RT_HubScore = []
    RR_HubScore = []
    AT_HubScore = []
    AR_HubScore = []
    RT_AuthorityScore = []
    RR_AuthorityScore = []
    AT_AuthorityScore = []
    AR_AuthorityScore = []
    for ni in G_Directed_with_Attributes.Nodes():
        if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                SU = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                SU = ast.literal_eval(SU)
                if SU[0] == 'RT':
                    for item in NIdHubH:
                        if ni.GetId() == item:
                            RT_HubScore.append (NIdHubH[item])
                            break
                    for item in NIdAuthH:
                        if ni.GetId() == item:
                            RT_AuthorityScore.append (NIdAuthH[item])
                            break
                elif SU[0] == 'RR':
                    for item in NIdHubH:
                        if ni.GetId() == item:
                            RR_HubScore.append (NIdHubH[item])
                            break
                    for item in NIdAuthH:
                        if ni.GetId() == item:
                            RR_AuthorityScore.append (NIdAuthH[item])
                            break
                elif SU[0] == 'AT':
                    for item in NIdHubH:
                        if ni.GetId() == item:
                            AT_HubScore.append (NIdHubH[item])
                            break
                    for item in NIdAuthH:
                        if ni.GetId() == item:
                            AT_AuthorityScore.append (NIdAuthH[item])
                            break
                elif SU[0] == 'AR':
                    for item in NIdHubH:
                        if ni.GetId() == item:
                            AR_HubScore.append (NIdHubH[item])
                            break
                    for item in NIdAuthH:
                        if ni.GetId() == item:
                            AR_AuthorityScore.append (NIdAuthH[item])
                            break        

                else :
                    None
        


    text_file = open(path_output + "S18_6_Output.txt", "a")
    text_file.write('====================================================================' "\n")
    text_file.write('Hubs and Authorities score ' "\n")                                             
    text_file.write("Hubs_Tweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RT_HubScore)) , float(np.std (RT_HubScore))))
    text_file.write("Authorities_Tweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RT_AuthorityScore)) , float(np.std (RT_AuthorityScore))))
    text_file.write("Hubs_Retweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RR_HubScore)) , float(np.std (RR_HubScore))))
    text_file.write("Authorities_Retweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RR_AuthorityScore)) , float(np.std (RR_AuthorityScore))))
    text_file.write("Hubs_Tweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AT_HubScore)) , float(np.std (AT_HubScore))))
    text_file.write("Authorities_Tweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AT_AuthorityScore)) , float(np.std (AT_AuthorityScore))))                                             
    text_file.write("Hubs_Retweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AR_HubScore)) , float(np.std (AR_HubScore))))
    text_file.write("Authorities_Retweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AR_AuthorityScore)) , float(np.std (AR_AuthorityScore))))
    text_file.write('====================================================================' "\n")                                             
    text_file.close()

    return NIdHubH , NIdAuthH
#-----------------------------------------
# This function calculates Farness centrality of a node
def Farness_centrality (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data) :
    import numpy as np
    import snap
    import ast
    RT_FarCentr = []
    RR_FarCentr = []
    AT_FarCentr = []
    AR_FarCentr = []
    for ni in G_Directed_with_Attributes.Nodes():
        if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                SU = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                SU = ast.literal_eval(SU)
                if SU[0] == 'RT':
                    FarCentr = snap.GetFarnessCentr(G_Directed_with_Attributes, ni.GetId(), True, True)
                    RT_FarCentr.append (FarCentr)

                elif SU[0] == 'RR':
                    FarCentr = snap.GetFarnessCentr(G_Directed_with_Attributes, ni.GetId(), True, True)
                    RR_FarCentr.append (FarCentr)
                    
                elif SU[0] == 'AT':
                    FarCentr = snap.GetFarnessCentr(G_Directed_with_Attributes, ni.GetId(), True, True)
                    AT_FarCentr.append (FarCentr)
                    
                elif SU[0] == 'AR':
                    FarCentr = snap.GetFarnessCentr(G_Directed_with_Attributes, ni.GetId(), True, True)
                    AR_FarCentr.append (FarCentr)       

                else :
                    None
        


    text_file = open(path_output + "S18_6_Output.txt", "a")
    text_file.write('====================================================================' "\n")
    text_file.write('Farness Centrality ' "\n")                                             
    text_file.write("Farness_centrality_Tweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RT_FarCentr)) , float(np.std (RT_FarCentr))))
    text_file.write("Farness_centrality_Retweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RR_FarCentr)) , float(np.std (RR_FarCentr))))
    text_file.write("Farness_centrality_Tweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AT_FarCentr)) , float(np.std (AT_FarCentr))))                                             
    text_file.write("Farness_centrality_Retweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AR_FarCentr)) , float(np.std (AR_FarCentr))))
    text_file.write('====================================================================' "\n")                                             
    text_file.close()

#-----------------------------------------
# This function calculates Farness centrality of a node
def Closeness_centrality (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data) :
    import numpy as np
    import snap
    import ast
    RT_CloseCentr = []
    RR_CloseCentr = []
    AT_CloseCentr = []
    AR_CloseCentr = []
    for ni in G_Directed_with_Attributes.Nodes():
        if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                SU = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                SU = ast.literal_eval(SU)
                if SU[0] == 'RT':
                    CloseCentr = snap.GetClosenessCentr(G_Directed_with_Attributes, ni.GetId(), True, True)
                    RT_CloseCentr.append (CloseCentr)

                elif SU[0] == 'RR':
                    CloseCentr = snap.GetClosenessCentr(G_Directed_with_Attributes, ni.GetId(), True, True)
                    RR_CloseCentr.append (CloseCentr)
                    
                elif SU[0] == 'AT':
                    CloseCentr = snap.GetClosenessCentr(G_Directed_with_Attributes, ni.GetId(), True, True)
                    AT_CloseCentr.append (CloseCentr)
                    
                elif SU[0] == 'AR':
                    CloseCentr = snap.GetClosenessCentr(G_Directed_with_Attributes, ni.GetId(), True, True)
                    AR_CloseCentr.append (CloseCentr)       

                else :
                    None
        


    text_file = open(path_output + "S18_6_Output.txt", "a")
    text_file.write('====================================================================' "\n")
    text_file.write('Closeness Centrality ' "\n")                                             
    text_file.write("Closeness_centrality_Tweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RT_CloseCentr)) , float(np.std (RT_CloseCentr))))
    text_file.write("Closeness_centrality_Retweeter_Rumor (Mean , SD) : " "%s %s\n" % (float(np.mean(RR_CloseCentr)) , float(np.std (RR_CloseCentr))))
    text_file.write("Closeness_centrality_Tweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AT_CloseCentr)) , float(np.std (AT_CloseCentr))))                                             
    text_file.write("Closeness_centrality_Retweeter_AntiRumor (Mean , SD) : " "%s %s\n" % (float(np.mean(AR_CloseCentr)) , float(np.std (AR_CloseCentr))))
    text_file.write('====================================================================' "\n")                                             
    text_file.close()

#-----------------------------------------
# This function calculates number of reciprocal edges between nodes in each category and number of edges between that category with the rest of the graph
def Edges_In_Out (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data) :
    import ast
    import snap
    RT_Nodes = snap.TIntV()
    RR_Nodes = snap.TIntV()
    AT_Nodes = snap.TIntV()
    AR_Nodes = snap.TIntV()
    for ni in G_Directed_with_Attributes.Nodes():
            if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                    SU = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                    SU = ast.literal_eval(SU)
                    if SU[0] == 'RT':
                        RT_Nodes.Add (ni.GetId())
                    elif SU[0] == 'RR':
                        RR_Nodes.Add (ni.GetId())
                    elif SU[0] == 'AT':
                        AT_Nodes.Add (ni.GetId())
                    elif SU[0] == 'AR':
                        AR_Nodes.Add (ni.GetId())
                    else:
                        None
    

    RT_Nodes_results = snap.GetEdgesInOut(G_Directed_with_Attributes, RT_Nodes)
    RR_Nodes_results = snap.GetEdgesInOut(G_Directed_with_Attributes, RR_Nodes)
    AT_Nodes_results = snap.GetEdgesInOut(G_Directed_with_Attributes, AT_Nodes)
    AR_Nodes_results = snap.GetEdgesInOut(G_Directed_with_Attributes, AR_Nodes)

    text_file = open(path_output + "S18_6_Output.txt", "a")
    text_file.write('====================================================================' "\n")
    text_file.write('Edges_In_Out ' "\n")                                             
    text_file.write("Edges_In_Out_Tweeter_Rumor (Reciprocal In Edges , Out Edges) : " "%s %s\n" % (float(RT_Nodes_results[0]) , float(RT_Nodes_results[1])))
    text_file.write("Edges_In_Out_Retweeter_Rumor (Reciprocal In Edges , Out Edges) : " "%s %s\n" % (float(RR_Nodes_results[0]) , float(RR_Nodes_results[1])))
    text_file.write("Edges_In_Out_Tweeter_AntiRumor (Reciprocal In Edges , Out Edges) : " "%s %s\n" % (float(AT_Nodes_results[0]) , float(AT_Nodes_results[1])))                                             
    text_file.write("Edges_In_Out_Retweeter_AntiRumor (Reciprocal In Edges , Out Edges) : " "%s %s\n" % (float(AR_Nodes_results[0]) , float(AR_Nodes_results[1])))
    text_file.write('====================================================================' "\n")                                             
    text_file.close()

#-----------------------------------------
# This function calculates Modularity of each category and number of edges between that category with the rest of the graph
def Modularity (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data) :
    import ast
    import snap
    RT_Nodes = snap.TIntV()
    RR_Nodes = snap.TIntV()
    AT_Nodes = snap.TIntV()
    AR_Nodes = snap.TIntV()
    for ni in G_Directed_with_Attributes.Nodes():
            if G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User"):
                    SU = G_Directed_with_Attributes.GetStrAttrDatN(ni, "State_of_User")
                    SU = ast.literal_eval(SU)
                    if SU[0] == 'RT':
                        RT_Nodes.Add (ni.GetId())
                    elif SU[0] == 'RR':
                        RR_Nodes.Add (ni.GetId())
                    elif SU[0] == 'AT':
                        AT_Nodes.Add (ni.GetId())
                    elif SU[0] == 'AR':
                        AR_Nodes.Add (ni.GetId())
                    else:
                        None
    

    RT_Nodes_results = snap.GetModularity(G_Directed_with_Attributes, RT_Nodes)
    RR_Nodes_results = snap.GetModularity(G_Directed_with_Attributes, RR_Nodes)
    AT_Nodes_results = snap.GetModularity(G_Directed_with_Attributes, AT_Nodes)
    AR_Nodes_results = snap.GetModularity(G_Directed_with_Attributes, AR_Nodes)

    text_file = open(path_output + "S18_6_Output.txt", "a")
    text_file.write('====================================================================' "\n")
    text_file.write('Modularity ' "\n")                                             
    text_file.write("Modularity_Tweeter_Rumor  : " "%s \n" % (float(RT_Nodes_results)))
    text_file.write("Modularity_Retweeter_Rumor  : " "%s \n" % (float(RR_Nodes_results)))
    text_file.write("Modularity_Tweeter_AntiRumor  : " "%s \n" % (float(AT_Nodes_results)))                                             
    text_file.write("Modularity_Retweeter_AntiRumor  : " "%s \n" % (float(AR_Nodes_results)))
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
def Main_Source_Spreaders_Centralities (G_Directed_with_Attributes,path_output,All_Retweeted_Tweets_Data,PRankH,NIdHubH,NIdAuthH):
    import ast
    import snap
    for NI in G_Directed_with_Attributes.Nodes():
        if NI.GetId() == All_Retweeted_Tweets_Data[0][5]:
            #---- Mutual ----
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
            Number_Mutal_Friends = len(set(Number_out_neighbors) & set(Number_In_neighbors))
            if InDeg != 0: #to avoid devide by zero
                Mutal_Friendship_TheMainSource_Rumor_Spreader = float(Number_Mutal_Friends)/float(InDeg)
            else:
                Mutal_Friendship_TheMainSource_Rumor_Spreader = float(Number_Mutal_Friends)/float(float(InDeg)+1)
            #---- PageRank ----
            for item in PRankH:
                if NI.GetId() == item:
                    PRank_TheMainSource_Rumor_Spreader = (PRankH[item])
            #---- Hub_Authority_Score ----
            for item in NIdHubH:
                if NI.GetId() == item:
                    HubScore_TheMainSource_Rumor_Spreader = (NIdHubH[item])
            for item in NIdAuthH:
                if NI.GetId() == item:
                    AuthorityScore_TheMainSource_Rumor_Spreader = (NIdAuthH[item])
            #---- Farness_centrality ----
            FarCentr_TheMainSource_Rumor_Spreader = snap.GetFarnessCentr(G_Directed_with_Attributes, NI.GetId(), True, True)
            #---- Closeness_centrality ----
            CloseCentr_TheMainSource_Rumor_Spreader = snap.GetClosenessCentr(G_Directed_with_Attributes, NI.GetId(), True, True)

        elif NI.GetId() == All_Retweeted_Tweets_Data[1][5]:
            #---- Mutual ----
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
            Number_Mutal_Friends = len(set(Number_out_neighbors) & set(Number_In_neighbors))
            if InDeg != 0: #to avoid devide by zero
                Mutal_Friendship_TheMainSource_AntiRumor_Spreader = float(Number_Mutal_Friends)/float(InDeg)
            else:
                Mutal_Friendship_TheMainSource_AntiRumor_Spreader = float(Number_Mutal_Friends)/float(float(InDeg)+1)
            #---- PageRank ----
            for item in PRankH:
                if NI.GetId() == item:
                    PRank_TheMainSource_AntiRumor_Spreader = (PRankH[item])
            #---- Hub_Authority_Score ----
            for item in NIdHubH:
                if NI.GetId() == item:
                    HubScore_TheMainSource_AntiRumor_Spreader = (NIdHubH[item])
            for item in NIdAuthH:
                if NI.GetId() == item:
                    AuthorityScore_TheMainSource_AntiRumor_Spreader = (NIdAuthH[item])
            #---- Farness_centrality ----
            FarCentr_TheMainSource_AntiRumor_Spreader = snap.GetFarnessCentr(G_Directed_with_Attributes, NI.GetId(), True, True)
            #---- Closeness_centrality ----
            CloseCentr_TheMainSource_AntiRumor_Spreader = snap.GetClosenessCentr(G_Directed_with_Attributes, NI.GetId(), True, True)

        else :
            None
        #--------

    text_file = open(path_output + "S18_6_Output.txt", "a")
    text_file.write('====================================================================' "\n")
    text_file.write('Source Nodes Centralities  ' "\n")
    text_file.write('MainSource_RumorSpreaders  (UserName, NumberOfRetweets, DistanceToRetweeter)  : ' "%s %s %s\n" %  (All_Retweeted_Tweets_Data[0][2] , All_Retweeted_Tweets_Data[0][9] , str(All_Retweeted_Tweets_Data[0][10])))
    text_file.write('MainSource_AntiRumorSpreaders  (UserName, NumberOfRetweets, DistanceToRetweeter)  : ' "%s %s %s\n" %  (All_Retweeted_Tweets_Data[1][2] , All_Retweeted_Tweets_Data[1][9] , str(All_Retweeted_Tweets_Data[1][10])))
    text_file.write("ratio_Mutal_Friends_to_Followers_MainSource (RT,AT) : " "%s %s\n" % (float(Mutal_Friendship_TheMainSource_Rumor_Spreader) , float(Mutal_Friendship_TheMainSource_AntiRumor_Spreader)))
    text_file.write("PageRank_MainSource (RT,AT) : " "%s %s\n" % (float(PRank_TheMainSource_Rumor_Spreader) , float(PRank_TheMainSource_AntiRumor_Spreader)))
    text_file.write("Hub_Score_MainSource (RT,AT) : " "%s %s\n" % (float(HubScore_TheMainSource_Rumor_Spreader) , float(HubScore_TheMainSource_AntiRumor_Spreader)))
    text_file.write("Authority_Score_MainSource (RT,AT) : " "%s %s\n" % (float(AuthorityScore_TheMainSource_Rumor_Spreader) , float(AuthorityScore_TheMainSource_AntiRumor_Spreader)))
    text_file.write("Farness_centrality_MainSource (RT,AT) : " "%s %s\n" % (float(FarCentr_TheMainSource_Rumor_Spreader) , float(FarCentr_TheMainSource_AntiRumor_Spreader)))
    text_file.write("Closeness_centrality_MainSource (RT,AT) : " "%s %s\n" % (float(CloseCentr_TheMainSource_Rumor_Spreader) , float(CloseCentr_TheMainSource_AntiRumor_Spreader)))
    text_file.write('====================================================================' "\n")
    text_file.close()
#-----------------------------------------
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
                                                                                Retweeted_Tweet_Data.append(Source_Mutal_To_N_Friends) #to become number followers 
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
main ()
print "################################"
raw_input('press enter key to exit...')

