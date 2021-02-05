import boto3
import pandas as pd
import numpy as np
import json, argparse, os, csv
import xmltodict
import io
import mturk_utils

avp_secrets = pd.read_csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/access_keys_avp.csv")
cds_secrets = pd.read_csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/access_keys_cds.csv")

region_name = 'us-east-1'
aws_access_key_id = cds_secrets['key_id'][0]
aws_secret_access_key = cds_secrets['access_key'][0]

# SANDBOX
#endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

# Uncomment this line to use in production NOT SANDBOX
endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'

client = boto3.client(
    'mturk',
    endpoint_url=endpoint_url,
    region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# This will return $10,000.00 in the MTurk Developer Sandbox
print(client.get_account_balance()['AvailableBalance'])

#-----------------------------------------------------
# Assign workers to groups with quals

worker_ids = pd.read_csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/anon_id_links.csv")
qualified_workers = pd.read_csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/results/01_prescreener/qualified_workers.csv")
worker_groups = worker_ids.merge(qualified_workers, how="inner")

group0 = worker_groups[worker_groups['group']=='group0']
group1 = worker_groups[worker_groups['group']=='group1']
group2 = worker_groups[worker_groups['group']=='group2']
group0_workers = group0['workerid'].tolist()
group1_workers = group1['workerid'].tolist()
group2_workers = group2['workerid'].tolist()

g0_qual = '39VCJNQUAP4BFGR22PHY7AOONL0XCB'
g1_qual = '30YN3SB4AK3QK8TP2K3LMJSR1N302B'
g2_qual = '31LAE79C57FYHR6ZW31PH2SAU4K8GP'

for i in range(len(group2_workers)):
    worker_id = group2_workers[i]
    qual_assignment = client.associate_qualification_with_worker(
        QualificationTypeId=g2_qual,
        WorkerId=worker_id,
        IntegerValue=1,
        SendNotification=False)
    print("assigned qual to %s" % worker_id)

#-----------------------------------------------------
# Set up inputs for study

Quals = [{
      "QualificationTypeId": g2_qual,
      "Comparator": "Exists",
      "ActionsGuarded": "DiscoverPreviewAndAccept"
    }]

exp_url = "https://nyu-mll.github.io/presupposition_dataset/experiments/02_judgements/experiment.html"
framehight = "650"

for i in range(10):
    this_exp = exp_url + "?stims=" + str(i) + "&amp;list=2"  # group 2

    Question = """
        <ExternalQuestion xmlns='http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd'>
          <ExternalURL>{}</ExternalURL>
          <FrameHeight>{}</FrameHeight>
        </ExternalQuestion>
        """.format(this_exp, framehight)

    create = client.create_hit(
        MaxAssignments=5,
        AutoApprovalDelayInSeconds=259200,  # 3 days
        LifetimeInSeconds=259200,  # 3 days
        AssignmentDurationInSeconds=7200,  # 2 hours
        Reward='2.50',
        Title='Judge sentence likelihood (10 min)',
        Keywords='English, rating, reading',
        Description='Read a short text and then judge how likely a statement is (10 min)',
        Question=Question,
        RequesterAnnotation='judgments_02_group_1',
        QualificationRequirements=Quals
    )
    
    print("successfully created HIT for stim set %s" % str(i))



#---------------------------------------------------------
# message workers

message_title = "You qualified for our HITs"
message = "Congratulations! You qualified to complete more HITs in our current series on sentence judgments. " \
          "We have just released small number of HITs with the title 'Judge sentence likelihood (10 min)' " \
          "as a pilot, and we will be releasing larger batches in the coming weeks."

# message_title = "HITs still available -- new bonus attached!"
# message = "We are following up on our message from yesterday about a small batch of HITs titled " \
#           "'Judge sentence likelihood (7-8 min)'. There are still many HITs in this initial batch available, " \
#           "and there is no limit on the number that you can complete! " \
#           "Upon review, we have found that the task can take closer to 10 minutes to complete, so we are paying " \
#           "an additional 50 cents as a bonus on each of these HITs. If you have already completed " \
#           "some, we will be sending out bonuses tomorrow to make up for our initial error in the " \
#           "time estimate."

# response = client.notify_workers(
#         Subject=message_title,
#         MessageText=message,
#         WorkerIds=group2_workers
# )
    
#---------------------------------------------------------
# track and get responses

# list relevant HITs
# created_HITs = client.list_hits(MaxResults=10)
# HITIds_2 = []
# for i in range(10):
#     this_id = created_HITs['HITs'][i]['HITId']
#     HITIds_2.append(this_id)

# df = pd.DataFrame(HITIds_2, columns = ["HITId"])
# df.to_csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/mturk_data/02_judgments/group2_HITIds.csv")

# WHICH GROUP TO LOOK AT
group = 'group2'

if group == 'group0':
    HITIds = HITIds_0
elif group == 'group1':
    HITIds = HITIds_1
elif group == 'group2':
    HITIds = HITIds_2

# see number of responses per HIT
tot = 0
for i in range(10):
    worker_results = client.list_assignments_for_hit(HITId=HITIds[i], MaxResults=100)
    print('HIT %s has %d responses and is %s' % (str(i), worker_results['NumResults'], 
                                                 client.get_hit(HITId=HITIds[i])['HIT']['HITStatus']))
    tot += worker_results['NumResults']
print("A total of %d HITs have been completed for %s" % (tot, group))

# save files
for i in range(10):
    results, result_types = get_results(HITIds[i])
    outname = "C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/" \
              "mturk_data/02_judgments/02_judgments_" + str(i) + "_" + group + ".json"
    with io.open(outname, "w") as outfile:
        outfile.write(json.dumps(results))

# ---------------------------------------------------------
# approve_assignments

#already_approved = []
#g0_assignments = []
for j in range(len(HITIds)):
    this_HITId = HITIds[j]
    if client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['NumResults'] > 0:
        for i in range(client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['NumResults']):
            ass_id = client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['Assignments'][i]['AssignmentId']
            if ass_id not in already_approved:
                approval = client.approve_assignment(
                    AssignmentId=ass_id
                )
                already_approved.append(ass_id)
                print("approved assignment for %s" % client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['Assignments'][i]['WorkerId'])
                if group == 'group0':
                    g0_assignments.append(ass_id)
print("Approved %d total assignments" % len(already_approved))


# ---------------------------------------------------------
# pay bonuses for group0 

