import pm4py
from pm4py.objects.log.importer.xes import importer as xes_importer
# =============================================================================
# LOADING THE LOG FILE IN PM4PY
# =============================================================================
log = xes_importer.apply('InternationalDeclarations.xes')
#%%
# =============================================================================
# SPLITTING THE LOG FILES BY YEARS 
# =============================================================================
from pm4py.algo.filtering.log.timestamp import timestamp_filter
# log_2019 = timestamp_filter.filter_traces_contained(log, "2019-01-01 00:00:00", "2019-12-31 23:59:59")
# =============================================================================
#  SPLITTING LOGS INTERSECTING IN THE TIME INTERVAL
# =============================================================================
# ----------------------------------FOR 2017---------------------------------------------
log_in_2017 = timestamp_filter.filter_traces_intersecting(log, "2017-01-01 00:00:00", "2017-12-31 23:59:59")
# ----------------------------------FOR 2018---------------------------------------------
log_in_2018 = timestamp_filter.filter_traces_intersecting(log, "2018-01-01 00:00:00", "2018-12-31 23:59:59")

# =============================================================================
# SPLITTING LOGS CONTAINED IN THE TIME INTERVAL
# =============================================================================
# ----------------------------------FOR 2017---------------------------------------------
log_con_2017 = timestamp_filter.filter_traces_contained(log, "2017-01-01 00:00:00", "2017-12-31 23:59:59")
# ----------------------------------FOR 2018---------------------------------------------
log_con_2018 = timestamp_filter.filter_traces_contained(log, "2018-01-01 00:00:00", "2018-12-31 23:59:59")
#%%
log=log_con_2018
filename=r'Data_con_2018.csv'
print("Total number of cases :"+str(len(log)))

# =============================================================================
# CONVERTING LOG FILES INTO DATAFRAME
# =============================================================================
import pandas as pd
from pm4py.objects.conversion.log import converter as log_converter
df = log_converter.apply(log, variant=log_converter.Variants.TO_DATA_FRAME)

#%%
# =============================================================================
# 1. for each case, get throughput time between 'Declaration SUBMITTED by EMPLOYEE' and 
# ( 'Payment Handled' OR 'Declaration REJECTED by EMPLOYEE', whichever comes later)
# =============================================================================
through_put=[0]*len(log)
case=[0]*len(log)
for i in range(len(log)): # CASE ITERATOR
#for i in range(5):
    for j in range(len(log[i])): # EVENT ITERATOR
        if (log[i][j]['concept:name']=="Declaration SUBMITTED by EMPLOYEE"):
#            print(i)
            t_start=log[i][j]['time:timestamp']
#            print(t_strat)
            break
    for j in reversed(range(len(log[i]))):
        if (log[i][j]['concept:name']=="Declaration REJECTED by EMPLOYEE"):
            t_end=log[i][j]['time:timestamp']
            t=(t_end-t_start).total_seconds()
            through_put[i]=t
            case[i]=int(0)
#            print("REJECTED",t)
            break
        
        if (log[i][j]['concept:name']=="Payment Handled"):           
            t_end=log[i][j]['time:timestamp']
            t=(t_end-t_start).total_seconds()
            through_put[i]=float(t)/86400
#            print("APPROVED",t)
            case[i]=int(1)
            break
# =============================================================================
# END 1
# =============================================================================
#%%
print(through_put)
#%%
# =============================================================================
# 2. for each case, get value of "Requested Amount" (1 value for each case)
# =============================================================================
amount_list=list(df['case:Amount'])
id_list=list(df['case:id'])
amount=[]
set_id=[]
for i in range(len(id_list)):
    if id_list[i] not in set_id:
        set_id.append(id_list[i])
        amount.append(float(amount_list[i]))            
#attribute_values = pm4py.get_trace_attribute_values(log, 'Amount')
#values=list(attribute_values.keys())
#print(len(values))
print("Total amount requested "+str(sum(amount)))
#print(len(amount))
# =============================================================================
# END 2
# =============================================================================

