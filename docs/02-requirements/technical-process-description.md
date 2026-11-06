# Description of Proposed technical Process implementation

This description provides a high-level overview of the process steps required to

- extract the text from an incoming complaint email (including attachements),
- translate the content and attachments,
- extract relevant data,
- map them to data fields of downstream systems,
- categorize and classify the complaint, and
- transfer the processed information to downstream systems.

## Step One (Receiving Complaints)

GBR provides several intake email adresses. Email accounts are specfic for a dedicated product or for a country or for bundle of cuntries (e.g.BeNeLux  Belgium Netherlands Belgium). ServiceNow receives such emails as eml files.

# Step Two (Intake of Complaints to ServiceNow)

ServiceNow (SN) receives email and creates a incident object in SN based on that. The incident object owns the sender name and the content of the email body including the email attachments as file attachments. Based on the incomming email adress a specific solvergoup will be assigned. At that moment it is unclear what type of incident it is. The status is open. No agent (complaint manager) is assigned to the incident.