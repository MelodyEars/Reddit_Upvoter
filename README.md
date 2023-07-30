# Reddit_Upvoter
Was used by a binary file for a large number of servers on windows 10 with a chrome-based browser. <br>
Connecting to the only database purchased on Digital Ocean.<br>
Use reddit accounts for put on UPvote <br>
This project has 10 projects.<br>

1. `new_run_TGBOT.py` <br>
  Run TelegramBot for your actions on Reddit.
  Сurrently the newest version (will not be supported further).<br>
  All files exists in `NW_Upvoter/`<br>
  Project works with remote DB(set up via Digital Ocean(SSL sertficate is in `work_fs/sertificate_db`)).<br>
  
2. `run_CHECK_ban.py`
   Parser that checks for permanent and shadow ban reddit accounts.<br>
   (in `SETTINGS.py` change `mine_project` on `True`(server) `False`(local) if db server or local)

3. `run_AUTH_cookie.py`
   Takes data from the end of files `proxies.txt` and `accounts.txt`.<br>
   Authorization on reddit. Makes a cookie and writes the path to the database.

4. `run_TGBOT.py`
   If you are going to use this project on the local machine, change `mine_project` on `True`(server) `False`(local) in the SETTINGS.py
   


  
