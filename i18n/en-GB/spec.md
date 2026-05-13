# KeepRight Spec

Release: pre-alpha; Spec version: 0.0.3; Schema version: 0.1.0

## About You

Your contact details are optional. We recommend including some contact info if you’re the responsible party. Anything you add will be visible to anyone who can see this declaration.

**Name**

- Answer type: `text`

**Email**

- Answer type: `email`

**Country**

- Answer type: `select`
- Option source: countries; ISO 3166-1 country list

## The Material

Here is where you describe what you’re making the declaration for as well as you can. There are two basic questions to start:

**Is this digital, physical, or both?**

- Answer type: `radio`
- Options:
  - `digital`: Digital
  - `physical`: Physical
  - `both`: Both

**Are you the copyright holder?**

- Answer type: `radio`
- Options:
  - `yes`: Yes
  - `no`: No
  - `not_sure`: Not sure

### Details

**What should we call this material?**

- Answer type: `text`

**What is it?**

- Answer type: `textarea`

**Does it live online?**

- Answer type: `radio`
- Shown when: condition `material_is_digital_or_both`
- Options:
  - `urls`: Yes, I have a URL or URLs
  - `ids`: Yes, I have some IDs (e.g. DOI)
  - `no`: No
- Follow-ups:
  - URL or URLs (`text`), shown when `m4_1` equals `urls`
  - IDs (`text`), shown when `m4_1` equals `ids`

**Which file formats or file extensions are involved?**

- Answer type: `text`
- Shown when: condition `material_is_digital_or_both`

**What's your relationship to it?**

- Answer type: `checkboxes`
- Options:
  - `made`: I made it
  - `own`: I own it
  - `family`: I'm a family member of the creator
  - `steward`: I'm a designated steward
  - `community`: I'm a community member
  - `let_me_tell_you`: Let me tell you...
- Follow-ups:
  - Tell us more (`textarea`), shown when `m5` contains `let_me_tell_you`

**Who made this, and who owns it now?**

- Answer type: `textarea`

**What's its copyright or licensing status, if you know?**

- Answer type: `radio`
- Options:
  - `all_rights_reserved`: All Rights Reserved
  - `open_license`: Open License (e.g. Creative Commons)
  - `public_domain`: Public Domain
  - `not_sure`: Not sure
  - `complicated`: It's complicated...
- Follow-ups:
  - Tell us more (`textarea`), shown when `m7` equals `complicated`

**Can you add any background on how, why, or when it was made? This will help future stewards understand the material. (optional)**

- Answer type: `textarea`

## Keep Right

Who can keep or see this?

**Who would you like to take care of this?**

- Answer type: `checkboxes`
- Options:
  - `person`: A specific person
  - `institution`: A specific institution
  - `any_archive_or_library`: Any qualified archive or library
  - `any_steward`: Open to any steward
  - `it_depends`: It depends...
- Follow-ups:
  - Name them (`text`), shown when `kr1` contains `person`
  - Name it (`text`), shown when `kr1` contains `institution`
  - Tell us more (`textarea`), shown when `kr1` contains `it_depends`

**And where should it live?**

- Answer type: `text`
- Shown when: condition `material_is_physical_or_both`

**Who should be able to see it, and are there any conditions?**

- Answer type: `radio`
- Options:
  - `anyone`: Anyone
  - `researchers`: Researchers only
  - `family_or_designated_people`: Family or designated people only
  - `no_one_for_now`: No one for now
  - `complicated`: It's complicated...
- Follow-ups:
  - Tell us more (`textarea`), shown when `kr2` equals `complicated`

**Until when? (optional)**

- Answer type: `text`

**What can your caretaker do with it?**

- Answer type: `checkboxes`
- Shown when: condition `copyright_holder_yes_or_unsure`
- Options:
  - `preserve_only`: Preserve only
  - `share_freely`: Share freely
  - `may_sell`: May sell
  - `your_call`: Your call
  - `do_not_care`: Don't care
  - `may_destroy`: May destroy it
  - `it_depends`: It depends...
- Follow-ups:
  - Add your conditions (`text`), shown when `kr3` contains `may_destroy`
  - Tell us more (`textarea`), shown when `kr3` contains `it_depends`