# =============================================================================
# 3. how many approvals each case has? aka: number of events by 
# (Administration / Supervisor / Budget Owner / Pre-Approver / Director.)
# but this should be unique value, i.e: if a case has 1 event "REJECTED by DIRECTOR" and 1 event 
# "APPROVED by DIRECTOR", it should only count as 1 instead of 2
# =============================================================================
staff_list=["PRE_APPROVER","DIRECTOR","SUPERVISOR","BUDGET OWNER","ADMINISTRATION"]
members_involved = []
pre_approver=int(0)
pre_approver_list=[int(0)]*len(log)
director=int(0)
director_list=[int(0)]*len(log)
supervisor=int(0)
supervisor_list=[int(0)]*len(log)
budget_owner=int(0)
budget_owner_list=[int(0)]*len(log)
administrator=int(0)
administrator_list=[int(0)]*len(log)
for i in range(len(log)):
    pre_approver=int(0)
    director=int(0)
    supervisor=int(0)
    budget_owner=int(0)
    administrator=int(0)
    temp=[]
    for j in range(len(log[i])):
        if staff_list[0] in log[i][j]['concept:name']:
            pre_approver=pre_approver+1
            pre_approver_list[i]=int(1)
        if staff_list[1] in log[i][j]['concept:name']:
            director=director+1
            director_list[i]=int(1)
        if staff_list[2] in log[i][j]['concept:name']:
            supervisor=supervisor+1
            supervisor_list[i]=int(1)
        if staff_list[3] in log[i][j]['concept:name']:
            budget_owner=budget_owner+1
            budget_owner_list[i]=int(1)
        if staff_list[4] in log[i][j]['concept:name']:
            administrator=administrator+1
            administrator_list[i]=int(1)
    temp=[pre_approver,director,supervisor,budget_owner,administrator]
    members_involved.append(temp)

#print(staff_list)
level=[int(0)]*len(members_involved)
for i in range(len(members_involved)):
#    print(members_involved[i])
    for j in range(5):
        if members_involved[i][j]>0:
            level[i]=level[i]+int(1)
        
# =============================================================================
# END 3
# =============================================================================

# =============================================================================
# 4. list of cases where DIRECTOR is invovled (this can be done just by filtering I think)
# =============================================================================
from pm4py.algo.filtering.log.attributes import attributes_filter

# Obtaining values in the column "concept:name" with the number of times 
# activities is type dict 
activities = attributes_filter.get_attribute_values(log, "concept:name") 

activity=list(activities.keys())
#list of activity in which director is involved
director_activity=[]

for i in activities:
    if "DIRECTOR" in i:
#        print(i, activities[i])
        director_activity.append(i)

#FILTERING CASES IN WHICH DIRECTOR IS INVOLVED
log_with_director = attributes_filter.apply_events(log, ["Permit REJECTED by DIRECTOR","Declaration REJECTED by DIRECTOR","Declaration FINAL_APPROVED by DIRECTOR","Permit FINAL_APPROVED by DIRECTOR"],parameters={attributes_filter.Parameters.ATTRIBUTE_KEY: "concept:name", attributes_filter.Parameters.POSITIVE: True})
print("The number of cases in which the DIRECTOR is involved :"+ str(len(log_with_director)))

# =============================================================================
# END 4
# =============================================================================
# =============================================================================
# 
# Approved_count=[]
# Rejected_count=[]
# acount=int(0)
# rcount=int(0)
# for i in range(len(log)):
#     acount=int(0)
#     rcount=int(0)
#     for j in range(len(log[i])):
#         if "APPROVED" in str(log[i][j]['concept:name']):
#             acount=acount+1
#         if "REJECTED" in str(log[i][j]['concept:name']):
#             rcount=rcount+1
#     Approved_count.append(acount)
#     Rejected_count.append(rcount)
# #print(Approved_count)
# #print(Rejected_count)
# =============================================================================

     
# =============================================================================
# OBTAINING CASE ID's
# =============================================================================
case_id = pm4py.get_trace_attribute_values(log, 'id')
case_id = list(case_id.keys())

# =============================================================================
# COVERTING OBTAINED DATA TO DATAFRAME AND EXPORTING TO CSV FILE
# =============================================================================
#%%
#print(through_put)
#%%
data={
      'Amount' : amount,
      'SUPERVISOR Involved':supervisor_list,
      'PRE_APPROVER Involved':pre_approver_list,
      'DIRECTOR Involved':director_list,
      'BUDGET_OWNER Involved':budget_owner_list,
      'ADMINISTRATOR Involved':administrator_list,
      'DIRECTOR Involved':director_list,
      'Number Of Levels':level,
      'APPROVED/REJECTED':case,
      'Throughput Time':through_put}
df = pd.DataFrame(data,index=case_id)

df.to_csv(filename)
#df.to_csv('test.csv')
#%%
from pandas import read_csv
import seaborn as sns
import matplotlib.pyplot as plt
data = read_csv(filename, delimiter=",")
to_be_plotted = ['Amount', 'Number Of Levels']
for feature in to_be_plotted:
    x = data[feature]
    y = data['Throughput Time']
    print(y)
    ax = sns.regplot(y=y, x=x, color='darkred')
#    plt.show()
data = read_csv(filename, delimiter=",")
to_be_plotted = ['Amount', 'Number Of Levels']
for feature in to_be_plotted:
    x = data[feature]
    y = data['Throughput Time']
#    ax = sns.regplot(y=y, x=x, color='darkred')
#    plt.show()