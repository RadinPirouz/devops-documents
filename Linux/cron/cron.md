```txt
 .---------------- minute (0 - 59)
 |  .------------- hour (0 - 23)
 |  |  .---------- day of month (1 - 31)
 |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
 |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
 |  |  |  |  |
 *  *  *  *  * user-name command to be executed
```
Here are some examples to illustrate different cron job schedules:

### Example 1: Run at 12:55 every day
```
55 12 * * * root hi
```
This command runs `hi` as the `root` user every day at 12:55.

### Example 2: Run every minute
```
*/1 * * * * root hi
```
This command runs `hi` as the `root` user every minute.

### Example 3: Run every 2 minutes
```
*/2 * * * * root hi
```
This command runs `hi` as the `root` user every 2 minutes.

### Example 4: Run at specific minutes
``` 
10,20,30 10 * * * root hi
```
This command runs `hi` as the `root` user at 10:10, 10:20, and 10:30.

### Example 5: Run after every reboot
```
@reboot root hi
```
This command runs `hi` as the `root` user after system reboot.
