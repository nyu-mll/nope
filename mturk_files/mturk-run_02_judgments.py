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
      "QualificationTypeId": g0_qual,
      "Comparator": "Exists",
      "ActionsGuarded": "DiscoverPreviewAndAccept"
    }]

exp_url = "https://nyu-mll.github.io/presupposition_dataset/experiments/02_judgements/experiment.html"
framehight = "650"

for i in range(10):
    this_exp = exp_url + "?stims=" + str(i) + "&amp;list=0;"  # group 0

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
        Reward='2.00',
        Title='Judge sentence likelihood (7-8 min)',
        Keywords='English, rating, reading',
        Description='Read a short text and then judge how likely a statement is (7-8 min)',
        Question=Question,
        RequesterAnnotation='judgments_02_group_0',
        QualificationRequirements=Quals
    )
    
    print("successfully created HIT for stim set %s" % str(i))



#---------------------------------------------------------
# message workers

message_title = "You qualified for our HITs"
message = "Congratulations! You qualified to complete more HITs in our current series on sentence judgments. " \
          "We have just released small number of HITs with the title 'Judge sentence likelihood (7-8 min)' " \
          "as a pilot, and we will be releasing larger batches in the coming weeks."

# response = client.notify_workers(
#         Subject=message_title,
#         MessageText=message,
#         WorkerIds=group0_workers
# )
    
#---------------------------------------------------------
# track and get responses

# list relevant HITs
created_HITs = client.list_hits(MaxResults=10)
HITIds = []
for i in range(10):
    this_id = created_HITs['HITs'][i]['HITId']
    HITIds.append(this_id)

# see number of responses per HIT
for i in range(10):
    worker_results = client.list_assignments_for_hit(HITId=HITIds[i], MaxResults=100)
    print("HIT %s has %d responses" % (str(i), worker_results['NumResults']))

# save files
for i in range(10):
    results, result_types = get_results(HITIds[i])
    outname = "C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/mturk_data/02_judgments_" + str(i) + "_group0.json"
    with io.open(outname, "w") as outfile:
        outfile.write(json.dumps(results))