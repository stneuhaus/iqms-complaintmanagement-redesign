# Fields on `complaint_intake__v` (Complaint Intake)

Source: `bayersbx-iqms-3-1-dev.veevavault.com`, API `v26.2`. Fields: 39.

| Field | Label | Type | Required | Editable | Max length | Required on type |
| --- | --- | --- | --- | --- | --- | --- |
| `awareness_date__v` | Awareness Date | Date | no | yes | - | - |
| `case_number__v` | Case Number | String | no | yes | 255 | - |
| `case_state__v` | Case State | String | no | yes | 255 | - |
| `comments__v` | Comments | LongText | no | yes | 5000 | - |
| `country_of_incident__v` | Country of Incident | Object | no | yes | - | - |
| `created_by__v` | Created By | Object | no | no | - | - |
| `created_date__v` | Created Date | DateTime | no | no | - | - |
| `date_of_event__v` | Date of Event | Date | no | yes | - | - |
| `description__v` | Description | String | no | yes | 1500 | - |
| `email_body__v` | Email Body | LongText | no | no | 32000 | - |
| `email_text__v` | Email Text | LongText | no | no | 32000 | - |
| `global_id__sys` | Global ID | String | no | no | 200 | - |
| `id` | ID | ID | no | no | - | - |
| `initial_contact_method__v` | Initial Contact Method | Picklist | yes | yes | - | Complaint Intake |
| `initial_report_date__v` | Initial Report Date | Date | yes | yes | - | Complaint Intake |
| `initial_reporter_details__v` | Initial Reporter | String | yes | yes | 1500 | Complaint Intake |
| `lifecycle__v` | Lifecycle | Component | no | no | - | - |
| `link__sys` | Link | String | no | yes | 255 | - |
| `message_id__v` | Message ID | String | no | no | 255 | - |
| `modified_by__v` | Last Modified By | Object | no | no | - | - |
| `modified_date__v` | Last Modified Date | DateTime | no | no | - | - |
| `name__v` | Name | String | yes | no | 128 | Complaint Intake |
| `object_type__v` | Complaint Intake Type | Object | no | no | - | - |
| `pqc_name__v` | Product Quality Complaint Name | String | no | yes | 255 | - |
| `pqc_state__v` | Product Quality Complaint State | String | no | yes | 255 | - |
| `promote_to_complaint__v` | Promote to Complaint Run? | Boolean | no | yes | - | - |
| `promote_to_complaint_required__v` | Promote to Complaint Required? | Boolean | no | yes | - | - |
| `reporter_type__v` | Reporter Type | Picklist | no | yes | - | - |
| `root_message_id__v` | Root Message ID | String | no | no | 1000 | - |
| `sender_email_address__v` | Sender Email Address | String | no | no | 1500 | - |
| `stage__sys` | Lifecycle Stage | Object | no | no | - | - |
| `state__v` | Lifecycle State | Component | no | no | - | - |
| `state_stage_id__sys` | Lifecycle State Stage ID | Object | no | no | - | - |
| `status__v` | Status | Picklist | no | no | - | - |
| `title__v` | Title | String | yes | yes | 255 | Complaint Intake |
| `triage_assessment__v` | Triage Assessment | String | no | yes | 1500 | - |
| `type__v` | Type | Picklist | no | yes | - | - |
| `type_of_complaint__v` | Type of Complaint | Picklist | no | yes | - | - |
| `vault_email_inbox_address__v` | Vault Email Inbox Address | String | no | no | 1500 | - |
