# Assessment Schedule Reminder

This script serves to send emails to module leaders reminding them about the assessment tasks taking place in the week during which the script is run.

It will advise module leaders of which assessments need to be handed out, which should be handed in, and for which assessments feedback is due to be returned to the students.


## Inputs
The script requires a number of file inputs.

One .csv file containing a list of modules and module leaders
One .csv file containing a list of module leaders and their email addresses
One .xlsx file containing a list of assessments and their details

Samples of all input files can be found in `sample_input/`

### Assessment details spreadsheet
The spreadsheet containing assessment details must contain columns [Module,Coursework,Percentage,Out,In,Feedback]. "Out", "In", "Feedback" are all expected to be the relevant dates where coursework is handed out, collected in and feedback returned for. These can be actual dates, or just the start of the week in which the activity occurs.

## Config

All configuration options are specified in the file `config.py`, see comments in that file for details.

## TODO

* Add comments to `config.py`!
* Input should be Semester weeks, not dates (makes it easier to generate from module review data, which can then be checked by year tutors/module leaders/A&F lead)
    * This needs a weeks -> dates conversion sheet as well
* Replace string messages with HTML templating (jinja)
    * Include mailto links for notification of problems/issues
* Generate assessment timetables from this data - much easier than creating spreadsheets
