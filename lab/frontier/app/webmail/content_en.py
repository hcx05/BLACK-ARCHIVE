"""English content pack for ROSTER webmail. Selected at Docker build time
(see Dockerfile ARG LANG) - webmail.py never branches on language."""

EMAILS = [
    {"from": "facilities@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2555-03-17 09:12",
     "subject": "New printer arriving 2nd floor next week",
     "body": ("The replacement for the 2nd floor printer ships Thursday. Yes, the\n"
              "same one that's been out of the darker toner cartridge on and off\n"
              "for as long as anyone can remember. IT will handle setup, no action\n"
              "needed from the floor.")},
    {"from": "hr@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2555-03-15 08:30",
     "subject": "Reminder: submit Q1 expense reports by Friday",
     "body": ("Late submissions roll to next quarter's batch and take longer to\n"
              "process. If you're missing a receipt, use the standard exception\n"
              "form instead of holding the whole report.")},
    {"from": "security@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2555-03-10 13:05",
     "subject": "Building 4 fire drill - Thursday 1400",
     "body": ("Standard annual drill, no equipment testing this cycle. Assemble at\n"
              "the usual lot behind Building 2. Should take about fifteen minutes.")},
    {"from": "hr@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-19 08:03",
     "subject": "Mandatory Annual Compliance Training - Due End of Month",
     "body": ("This is your second reminder. Records show 41% completion for Region 4.\n"
              "The module takes approximately 25 minutes. Access it through the HR\n"
              "portal, not through ROSTER - several people have submitted tickets\n"
              "about this and ROSTER was never going to have it.\n\n"
              "Supervisors: please follow up with staff who have not completed this.")},
    {"from": "facilities@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-18 14:02",
     "subject": "Water shutoff - Building 4, Tuesday 0600-0900",
     "body": ("Maintenance is replacing a valve on the third floor. Water will be\n"
              "unavailable in Building 4 (this includes the break room and both\n"
              "restrooms on our floor) from 0600 to approximately 0900 local.\n"
              "Building 2 facilities are unaffected if you need to relocate.")},
    {"from": "facilities@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-17 16:40",
     "subject": "Elevator B Out of Service",
     "body": ("Elevator B is out of service pending a part that's on backorder.\n"
              "Estimated return to service is unknown. Please use Elevator A or\n"
              "the stairwell by the east entrance. We are aware this is the third\n"
              "time this year.")},
    {"from": "t.reyes@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-16 09:47",
     "subject": "re: printer on 2nd floor again",
     "body": ("Yeah I know. It's out of the darker toner cartridge, not the standard\n"
              "one, so it's going to be a few days - vendor doesn't stock it locally.\n"
              "Use the one by the break room until then. Sorry.")},
    {"from": "t.reyes@ocpa.unsc.mil", "to": "k.torres@ocpa.unsc.mil", "date": "2547-02-15 17:52",
     "subject": "you're not going to believe this",
     "body": ("Told my supervisor about the transfer_ref thing again (yes, again) and\n"
              "got the exact same \"it's a known migration artifact, don't open a\n"
              "ticket\" answer, word for word, like it's copy-pasted. Which it probably\n"
              "is.\n\n"
              "Anyway. Drinks Friday?")},
    {"from": "t.reyes@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-13 16:20",
     "subject": "RE: RE: SPINDLE decommission - final sign-off checklist",
     "body": ("Compliance signed off, Records signed off. Putting this to bed on our\n"
              "end - full checklist below for the file.\n\n"
              "> On 2547-02-12, S. Andrade (Compliance) wrote:\n"
              "> Compliance sign-off: no objection to decommission proceeding.\n"
              "> Disposition of acquisition-era material handled separately per\n"
              "> Cmdr. Petrov's office, not in Compliance's remit to review further.\n"
              ">\n"
              "> > On 2547-02-12, N. Okafor (Records, temp. migration support) wrote:\n"
              "> > Batch reindex complete for Eridanus II / Madrigal cases, migrated\n"
              "> > to LEDGER. Couple of odd transfer-reference entries carried over\n"
              "> > from SPINDLE that don't resolve to anything current - flagged them\n"
              "> > in the ticket, was told it's a known migration artifact. Noting it\n"
              "> > here too in case anyone else asks later.\n"
              "> >\n"
              "> > > On 2547-02-11, T. Reyes (Systems) wrote:\n"
              "> > > SPINDLE hardware powered down for good this afternoon. Anyone\n"
              "> > > who still needs something off it, this was your last chance,\n"
              "> > > I told you that in three separate emails.\n\n"
              "- T.R.")},
    {"from": "d.okonkwo@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-13 10:12",
     "subject": "re: re: re: Thursday lunch order",
     "body": ("Put me down for the same as last time. If they're out of it again\n"
              "just get me whatever, I'm not picky. Are we still doing this at\n"
              "noon or did that move because of the compliance training thing.")},
    {"from": "records@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-02-10 08:15",
     "subject": "New Case Handler Onboarding",
     "body": ("Please provision terminal access for new case handlers.\n"
              "Default temp password: Roster2024!\n\n"
              "Also — a reminder to the floor: the Dependent Status Index still shows\n"
              "leftover reference numbers from the old SPINDLE migration. If a closed\n"
              "case cites a transfer reference that doesn't resolve to anything in the\n"
              "current system, that's expected. It's a decommissioned system, not an\n"
              "active investigation. Please stop opening tickets about it.")},
    {"from": "systems@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-08 07:55",
     "subject": "Scheduled patch window - terminal reboot required overnight",
     "body": ("ROSTER and Webmail will restart automatically between 0100-0200\n"
              "tonight for routine security patches. Save your work before end\n"
              "of day. No action needed if you're not logged in overnight.")},
    {"from": "ops@ocpa.unsc.mil", "to": "sysadmin@ocpa.unsc.mil", "date": "2547-02-05 21:33",
     "subject": "LEDGER sandbox refresh",
     "body": ("Sandbox instance on LEDGER migrated over the weekend.\n"
              "Host: relay.internal\nUser: root\nPass: S3cretDB!2024\n"
              "This is the sandbox copy, not the case-index replica. Don't point\n"
              "anything production-facing at it.")},
    {"from": "ops@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-02-03 13:20",
     "subject": "Office supply requisition - toner and staples backordered",
     "body": ("Standard-cartridge toner and box staples are backordered through\n"
              "at least the 20th. Ration what's left at the supply closet. Do not\n"
              "submit duplicate requisition requests, it doesn't make the vendor\n"
              "ship faster.")},
    {"from": "security@ocpa.unsc.mil", "to": "all-staff@ocpa.unsc.mil", "date": "2547-01-30 09:00",
     "subject": "Building 4 badge access - temporary contractor suspension",
     "body": ("Contractor badge access to Building 4 is suspended pending the\n"
              "annual access review. This does not affect regular staff badges.\n"
              "Contractors needing floor access should be escorted and signed in\n"
              "at the front desk in the interim.")},
    {"from": "t.reyes@ocpa.unsc.mil", "to": "duty.admin@ocpa.unsc.mil", "date": "2547-01-28 11:04",
     "subject": "LEDGER Terminal Access (old creds, deprecated?)",
     "body": ("Whoever's on duty — I still see a stale note floating around for a\n"
              "'svc-relay' account on the LEDGER gateway. I don't think that account\n"
              "exists anymore, or it was never provisioned properly. If someone needs\n"
              "in, use your own duty credentials against the gateway SSH, same as\n"
              "always. Don't go hunting for svc-relay / R3lay!Access9, it's not real.\n"
              "Host: relay.internal, port 22.")},
    {"from": "records@ocpa.unsc.mil", "to": "j.brandt@colonial-admin.mdg", "date": "2547-01-15",
     "subject": "RE: Follow-up - dependent case OCPA-R4-11944",
     "body": ("Case OCPA-R4-11944 is closed and has been for some time. This office\n"
              "has responded to substantially the same inquiry from your predecessor's\n"
              "office on at least two prior occasions. Absent a new filing or a named\n"
              "requesting party with standing, there is nothing further Records can add.\n\n"
              "> On 2547-01-14, J. Brandt (Madrigal Colonial Administration) wrote:\n"
              "> Writing again regarding case OCPA-R4-11944 - this office continues to\n"
              "> receive occasional informal inquiries about this closed case, most\n"
              "> recently last month. We have nothing to add beyond what was already\n"
              "> provided, but wanted OCPA aware the interest hasn't gone away on our\n"
              "> end either.\n\n"
              "Records, OCPA Region 4")},
    {"from": "records@ocpa.unsc.mil", "to": "v.dumont@colonial-admin.eri2", "date": "2547-01-09",
     "subject": "RE: Case status inquiry - OCPA-R4-11902",
     "body": ("Case OCPA-R4-11902 is closed. Per policy, closed dependent cases are\n"
              "not subject to further inter-administration correspondence absent a\n"
              "new filing. Please direct any future inquiries to the standard public\n"
              "records request process.\n\n"
              "> On 2547-01-08, V. Dumont (Eridanus II Colonial Administration) wrote:\n"
              "> Following up on behalf of a constituent regarding case\n"
              "> OCPA-R4-11902. Colonial Administration has received periodic\n"
              "> inquiries about this closed case over the years. Standard closure\n"
              "> documentation was previously provided; this office has no further\n"
              "> information to add and no standing to request additional detail\n"
              "> from OCPA directly. Please advise if there is a more appropriate\n"
              "> contact for follow-up questions of this nature going forward.\n\n"
              "Records, OCPA Region 4")},
]

UI = {
    "page_title": "OCPA Webmail",
    "banner": "OCPA REGION 4 INTERNAL MAIL -- DO NOT FORWARD OFF NETWORK",
    "brand": "OCPA Mail",
    "folder_inbox": "Inbox",
    "folder_sent": "Sent",
    "folder_drafts": "Drafts",
    "folder_trash": "Trash",
    "login_title": "OCPA Region 4 :: Webmail",
    "placeholder_user": "Username",
    "placeholder_pass": "Password",
    "login_button": "Login",
    "inbox_title": "Inbox",
    "invalid_creds": "Invalid credentials for user:",
    "back_link": "Back",
}
