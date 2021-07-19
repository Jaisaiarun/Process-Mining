#%%
import pm4py
# =============================================================================
# import pandas as pd
# from pm4py.objects.log.util import dataframe_utils
# from pm4py.objects.conversion.log import converter as log_converter
# from pm4py.algo.filtering.log.timestamp import timestamp_filter
# =============================================================================
from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.algo.filtering.log.timestamp import timestamp_filter
#%%
log = xes_importer.apply('InternationalDeclarations.xes')
#%% FOR CSV FILE 
# =============================================================================
# log_csv = pd.read_csv(r'InternationalDeclarations.csv', sep=',')
# # TO RENAME THE Case_ID to case:Case_ID
# log_csv.rename(columns={'Case_ID': 'case:Case_ID'}, inplace=True)
# log_csv = dataframe_utils.convert_timestamp_columns_in_df(log_csv)
# # TO COMBINE ALL THE ROWS WITH THE SAME VALUE IN COLUMN RESOURCE
# parameters = {log_converter.Variants.TO_EVENT_LOG.value.Parameters.CASE_ID_KEY: 'Resource'} 
# event_log = log_converter.apply(log_csv, parameters=parameters, variant=log_converter.Variants.TO_EVENT_LOG)
# #log_csv = log_csv.sort_values('Complete Timestamp')
# #event_log = log_converter.apply(log_csv)
# 
# from pm4py.statistics.traces.log import case_statistics
# all_case_durations = case_statistics.get_all_casedurations(event_log, parameters={
#     case_statistics.Parameters.TIMESTAMP_KEY: "2016-05-10 00:00:00"})
# =============================================================================
#%%
print(log[0][0])
#%% TO FILTER LOGS BASED ON TIME STAMP
filtered_log = timestamp_filter.filter_traces_contained(log, "2016-05-10 00:00:00", "2017-03-07 23:59:59")
print(filtered_log)
#%%  traces between 1 and 10 days are kept
from pm4py.algo.filtering.log.cases import case_filter
filtered_log = case_filter.filter_case_performance(log, 86400, 864000)
print(filtered_log)
#%%
from pm4py.algo.filtering.log.start_activities import start_activities_filter
log_start = start_activities_filter.get_start_activities(log)
filtered_log = start_activities_filter.apply(log, ["Start trip"]) #suppose "S1" is the start activity you want to filter on
#print(log_start)
#%%
from pm4py.algo.filtering.log.end_activities import end_activities_filter
log_end = end_activities_filter.get_end_activities(log)
#filtered_log = end_activities_filter.apply(log, ["Start trip"]) #suppose "S1" is the start activity you want to filter on
print(log_end)
#%%
# =============================================================================
# A variant is a set of cases that share the same control-flow perspective, 
# so a set of cases that share the same classified events (activities) in the same order
# FILTERING BY VARIANT
# =============================================================================
from pm4py.algo.filtering.log.variants import variants_filter
variants = variants_filter.get_variants(log)
from pm4py.statistics.traces.log import case_statistics
variants_count = case_statistics.get_variant_statistics(log)
variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)
#%%
#print(variants_count[0])
# KEY : VARIANT AND VALUE : COUNT
variant=[]
count=[]
for i in variants_count:
#    print(i[])
    variant.append(i['variant'])
    count.append(i['count'])
#%%
for i in range(len(variant)-10,len(variant)):
    print(str(variant[i])+"\n")
#%% FOR CALUCLATING THROUGHPUT OF A GIVEN CASE
from pm4py.statistics.traces.log import case_statistics
all_case_durations = case_statistics.get_all_casedurations(log, parameters={
    case_statistics.Parameters.TIMESTAMP_KEY: "time:timestamp"})

print(len(all_case_durations))

# all_case_duration in seconds
#print(all_case_durations[0]/(60*60))
#print(len(all_case_durations))
#%%
from pm4py.algo.filtering.log.attributes import attributes_filter
activities = attributes_filter.get_attribute_values(log, "concept:name")
resources = attributes_filter.get_attribute_values(log, "org:resource")

activity=list(activities.keys())
print(activity)
#%%
#tracefilter_log_pos = attributes_filter.apply_events(log, ["Permit REJECTED by DIRECTOR","Declaration REJECTED by DIRECTOR","Declaration FINAL_APPROVED by DIRECTOR","Permit FINAL_APPROVED by DIRECTOR"],parameters={attributes_filter.Parameters.ATTRIBUTE_KEY: "concept:name", attributes_filter.Parameters.POSITIVE: True})
#tracefilter_log_pos = attributes_filter.apply_events(log,activity,parameters={attributes_filter.Parameters.ATTRIBUTE_KEY: "concept:name", attributes_filter.Parameters.POSITIVE: True})
tracefilter_log_neg = attributes_filter.apply_events(log,["Permit SUBMITTED by EMPLOYEE"],parameters={attributes_filter.Parameters.ATTRIBUTE_KEY: "concept:name", attributes_filter.Parameters.POSITIVE: True})
#%% 
# 6255
print(len(tracefilter_log_neg))

