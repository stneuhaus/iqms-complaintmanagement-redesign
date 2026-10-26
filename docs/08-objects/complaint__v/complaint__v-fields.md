# Fields on `complaint__v` (Complaint)

Source: `bayersbx-iqms-3-1-dev.veevavault.com`, API `v26.2`. Fields: 223.

| Field | Label | Type | Required | Editable | Max length | Required on type |
| --- | --- | --- | --- | --- | --- | --- |
| `adverse_event__v` | Adverse Event Reported? * | Boolean | no | yes | - | - |
| `adverse_event_outcomes__v` | Adverse Event Type * | Picklist | no | yes | - | - |
| `ae_classification__v` | Classification of Incident | Picklist | no | yes | - | - |
| `ae_description__v` | Description of the Adverse Event | String | no | yes | 1500 | - |
| `ae_severity__v` | Severity Outcome | Picklist | no | yes | - | - |
| `age__v` | Age | Number | no | yes | - | - |
| `age_unit__v` | Age Unit | Picklist | no | yes | - | - |
| `alert_received__c` | Alert Received? | Boolean | no | yes | - | - |
| `amendment_date__v` | Amendment Date | Date | no | yes | - | - |
| `argus_notification_requested__c` | Argus Notification Requested | DateTime | no | yes | - | - |
| `attlas_alert_code__c` | ATTLAS Alert Code | String | no | yes | 14 | - |
| `attlas_alert_date__c` | ATTLAS Alert Date | Date | no | yes | - | - |
| `attlas_data_upload_time__c` | ATTLAS DATA Upload Time | String | no | yes | 32 | - |
| `attlas_emvs_report_status__c` | ATTLAS EMVS Report Status | String | no | yes | 60 | - |
| `attlas_emvs_report_type__c` | ATTLAS EMVS Report Type | String | no | yes | 20 | - |
| `attlas_production_site__c` | ATTLAS Production Site | String | no | yes | 20 | - |
| `attlas_sgtin__c` | ATTLAS SGTIN | String | no | yes | 99 | - |
| `attlas_sgtin_status__c` | ATTLAS SGTIN Status | String | no | yes | 20 | - |
| `authority_reference_number__c` | Authority Reference Number | String | no | yes | 50 | - |
| `awareness_date__v` | Initial Receipt Date | Date | no | yes | - | - |
| `bay_project_id__c` | Bay Project ID | String | no | yes | 150 | - |
| `cancellation_reason_justification__v` | Cancellation Reason/Justification | String | no | yes | 1500 | - |
| `capa_notification_rationale__v` | CAPA Notification Rationale | String | no | yes | 1500 | - |
| `capa_plan_summary__v` | CAPA Justification | String | no | yes | 1500 | - |
| `capa_required__v` | CAPA Required?** | Boolean | no | yes | - | - |
| `capa_schedule__v` | CAPA Schedule | String | no | yes | 1500 | - |
| `catalog_number_marketing_product_name__c` | Catalog Number / Marketing Product Name | String | no | yes | 30 | - |
| `cause_investigation_type_of_inv_2__c` | Cause Investigation: Type of Inv. - 2 | Object | no | yes | - | - |
| `cause_investigation_type_of_inv__c` | Cause Investigation: Type of Inv. - 3 | Object | no | yes | - | - |
| `cmo_date_received__c` | Third Party Date Received | Date | no | yes | - | - |
| `cmo_date_sent__c` | Third Party Due Date | Date | no | yes | - | - |
| `combination_product_type__c` | Combination Product Type | Picklist | no | yes | - | - |
| `comments__v` | Comments | String | no | yes | 1500 | - |
| `comments_on_trends_identified__c` | Comments on Trends Identified | String | no | yes | 1500 | - |
| `complainant__v` | Complainant | Object | no | yes | - | - |
| `complainant_contact_information__v` | Complainant Contact Information | Object | no | yes | - | - |
| `complainant_type__v` | Complainant Type | Picklist | no | yes | - | - |
| `complaint_intake__v` | Complaint Intake | Object | no | yes | - | - |
| `complaint_type__c` | Complaint Type * | Picklist | no | yes | - | - |
| `completed_complaint__v` | Completed Complaint | Object | no | yes | - | - |
| `completed_complaint_unbound__v` | Completed Complaint (unbound) | Number | no | yes | - | - |
| `component_involved_in_complaint__c` | Component Involved in Complaint | String | no | yes | 1500 | - |
| `conclusion__c` | Conclusion** | Picklist | no | yes | - | - |
| `conclusion_on_complaint_description__c` | Conclusion on Complaint Description** | Picklist | no | yes | - | - |
| `confirmed_lot__v` | Confirmed Lot Number | String | no | yes | 100 | - |
| `contract_manufacturer__c` | Third Party? * | Boolean | no | yes | - | - |
| `counterfeit_falsification_confirmed__c` | Counterfeit / Falsification Confirmed?* | Boolean | no | yes | - | - |
| `country_of_incident__v` | Country of Event / Incident * | Object | no | yes | - | - |
| `country_where_product_purchased__c` | Country Where Product Purchased | Object | no | yes | - | - |
| `created_by__v` | Created By | Object | no | no | - | - |
| `created_date__v` | Created Date | DateTime | no | no | - | - |
| `crm_reference_number__c` | CRM / Reference Number | String | no | yes | 50 | - |
| `customer_contact__v` | Customer Contact | String | no | yes | 500 | - |
| `customer_forbids_further_contact__c` | Customer Forbids Further Contact? * | Boolean | no | yes | - | - |
| `customer_response_required__c` | Customer Response Required? * | Boolean | no | yes | - | - |
| `date_closed__v` | Date Closed | Date | no | yes | - | - |
| `date_of_birth__v` | Date of Birth | Date | no | yes | - | - |
| `date_of_death__v` | Date of Death | Date | no | yes | - | - |
| `date_of_event__v` | Date of Occurrence | Date | no | yes | - | - |
| `date_of_event_to__v` | Date of Event - To | Date | no | yes | - | - |
| `date_received__v` | Awareness Date * | Date | no | yes | - | - |
| `date_return_requested__v` | Date Return Requested | Date | no | yes | - | - |
| `date_sample_received_at_qu__c` | Date Sample Received at QU | Date | no | yes | - | - |
| `days_open__v` | Days Open | Number | no | no | - | - |
| `department_where_root_cause_occurred__c` | Department where Root Cause Occurred | Object | no | yes | - | - |
| `description__v` | Description | RichText | no | yes | 32000 | Complaint |
| `description_of_manufacturers_evaluation__c` | Description of Manufacturer's Evaluation | RichText | no | yes | 5000 | - |
| `description_of_the_action__c` | Description of the Action | String | no | yes | 1500 | - |
| `device_serial__v` | Device Serial # | String | no | yes | 1000 | - |
| `did_the_component_malfunction__c` | Did the Component Malfunction? | Boolean | no | yes | - | - |
| `division__c` | Division * | Picklist | no | yes | - | - |
| `due_date__v` | Current Due Date | Date | no | yes | - | - |
| `email_body__v` | Email Body | LongText | no | no | 32000 | - |
| `email_text__v` | Email Text | LongText | no | no | 32000 | - |
| `escalation_required__c` | Immediate Escalation Required? | Boolean | no | yes | - | - |
| `ethnicity__v` | Ethnicity | Picklist | no | yes | - | - |
| `expiration_date__v` | Expiration Date | Date | no | yes | - | - |
| `extent_of_defect__c` | Extent of defect/impact on batches** | Picklist | no | yes | - | - |
| `external_link_url__c` | External Link URL | String | no | yes | 320 | - |
| `external_system_number__c` | External System Number | String | no | yes | 50 | - |
| `external_system_type__c` | External System Type | Picklist | no | yes | - | - |
| `feedback_type__c` | Feedback Type * | Picklist | no | yes | - | - |
| `field_correction_required__v` | Field Correction Required? | Boolean | no | yes | - | - |
| `final_comments_from_manufacturer__c` | Final Comments from Manufacturer  | String | no | yes | 1500 | - |
| `final_reportability_determination__c` | Final Reportability Determination? | Boolean | no | yes | - | - |
| `firmware_version_number__c` | Firmware Version Number | String | no | yes | 15 | - |
| `from__v` | From | Object | no | yes | - | - |
| `further_investigations__v` | Further Investigations | String | no | yes | 1500 | - |
| `gbs__c` | GBS | Picklist | no | no | - | - |
| `gender__v` | Gender | Picklist | no | yes | - | - |
| `gender_other__v` | Gender - Other | String | no | yes | 40 | - |
| `global_id__sys` | Global ID | String | no | no | 200 | - |
| `global_safety_database_number__c` | Global Safety Database Number | String | no | yes | 150 | - |
| `healthcare_facility_number__v` | Healthcare Facility Report Number | String | no | yes | 50 | - |
| `how_long_device_used__v` | How Long Device Used? | String | no | yes | 1500 | - |
| `id` | ID | ID | no | no | - | - |
| `immediate_action_taken__v` | Immediate Action Taken | String | no | yes | 1500 | - |
| `impact_assessment_required__v` | Impact Assessment Required? | Boolean | no | yes | - | - |
| `impact_on_other_batches__c` | Impact on Other Batches | String | no | yes | 1500 | - |
| `impact_risk_analysis__v` | Impact and Risk Analysis | RichText | no | yes | 32000 | - |
| `implant_date__v` | Implant Date | Date | no | yes | - | - |
| `incident_location__v` | Location of Incident | Picklist | no | yes | - | - |
| `incident_location_other__v` | Location of Incident - Other | String | no | yes | 1500 | - |
| `initial_contact_method__v` | Initial Contact Method | Picklist | no | yes | - | - |
| `initial_report_date__v` | Initial Report Date | Date | no | yes | - | - |
| `initial_reporter__c` | Initial Reporter | Object | no | yes | - | - |
| `initial_reporter__v` | Reporter | Object | no | yes | - | - |
| `initial_reporter_role__v` | Role of Initial Reporter | Picklist | no | yes | - | - |
| `initial_review_date_by_quality__c` | Initial Review Date by QU* | Date | no | yes | - | - |
| `initial_risk_classification__c` | Initial Risk Classification* | Picklist | no | yes | - | - |
| `investigation_start_date__c` | Investigation Start Date | Date | no | yes | - | - |
| `investigation_summary_and_conclusion__c` | Investigation Summary and Conclusion* | RichText | no | yes | 5000 | - |
| `issue_category__c` | Defect Category** | Picklist | no | yes | - | - |
| `justification__v` | Justification | String | no | yes | 1500 | - |
| `latest_info_date__v` | Latest Info Available Date | Date | no | yes | - | - |
| `legacy__c` | Legacy System Number | String | no | yes | 15 | - |
| `legal_manufacturer__c` | Legal Manufacturer | Object | no | yes | - | - |
| `lifecycle__v` | Lifecycle | Component | yes | no | - | Complaint |
| `link__sys` | Link | String | no | yes | 255 | - |
| `local_closure__c` | Local Closure? | Boolean | no | yes | - | - |
| `manufacturer_initial_actions_implemented__c` | Manufacturer Initial Actions Implemented | String | no | yes | 1500 | - |
| `medication_number__c` | Medication Number | String | no | yes | 150 | - |
| `message_id__v` | Message ID | String | no | no | 255 | - |
| `mfg_date__v` | Manufacture Date | Date | no | yes | - | - |
| `mfg_final_comments_cause__v` | Final Comments | String | no | yes | 1500 | - |
| `mfg_narrative__v` | AE - Manufacturer Narrative | String | no | yes | 1500 | - |
| `mfg_report_number__v` | Mfg Report # | String | no | yes | 21 | - |
| `mfg_site_contact_info__v` | Manufacturing Site - Contact Info | Object | no | yes | - | - |
| `miidas_ae_number__c` | MIIDAS AE Number | String | no | yes | 50 | - |
| `miidas_number_ptc__c` | MIIDAS Number (PTC) | String | no | yes | 50 | - |
| `modified_by__v` | Last Modified By | Object | no | no | - | - |
| `modified_date__v` | Last Modified Date | DateTime | no | no | - | - |
| `multiple_devices__v` | Incident Involves Multiple Devices? | Boolean | no | yes | - | - |
| `name__v` | Identifier | String | yes | no | 128 | Complaint |
| `new_hazards_risk_identified__c` | Is Risk Assessment Adequate? | Boolean | no | yes | - | - |
| `non_reportable_explanation__v` | Non-Reportable Incident - Explanation | String | no | yes | 1500 | - |
| `notify_capa_team__v` | Notify CAPA Team | Boolean | no | yes | - | - |
| `number_of_bundled_cases__c` | Number of Cases | Number | no | yes | - | - |
| `number_of_complaint_packages1__c` | Number of Complained Packages * | Number | no | yes | - | - |
| `number_of_patients__v` | Number of Patients Involved | Number | no | yes | - | - |
| `object_type__v` | Complaint Object Type | Object | no | no | - | - |
| `origin_of_issue_or_defect__c` | Origin of Issue or Defect** | Picklist | no | yes | - | - |
| `original_due_date__v` | Original Due Date | Date | no | yes | - | - |
| `other_adverse_event_numbers__c` | Other Adverse Event Number(s) | String | no | yes | 1500 | - |
| `other_history__v` | Other Relevant History | String | no | yes | 1500 | - |
| `owner__v` | Owner | Object | no | yes | - | - |
| `patient_consequences__v` | Patient Consequences | String | no | yes | 1500 | - |
| `patient_id__v` | Patient ID | String | no | yes | 100 | - |
| `patient_sex__v` | Patient’s Sex | Picklist | no | yes | - | - |
| `photos_available_for_investigation__c` | Photos Available for Investigation? * | Boolean | no | yes | - | - |
| `physical_sample_available_for_return__c` | Physical Sample Available for Return? * | Boolean | no | yes | - | - |
| `probability__v` | Probability | Picklist | no | yes | - | - |
| `product__v` | Product | Object | no | yes | - | - |
| `product_family__v` | Product Family | Object | no | yes | - | - |
| `product_type__c` | Product Type * | Picklist | no | yes | - | - |
| `product_variant__v` | Product Variant | Object | no | yes | - | - |
| `production_line_packaging_line__c` | Production Line / Packaging Line | String | no | yes | 1500 | - |
| `projected_timing_final__c` | Projected Timing Final | String | no | yes | 1500 | - |
| `race__v` | Race | Picklist | no | yes | - | - |
| `rating__v` | Final Risk Classification** | Picklist | no | yes | - | - |
| `rationale_for_abbreviated_workflow__c` | Rationale for Abbreviated Workflow | Picklist | no | yes | - | - |
| `rationale_for_local_closure__c` | Rationale for Local Closure | Picklist | no | yes | - | - |
| `reason_for_change_capture__v` | Reason For Change Capture | LongText | no | yes | 32000 | - |
| `record_check_result__v` | Record Check Result | Object | no | yes | - | - |
| `record_check_result_state__v` | Record Check Result State | Component | no | no | - | - |
| `related_document__c` | Complaint Response Letter | Object | no | yes | - | - |
| `related_document_unbound__c` | Related Document (unbound) | Number | no | yes | - | - |
| `related_issue_escalation__v` | Related Issue Escalation | Object | no | yes | - | - |
| `related_quality_incident__v` | Related Quality Incident | Object | no | yes | - | - |
| `reply_to__v` | Reply To | Object | no | yes | - | - |
| `report_source__c` | Report Source * | Picklist | no | yes | - | - |
| `reported_lot__v` | Reported Lot Number | String | no | yes | 100 | - |
| `reporter_contact_info__v` | Reporter's Contact Information | Object | no | yes | - | - |
| `reporter_occupation__v` | Reporter - Occupation | Picklist | no | yes | - | - |
| `reporter_organization__v` | Reporter Organization | Object | no | yes | - | - |
| `reporter_type__v` | Reporter / Complainant Type * | Picklist | no | yes | - | - |
| `response_summary__v` | Response Summary | String | no | yes | 1500 | - |
| `risk_assessment_reviewed__c` | Risk Assessment Reviewed? | Boolean | no | yes | - | - |
| `root_cause_analysis__v` | Root Cause Analysis | String | no | yes | 1500 | - |
| `root_cause_confirmed__v` | Root Cause Confirmed? | Boolean | no | yes | - | - |
| `root_message_id__v` | Root Message ID | String | no | no | 1000 | - |
| `sample_description__c` | Sample Description | String | no | yes | 1500 | - |
| `sample_description_at_qu__c` | Sample Description at QU | String | no | yes | 1500 | - |
| `sample_received_at_qu__c` | Sample Received at QU?* | Boolean | no | yes | - | - |
| `sample_requested__v` | (Do not use) Sample Requested | Boolean | no | yes | - | - |
| `sender_email_address__v` | Sender Email Address | String | no | no | 1500 | - |
| `service_notification_number__c` | Service Notification Number | String | no | yes | 150 | - |
| `service_organization__c` | Service Organization | Picklist | no | yes | - | - |
| `service_request_number__c` | Service Request Number | String | no | yes | 150 | - |
| `severity__v` | Severity | Picklist | no | yes | - | - |
| `severity_category__c` | Severity Category | Picklist | no | yes | - | - |
| `site__c` | Owning Organization * | Object | no | yes | - | - |
| `site_where_defect_occurred__c` | Organization where Root Cause Occurred** | Object | no | yes | - | - |
| `software_version_number__c` | Software Version Number | String | no | yes | 15 | - |
| `specific_response_required__c` | Specific Response Required | String | no | yes | 1500 | - |
| `stage__sys` | Lifecycle Stage | Object | no | no | - | - |
| `state__v` | Lifecycle State | Component | yes | no | - | Complaint |
| `state_stage_id__sys` | Lifecycle State Stage ID | Object | no | no | - | - |
| `status__v` | Status | Picklist | yes | no | - | Complaint |
| `study_center__c` | Study Center | String | no | yes | 1500 | - |
| `study_id__c` | Study ID | String | no | yes | 1500 | - |
| `symptom_code__v` | Symptom Code | Picklist | no | yes | - | - |
| `sys_imdrf_created__c` | SYS_IMDRF_Created? | Boolean | no | yes | - | - |
| `sys_issue_escalation_initiated__c` | SYS_Issue Escalation Initiated | Boolean | no | yes | - | - |
| `sys_revised__c` | SYS_Revised? | Boolean | no | yes | - | - |
| `template__c` | Template? | Boolean | yes | yes | - | Complaint |
| `template_description__c` | Template Description | String | no | yes | 150 | - |
| `template_name__c` | Template Name | String | no | yes | 150 | - |
| `timeline__c` | Timeline | Picklist | no | yes | - | - |
| `title__v` | Title * | String | no | yes | 150 | - |
| `trend_identified__c` | Trend Identified? | Boolean | no | yes | - | - |
| `type__v` | Type | Picklist | no | yes | - | - |
| `udi__v` | Unique Device Identifier (UDI) | String | no | yes | 1500 | - |
| `uf_importer_awareness_date__v` | UF / Importer - Awareness Date | Date | no | yes | - | - |
| `unique_alert_id__c` | Unique Alert ID | String | no | yes | 1500 | - |
| `unknown_batch_serial_number__c` | Batch / Serial Number Status * | Picklist | no | yes | - | - |
| `vault_email_inbox_address__v` | Vault Email Inbox Address | String | no | no | 1500 | - |
| `weight__v` | Weight | Number | no | yes | - | - |
| `weight_unit__v` | Weight Unit | Picklist | no | yes | - | - |
| `why_physical_sample_is_not_available__c` | Why Physical Sample not Available/Needed | Picklist | no | yes | - | - |
| `why_risk_assessment_is_not_reviewed__c` | Why Risk Assessment is not reviewed? | String | no | yes | 1500 | - |
| `within_warranty__v` | Within Warranty? | Picklist | no | yes | - | - |
| `year__c` | Year | Number | no | yes | - | - |
