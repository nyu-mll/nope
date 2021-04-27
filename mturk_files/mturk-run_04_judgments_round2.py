import boto3
import pandas as pd
import numpy as np
import json, argparse, os, csv
import xmltodict
import io
import mturk_utils
import datetime
from pytz import timezone

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
# check workers groups and quals

worker_ids = pd.read_csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/anon_id_links.csv")
qualified_workers = pd.read_csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/presupposition_dataset/results/01_prescreener/qualified_workers_all.csv")
worker_groups = worker_ids.merge(qualified_workers, how="inner")

group0 = worker_groups[worker_groups['group']=='group0']
group1 = worker_groups[worker_groups['group']=='group1']
group0_workers = group0['workerid'].tolist()
group1_workers = group1['workerid'].tolist()

g0_qual = '39VCJNQUAP4BFGR22PHY7AOONL0XCB'
g1_qual = '30YN3SB4AK3QK8TP2K3LMJSR1N302B'
sufficient_completed = '3XQ9J27GI6KR2C3EAATQ7K56T9EMHI'

# for i in range(len(group1_workers)):
#     worker_id = group1_workers[i]
#     qual_assignment = client.associate_qualification_with_worker(
#         QualificationTypeId=g1_qual,
#         WorkerId=worker_id,
#         IntegerValue=1,
#         SendNotification=False)
#     print("assigned qual to %s" % worker_id)

for i in range(len(workers_completed)):
    worker_id = workers_completed_1[i]
    qual_assignment = client.associate_qualification_with_worker(
        QualificationTypeId=sufficient_completed_1,
        WorkerId=worker_id,
        IntegerValue=1,
        SendNotification=False)
    print("assigned qual to %s" % worker_id)

# response = client.list_workers_with_qualification_type(
#     QualificationTypeId=sufficient_completed,
#     Status='Granted',
#     MaxResults=99
# )
#
# for i in range(len(response['Qualifications'])):
#     worker_id = response['Qualifications'][i]['WorkerId']
#     qual_assignment = client.disassociate_qualification_from_worker(
#         QualificationTypeId=sufficient_completed,
#         WorkerId=worker_id,
#         Reason="Eligible to complete additional HITs")
#     print("dissociated qual from %s" % worker_id)

#-----------------------------------------------------
# Set up inputs for study
infos = [(g0_qual, "0"), (g1_qual, "1")]

for inf in range(len(infos)):
    Quals = [{
          "QualificationTypeId": infos[inf][0],
          "Comparator": "Exists",
          "ActionsGuarded": "DiscoverPreviewAndAccept"
        },
        {
          "QualificationTypeId": sufficient_completed,
          "Comparator": "DoesNotExist",
          "ActionsGuarded": "DiscoverPreviewAndAccept"
        }]

    exp_url = "https://nyu-mll.github.io/presupposition_dataset/experiments/04_judgements_round2/experiment.html"
    framehight = "650"

    for i in range(1, 10):
        this_exp = exp_url + "?stims=" + str(i) + "&amp;list=" + infos[inf][1]

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
            Reward='2.5',
            Title='Judge sentence likelihood (10 min)',
            Keywords='English, rating, reading',
            Description='Read a short text and then judge how likely a statement is (10 min). You can complete multiple HITs.',
            Question=Question,
            RequesterAnnotation='04_judgments_group_%s_list_%s' % (infos[inf][1], str(i)),
            QualificationRequirements=Quals
        )

        print("successfully created HIT for stim set %s" % str(i))

#---------------------------------------------------------
# message workers

message_title = "HITs that you qualified for are now available"
message = "Congratulations! You qualified to complete more HITs in our current series on sentence judgments. " \
          "We have just released another batch of HITs with the title 'Judge sentence likelihood (10 min)'. " \
          "We'll be releasing batches of HITs throughout the day from now through Wednesday, and you can complete " \
          "a total of 10 HITs. "

# response = client.notify_workers(
#         Subject=message_title,
#         MessageText=message,
#         WorkerIds=group1_workers
# )

#---------------------------------------------------------
# track and get responses

# list relevant HITs
created_HITs = client.list_hits(MaxResults=20)
HITIds = []
for i in range(len(created_HITs['HITs'])):
    this_id = created_HITs['HITs'][i]['HITId']
    HITIds.append(this_id)

# df = pd.DataFrame(HITIds, columns = ["HITIds"])
# df.to_csv("C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/mturk_data/04_judgments_part2/batch1_HITIds.csv")

# see number of responses per HIT
tot = 0
for i in range(len(HITIds)):
    worker_results = client.list_assignments_for_hit(HITId=HITIds[i], MaxResults=100)
    print('HIT %s has %d responses of %d and is %s' % (client.get_hit(HITId=HITIds[i])['HIT']['RequesterAnnotation'],
                                                       worker_results['NumResults'],
                                                       client.get_hit(HITId=HITIds[i])['HIT']['MaxAssignments'],
                                                       client.get_hit(HITId=HITIds[i])['HIT']['HITStatus']))
    tot += worker_results['NumResults']
print("A total of %d HITs have been completed" % tot)

# save files
for i in range(len(HITIds)):
    results, result_types = get_results(HITIds[i])
    outname = "C:/Users/NYUCM Loaner Access/Documents/GitHub/SECRET/presup_dataset_SECRET/" \
              "mturk_data/04_judgments_part2/" + client.get_hit(HITId=HITIds[i])['HIT']['RequesterAnnotation'] + ".json"
    with io.open(outname, "w") as outfile:
        outfile.write(json.dumps(results))

# ---------------------------------------------------------
# approve_assignments

#already_approved = []
#approved_ids = []
for j in range(len(HITIds)):
    this_HITId = HITIds[j]
    if client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['NumResults'] > 0:
        for i in range(client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['NumResults']):
            ass_id = client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['Assignments'][i]['AssignmentId']
            #if ass_id not in already_approved:
            if client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['Assignments'][i]['AssignmentStatus'] == 'Submitted':
                approval = client.approve_assignment(
                    AssignmentId=ass_id
                )
                already_approved.append(ass_id)
                approved_ids.append(client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['Assignments'][i]['WorkerId'])
                print("approved assignment for %s" % client.list_assignments_for_hit(HITId=this_HITId, MaxResults=50)['Assignments'][i]['WorkerId'])
print("Approved %d total assignments" % len(already_approved))

df_approved = pd.DataFrame(approved_ids, columns=['worker_id'])
df_approved.worker_id.value_counts()

# ---------------------------------------------------------
# extend time of HITs
tz = timezone('EST')

for idd in HITIds:
    response = client.update_expiration_for_hit(
        HITId=idd,
        ExpireAt=datetime.datetime(2021, 4, 5, 4, 45, 15, tzinfo=tz)
    )

# check who's completed which HIT
for i in range(client.list_assignments_for_hit(HITId='3THR0FZ95QVO2NL8NZ6JF52MONYLOJ', MaxResults=50)['NumResults']):
    print(client.list_assignments_for_hit(HITId='3THR0FZ95QVO2NL8NZ6JF52MONYLOJ', MaxResults=50)['Assignments'][i]['WorkerId'])