#%%
activity=list(activities.keys())
print(activity)
#DIRECTOR
#%%
sum_dircector=int(0)
for i in activities:
#    if "DIRECTOR" in i:
#    sum_dircector=sum_dircector+activities[i]
    print(i, activities[i])

#print(sum_dircector)
#%%
print(list(activities.keys()))
#%%
staff_list=["PRE_APPROVER","DIRECTOR","SUPERVISOR","BUDGET OWNER","ADMINISTRATION"]
members_involved = []
pre_approver=int(0)
director=int(0)
supervisor=int(0)
budget_owner=int(0)
administrator=int(0)
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
        if staff_list[1] in log[i][j]['concept:name']:
            director=director+1
        if staff_list[2] in log[i][j]['concept:name']:
            supervisor=supervisor+1
        if staff_list[3] in log[i][j]['concept:name']:
            budget_owner=budget_owner+1
        if staff_list[4] in log[i][j]['concept:name']:
            administrator=administrator+1
    temp=[pre_approver,director,supervisor,budget_owner,administrator]
    members_involved.append(temp)
#%%
#print(staff_list)
level=[0]*len(members_involved)
for i in range(len(members_involved)):
#    print(members_involved[i])
    for j in range(5):
        if members_involved[i][j]>0:
            level[i]=level[i]+1
#%%
print(max(level))

#%%
# TRACE ARE ATTRIBUTES WITH "case:" in csv file
#Returns the attributes at the event level of the log.
attributes_list = pm4py.get_attributes(log)
print(attributes_list)
#%%
# Gets the attributes at the trace level of a log object.
attributes_list = pm4py.get_trace_attributes(log)
print(attributes_list)
#%% Returns the values for a specified attribute.
attribute_values = pm4py.get_attribute_values(log, 'concept:name')
print(attribute_values)
#%% Returns the values for a specified trace attribute.
attribute_values = pm4py.get_trace_attribute_values(log, 'id')
print(len(attribute_values))
#%%
values=list(attribute_values.keys())
#print(sum(values))
print(values)

#%%
#REJECTED
#APPROVED
Approved_count=[]
Rejected_count=[]
acount=int(0)
rcount=int(0)
for i in range(len(log)):
    acount=int(0)
    rcount=int(0)
    for j in range(len(log[0])):
        if "APPROVED" in str(log[0][j]['concept:name']):
            acount=acount+1
        if "REJECTED" in str(log[0][j]['concept:name']):
            rcount=rcount+1
        Approved_count.append(acount)
        Rejected_count.append(rcount)
#%%    
print(Approved_count)
#print("APPROVED" in "Declaration FINAL_APPROVED by SUPERVISOR")
#%%
end=[]
for i in range(len(log)):
#    for j in range(1,len(log[i])-1):
#        if (log[i][j]['time:timestamp'] > log[i][j+1]['time:timestamp']):
#            print("false")
#    print(log[i][len(log[i])-1]['concept:name'])
    end.append(log[i][len(log[i])-1]['concept:name'])
#%% 
from pm4py.algo.filtering.log.end_activities import end_activities_filter
end_activities = end_activities_filter.get_end_activities(log)
#filtered_log = end_activities_filter.apply(log, ["pay compensation"])
print(end_activities)
#%%
from pm4py.algo.filtering.log.start_activities import start_activities_filter
start_activities = start_activities_filter.get_start_activities(log)
#filtered_log = start_activities_filter.apply(log, ["S1"]) 
print(start_activities)
#%%
through_put_approved=[0]*len(log)
through_put_rejected=[0]*len(log)
for i in range(len(log)):
#for i in range(5):
    for j in range(len(log[i])):
        if (log[i][j]['concept:name']=="Declaration SUBMITTED by EMPLOYEE"):
#            print(i)
            t_start=log[i][j]['time:timestamp']
#            print(t_strat)
            break
    for j in reversed(range(len(log[i]))):
        if (log[i][j]['concept:name']=="Declaration REJECTED by EMPLOYEE"):
            t_end=log[i][j]['time:timestamp']
            t=(t_end-t_start).total_seconds()
            through_put_rejected[i]=t
#            print("REJECTED",t)
            break
        
        if (log[i][j]['concept:name']=="Payment Handled"):           
            t_end=log[i][j]['time:timestamp']
            t=(t_end-t_start).total_seconds()
            through_put_approved[i]=t
#            print("APPROVED",t)

#print(len(log[1]))            
#t_start=log[1][0]['time:timestamp']            
#t_end=log[1][7]['time:timestamp']
#print(t_end-t_start)
print(through_put_rejected[50:100])
#%%

