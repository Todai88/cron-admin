=======
cron-admin
==========

We have a set of tasks, each running at least daily, which are scheduled with a simplified cron. We want to find when each of them will next run.

The scheduler config looks like this:

30 1 /bin/run_me_daily
45 * /bin/run_me_hourly
* * /bin/run_me_every_minute
* 19 /bin/run_me_sixty_times

The first field is the minutes past the hour, the second field is the hour of the day and the third is the command to run. For both cases * means that it should run for all values of that field. In the above example run_me_daily has been set to run at 1:30am every day and run_me_hourly at 45 minutes past the hour every hour. The fields are whitespace separated and each entry is on a separate line.

We want you to write a command line program that when fed this config to stdin and a simulated 'current time' in the format HH:MM as command line argument outputs the soonest time at which each of the commands will fire and whether it is today or tomorrow. When the task should fire at the simulated 'current time' then that is the time you should output, not the next one.

For example given the above examples as input and the simulated 'current time' command-line argument 16:10 the output should be

1:30 tomorrow - /bin/run_me_daily
16:45 today - /bin/run_me_hourly
16:10 today - /bin/run_me_every_minute
19:00 today - /bin/run_me_sixty_times

* Assumptions

1. This script will be part of a production environment, hence the production files (requirements, jenkins etc)
2. While a simple script could have done the same thing I want to show how I would develop in normal practice (robust, simple and clear code)
3. Parsing of cron files / data was separated from other logic for flexibility / extendability
4. Tests were written within a reasonable timescale but are not complete
5. Further error / boundary checking should be added to the tests / code where reqd

* Running

From the top level directory (cron-admin) __main__ is in the nextrun directory:

** Arguments
-t time in HH:MM format [required]
-p path to cron file to parse [optional]
-s cron data string to parse [optional or required if no path is specified]

examples:
python nextrun -t 16:10 -p test/crontab.txt
python nextrun -t 16:10 -s "30 1 /bin/run_me_daily \n 45 * /bin/run_me_hourly \n * * /bin/run_me_every_minute \n * 19 /bin/run_me_sixty_times"


