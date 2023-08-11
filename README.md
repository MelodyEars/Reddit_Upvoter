# Reddit_Upvoter
A binary file was utilized for a substantial number of servers on Windows with a Chrome-based browser.<br>
Each server was connected to a unified database obtained from Digital Ocean.<br>
<br>
This is a project that encompasses numerous applications (including both synchronous and asynchronous versions).<br>
The main objective was to place upvotes on Reddit posts (using Selenium). <br>
The client interface was developed through a Telegram bot (aiogram),<br>
the servers of which were hosted on Windows for launching browsers, with an adjacent PostgreSQL database (ClusterDB) from DigitalOcean.<br>
For database interaction, I utilized the Peewee and TortoiseORM (with an SSL certificate).<br>
AIOHTTP/Requests were used to verify proxies (I determined the proxy server's location and adjusted the Selenium browser accordingly).<br>
I employed concurrent.futures to merge asynchronous code (Telegram bot, database, parsing) with synchronous code (browser control).

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
   


  