## Copy Right

Who can make or keep copies?

_Shown when: condition `material_is_digital_or_both`_

**Can copies be made?**

- Answer type: `radio`
- Options:
  - `yes_freely`: Yes, freely
  - `yes_but`: Yes, but...
  - `no`: No
  - `do_not_care`: Don't care
- Follow-ups:
  - Tell us more (`textarea`), shown when `cr1` equals `yes_but`

**What must copies preserve?**

- Answer type: `checkboxes`
- Options:
  - `original_file_format`: Original file format
  - `all_metadata`: All metadata
  - `folder_structure`: Folder structure
  - `file_names`: File names
  - `original_quality`: Original quality (no compression)
  - `it_depends`: It depends...
- Follow-ups:
  - Tell us more (`textarea`), shown when `cr2` contains `it_depends`

**Where can copies live?**

- Answer type: `radio`
- Options:
  - `anywhere`: Anywhere
  - `specific_countries`: Only in specific countries
  - `specific_institutions`: Only with specific institutions
  - `distributed_widely`: Distributed as widely as possible for safety
  - `let_me_tell_you`: Let me tell you...
- Follow-ups:
  - List countries (`text`), shown when `cr3` equals `specific_countries`
  - List institutions (`text`), shown when `cr3` equals `specific_institutions`
  - Tell us more (`textarea`), shown when `cr3` equals `let_me_tell_you`

_Shown when: condition `material_is_physical_or_both`_

**Should this be digitised?**

- Answer type: `radio`
- Options:
  - `yes_please`: Yes, please
  - `qualified_institution_only`: Yes, but only by a qualified institution
  - `yes_but`: Yes, but...
  - `no`: No
  - `do_not_mind`: Don't mind
- Follow-ups:
  - Tell us more (`textarea`), shown when `cr4` equals `yes_but`

**What must a digitised version preserve?**

- Answer type: `checkboxes`
- Options:
  - `original_colours`: Original colours
  - `full_resolution`: Full resolution
  - `both_sides`: Both sides
  - `physical_scale`: Physical scale
  - `all_accompanying_materials`: All accompanying materials (e.g. notes, packaging)
  - `let_me_tell_you`: Let me tell you...
- Follow-ups:
  - Tell us more (`textarea`), shown when `cr5` contains `let_me_tell_you`

**Where can digital copies live?**

- Answer type: `radio`
- Options:
  - `anywhere`: Anywhere
  - `specific_countries`: Only in specific countries
  - `specific_institutions`: Only with specific institutions
  - `distributed_widely`: Distributed as widely as possible for safety
  - `it_depends`: It depends...
- Follow-ups:
  - List countries (`text`), shown when `cr6` equals `specific_countries`
  - List institutions (`text`), shown when `cr6` equals `specific_institutions`
  - Tell us more (`textarea`), shown when `cr6` equals `it_depends`

## Machine Right

Can machines use this?

**Can machines analyse or index this material?**

- Answer type: `radio`
- Options:
  - `yes_freely`: Yes, freely
  - `preservation_only`: Yes, for preservation purposes only
  - `yes_but`: Yes, but...
  - `no`: No
- Follow-ups:
  - Tell us more (`textarea`), shown when `mr1` equals `yes_but`

**Can this material be used to train AI?**

- Answer type: `radio`
- Options:
  - `yes`: Yes
  - `non_commercial_only`: Yes, but not for commercial purposes
  - `yes_but`: Yes, but...
  - `no`: No
  - `do_not_mind`: Don't mind
- Follow-ups:
  - Tell us more (`textarea`), shown when `mr2` equals `yes_but`

**If this material is used by an AI, what matters to you?**

- Answer type: `checkboxes`
- Options:
  - `attribution`: Attribution (I want to be credited)
  - `transparency`: Transparency (I want to know how it was used)
  - `copy_of_outputs`: A copy of anything produced using it
  - `nothing_in_particular`: Nothing in particular
  - `complicated`: It's complicated...
- Follow-ups:
  - Tell us more (`textarea`), shown when `mr3` contains `complicated`
