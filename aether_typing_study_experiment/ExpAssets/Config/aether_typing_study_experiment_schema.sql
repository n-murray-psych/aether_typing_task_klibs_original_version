/*

******************************************************************************************
                         NOTES ON HOW TO USE AND MODIFY THIS FILE
******************************************************************************************

This file is used at the beginning of your project to create the SQLite database in which
all recorded experiment data is stored.

By default there are only two tables that KLibs writes data to: the 'participants' table,
which stores demograpic and runtime information, and the 'trials' table, which is where
the data recorded at the end of each trial is logged. You can also create your own tables
in the database to record data for things that might happen more than once a trial
(e.g eye movements) or only once a session (e.g. a questionnaire or quiz), or to log data
for recycled trials that otherwise wouldn't get written to the 'trials' table.


As your project develops, you may change the number of columns, add other tables, or
change the names/datatypes of columns that already exist.

To do this, modify this document as needed, then rebuild the project database by running:

  klibs db-rebuild

while within the root of your project folder.

But be warned: THIS WILL DELETE ALL YOUR CURRENT DATA. The database will be completely 
destroyed and rebuilt. If you wish to keep the data you currently have, run:

  klibs export

while within the root of your project folder. This will export all participant and trial
data in the database to text files found in aether_typing_study_experiment/ExpAssets/Data.


Note that you *really* do not need to be concerned about datatypes when adding columns;
in the end, everything will be a string when the data is exported. The *only* reason you
would use a datatype other than 'text' would be to ensure that the program will throw an
error if, for example, it tries to assign a string to a column you know is always going
to be an integer.

*/

CREATE TABLE participants (
    id integer primary key autoincrement not null,
    userhash text not null,
    gender text not null,
    age integer not null, 
    handedness text not null,
    created text not null
);

CREATE TABLE trials (
    id integer primary key autoincrement not null,
    participant_id integer not null references participants(id),
    block_num integer not null,
    trial_num integer not null, 
    condition text not null, 
    typed_practice_stimuli text not null,
    typed_practice1 text not null, 
    typed_practice2 text not null, 
    typed_practice3 text not null,
    t1_stimuli text not null, 
    typed1 text not null, 
    t2_stimuli text not null,
    typed2 text not null, 
    t3_stimuli text not null,
    typed3 text not null, 
    t4_stimuli text not null,
    typed4 text not null, 
    t5_stimuli text not null,
    typed5 text not null, 
    t6_stimuli text not null,
    typed6 text not null, 
    s_practice1_stimuli text not null, 
    s_practice2_stimuli text not null,
    s_practice3_stimuli text not null,
    s_practice4_stimuli text not null,
    spatial_practice1 text not null, 
    spatial_practice2 text not null, 
    spatial_practice3 text not null, 
    spatial_practice4 text not null, 
    s1_stimuli text not null, 
    s2_stimuli text not null,
    s3_stimuli text not null,
    s4_stimuli text not null,    
    spatial_target1 text not null, 
    spatial_target2 text not null, 
    spatial_target3 text not null, 
    spatial_target4 text not null, 
    s5_stimuli text not null, 
    s6_stimuli text not null,
    s7_stimuli text not null,
    s8_stimuli text not null,   
    spatial_target5 text not null, 
    spatial_target6 text not null, 
    spatial_target7 text not null, 
    spatial_target8 text not null, 
    v_practice1_stimuli text not null, 
    v_practice2_stimuli text not null,
    v_practice3_stimuli text not null,
    v_practice4_stimuli text not null,
    verbal_practice1 text not null, 
    verbal_practice2 text not null, 
    verbal_practice3 text not null, 
    verbal_practice4 text not null, 
    v1_stimuli text not null, 
    v2_stimuli text not null, 
    v3_stimuli text not null, 
    v4_stimuli text not null, 
    verbal_target1 text not null, 
    verbal_target2 text not null, 
    verbal_target3 text not null, 
    verbal_target4 text not null, 
    v5_stimuli text not null, 
    v6_stimuli text not null, 
    v7_stimuli text not null, 
    v8_stimuli text not null, 
    verbal_target5 text not null, 
    verbal_target6 text not null, 
    verbal_target7 text not null, 
    verbal_target8 text not null

);
