"""English content pack for the CAIRN Records Terminal. Selected at Docker
build time (see Dockerfile ARG LANG) - admin_panel.py never branches on
language."""

RECORDS = [
    (101, "ONI Section III - Disposition Order 2547-014",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "DISPOSITION ORDER 2547-014\n"
     "FROM: Cmdr. I. Petrov, ONI Section III\n"
     "TO: CAIRN Records Custodian\n"
     "DATE: 2547-02-11\n"
     "RE: SPINDLE decommission - records disposition\n\n"
     "Per review of the SPINDLE decommission, all case material predating the\n"
     "2547 migration is reclassified RESTRICTED - DISPOSITION HOLD pending further\n"
     "review. Active dependent cases remain on LEDGER. All acquisition-era\n"
     "material, including subject transfer records and program correspondence,\n"
     "is to be retained on this node pending full transfer to permanent\n"
     "archival custody, and is not to be referenced in any active OCPA case\n"
     "file in the interim.\n\n"
     "Note for custodian: this is a staging mirror, not the permanent archive.\n"
     "Full decommission of this node was scheduled following transfer\n"
     "completion. Do not treat this system as production infrastructure.\n\n"
     "This order does not authorize destruction of the material. Retention only."),

    (102, "Flash-Clone Substitution Protocol - Medical Annex",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "MEDICAL ANNEX - FLASH-CLONE SUBSTITUTION PROTOCOL\n"
     "REVIEWED BY: Dr. M. Castel, ONI Section III Medical Oversight\n"
     "RE: Candidate acquisition - case closure procedure\n\n"
     "Standard procedure for candidate acquisition required a substitute\n"
     "biological record to close the originating case file without raising\n"
     "family or colonial-administration inquiry. Substitutes were full-body\n"
     "flash clones - accelerated-growth constructs with a known, inherent\n"
     "limit on viability, not a purpose-built defect. Left to run their\n"
     "course, they fail within a short window in a way that reads as an\n"
     "ordinary natural/medical death to any attending physician. That\n"
     "existing limitation was the point: the local physician closing each\n"
     "case would have no reason to suspect anything and no need to be read\n"
     "into the program.\n\n"
     "This office's role was limited to program-side medical oversight:\n"
     "reviewing each case file after local closure to confirm the substitution\n"
     "held up under normal scrutiny, and maintaining the clone specification\n"
     "records. This office did not attend any closure in person.\n\n"
     "Cross-reference note (added later, different hand): I reviewed and\n"
     "signed off on three of these case files after the fact, confirming\n"
     "each closure was clean. I did that before I understood what I was\n"
     "actually confirming. I am not proud of that, and I am not going to\n"
     "pretend I didn't have a choice.\n"
     "- M.C."),

    (103, "Correspondence Fragment - C. Halsey to Section III, 2517",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "CORRESPONDENCE FRAGMENT (RECOVERED, PARTIAL)\n"
     "FROM: Dr. C. Halsey\n"
     "TO: ONI Section III\n"
     "DATE: 2517 (exact date not recovered)\n\n"
     "...you asked me whether I could live with it. I don't think that is the\n"
     "right question. The right question is whether the colonies survive long\n"
     "enough to ask me anything at all. I have run the projections three more\n"
     "times since we spoke. They do not improve.\n\n"
     "I will not pretend this is anything other than what it is. I am asking\n"
     "you to let me take children out of their lives without their consent or\n"
     "their parents'. I am telling you I believe it is necessary. Both of those\n"
     "things are true at once, and I don't expect either of us to feel settled\n"
     "about it.\n\n"
     "Proceed with the candidate list as submitted."),

    (104, "Internal Memo - CPO M. Kade to Records, 2540",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "INTERNAL MEMO\n"
     "FROM: CPO M. Kade, UNSC Training Command (Reach)\n"
     "TO: Records\n"
     "DATE: 2540\n\n"
     "To whoever eventually reads this file and not just stamps it -\n\n"
     "I was one of Chief Mendez's training staff on Reach, not the one running\n"
     "the program - that was his, from the first candidate to the last. My own\n"
     "assignment was a small group off the SPINDLE list, not the whole cohort.\n"
     "The ones I had, I trained personally, start to finish. I watched some\n"
     "of them not survive augmentation. I watched the rest of them become\n"
     "something this species needed a great deal more than it ever admitted to\n"
     "needing.\n\n"
     "I don't know if that makes it right. I know I'd do it again, and I know\n"
     "that scares me more than anything the Covenant has thrown at us. Keep the\n"
     "file. Don't let it disappear. Somebody should be able to ask the question\n"
     "later, even if we can't answer it now.\n\n"
     "One more thing, since this is going in the sealed file and not a report\n"
     "anyone reviews. I still think about 07-B. Skopje kid, angriest six-year-old\n"
     "I ever met, best reflexes in the whole cohort by the second year. The\n"
     "official log on that one reads as a medical discharge. That is not what\n"
     "I watched happen in the augmentation bay, and I was standing right there.\n"
     "I did not write it up that way. I don't know who did, or why.\n\n"
     "- M. Kade, CPO"),

    (105, "Medical Certification Log Fragment - Case Closures 2517",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "MEDICAL CERTIFICATION LOG (FRAGMENT)\n"
     "RE: Death certificates issued under substitution protocol, 2517 batch\n\n"
     "  CASE REF        LOCAL CERTIFYING PHYSICIAN      ONI FILE REVIEW\n"
     "  OCPA-R4-11902    Dr. H. Idowu (Eridanus II)       M. Castel\n"
     "  OCPA-R4-11944    Dr. A. Petrides (Madrigal)       M. Castel\n"
     "  OCPA-R4-11887    Dr. T. Marlow (Skopje)           M. Castel\n"
     "  OCPA-R4-10733    Dr. H. Idowu (Eridanus II)       R. Achebe\n\n"
     "Local certifying physicians had no access to acquisition-program\n"
     "material and certified each closure as an ordinary case, per design.\n"
     "Log fragment only - remaining entries lost in the SPINDLE migration."),

    (106, "Cryogenic Recovery Transfer Authorization - Subject 07-B",
     "//CLASSIFIED - ONI SECTION III - EYES ONLY//\n"
     "TRANSFER AUTHORIZATION (MEDICAL)\n"
     "RE: Post-augmentation recovery transfer, subject 07-B\n"
     "DATE: 2525 (augmentation cycle)\n\n"
     "Subject 07-B authorized for transfer to long-term cryogenic recovery\n"
     "pending reassessment. Augmentation bay report on file lists subject as\n"
     "clinically non-viable at time of transfer; recovery team elected to\n"
     "proceed with suspension rather than log a field determination.\n\n"
     "This authorization does not supersede or amend any existing case\n"
     "closure. It is filed separately per standing medical procedure for\n"
     "suspension-pending cases.\n\n"
     "No follow-up reassessment record has been located in this archive."),
]

UI = {
    "login_title": "CAIRN Records Terminal",
    "classbar": "CLASSIFIED // ONI SECTION III // EYES ONLY",
    "login_seal_h1": "CAIRN RECORDS TERMINAL",
    "login_warning": "DISPOSITION HOLD ACCESS ONLY -- UNAUTHORIZED ACCESS IS A VIOLATION OF UNSC MILITARY CODE ART. 12",
    "placeholder_user": "Username",
    "placeholder_pass": "Password",
    "access_button": "ACCESS",
    "dashboard_title": "CAIRN Dashboard",
    "dashboard_h1": "DISPOSITION HOLD -- RECORD INDEX",
    "terminal_status": "Terminal Status",
    "status_hostname": "Hostname:",
    "status_user": "User:",
    "status_role": "Role: staging mirror (post-SPINDLE migration, transfer pending)",
    "status_decommission": "Decommission: scheduled, not completed",
    "back_to_index": "&laquo; back to index",
    "record_not_found": "RECORD NOT FOUND / OUT OF SCOPE.",
    "access_denied": "ACCESS DENIED",
    "back_link": "Back",
    "photo_on_file": "personnel photo on file",
}
