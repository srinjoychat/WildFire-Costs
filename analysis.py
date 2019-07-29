import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

##reading the csv file
df=pd.read_csv("fireCosts.csv",low_memory=False)


##Find number of wildfires in each state
print("Computing number of wildfires in each state: ")
current_df=df.copy()

##Grouping the wildfires by state code
statewise=current_df.groupby(["POO_STATE_CODE"])

##dictonary to store number of fires in each state
fireCount={}
for key in statewise.groups.keys():
    state_df=current_df.loc[current_df["POO_STATE_CODE"]==key]
    numFires=state_df["INC_IDENTIFIER"].nunique()
    fireCount[key]=numFires

print(fireCount)

##Plotting bar plot for number of fires
plt.figure()
plt.bar([i for i in range(len(fireCount))], fireCount.values())
plt.xlabel("State ID")
plt.ylabel("Number of Wildfires")

##Finding statistics of fire duration
print("Computing statistics of wildfire durations: ")

current_df=df.copy()
current_df=current_df[["INC_IDENTIFIER", "REPORT_FROM_DATE", "REPORT_TO_DATE"]]

##Compute duration of each wildfire in mins using the datetime objects in Python
def getTime(initString, finalString):
    ##return time if report_from and report_to entries are valid
    if type(initString)==str and type(finalString)==str:
        initDatetime=datetime.datetime.strptime(initString,'%Y-%m-%d %H:%M:%S')
        finalDatetime=datetime.datetime.strptime(finalString,'%Y-%m-%d %H:%M:%S')

        elapsedTime=finalDatetime-initDatetime
        elapsedTime=elapsedTime.total_seconds() /60

        return (True,elapsedTime)

    return (False,0)


##Compute global statistics on wildfire duration
fireDuration={}
for incident in current_df["INC_IDENTIFIER"].unique():
    incident_df=current_df[current_df["INC_IDENTIFIER"]==incident]

    incidentFlag,incidentDuration=getTime(incident_df["REPORT_FROM_DATE"].values[0],incident_df["REPORT_TO_DATE"].values[-1])

    if incidentFlag:
        fireDuration[incident]=incidentDuration


times=[val for val in fireDuration.values()]
totalMean=np.mean(times)
totalStd=np.std(times)
print("Mean wildfire duration (in mins): "+str(np.mean(times)))
print("Standard deviation in wildfire duration (in mins)"+ str(np.std(times)))


##Finding statewise statistics of wildfire duration

print("Computing statewise statistics of wildfire durations: ")
current_df=df.copy()
statewise=current_df.groupby(["POO_STATE_CODE"])
fireCount={}

stateMean={}
stateStd={}

for key in statewise.groups.keys():
    state_df=current_df.loc[current_df["POO_STATE_CODE"]==key]
    fireDuration = {}
    for incident in state_df["INC_IDENTIFIER"].unique():
        incident_df = state_df[state_df["INC_IDENTIFIER"] == incident]

        incidentFlag, incidentDuration = getTime(incident_df["REPORT_FROM_DATE"].values[0],
                                                 incident_df["REPORT_TO_DATE"].values[-1])

        if incidentFlag:
            fireDuration[incident] = incidentDuration

    times = [val for val in fireDuration.values()]

    stateMean[key]=np.mean(times)
    stateStd[key]= np.std(times)


##Plotting statewise mean and standard deviation along with global statistics
plt.figure()
plt.subplot(2,1,1)
plt.plot([i for i in range(len(stateMean))], stateMean.values(),'rd')
plt.hlines(totalMean*np.ones(len(stateMean)),xmin=0, xmax=len(stateMean.keys()))
plt.grid()
plt.xlabel("State ID")
plt.ylabel("Mean of duration")

plt.subplot(2,1,2)
plt.plot([i for i in range(len(stateMean))], stateStd.values(),'rd')
plt.hlines(totalStd*np.ones(len(stateStd)),xmin=0, xmax=len(stateMean.keys()))
plt.grid()
plt.xlabel("State ID")
plt.ylabel("Standard Deviation of duration")
plt.show()



