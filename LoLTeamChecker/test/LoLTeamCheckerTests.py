"""Script to test LoLTeamCheckers' model and controller."""
## [e] = existing (i.e. real summoner, and champ they have ranked
## stats with. [n] = nonexisting


# 1. Tests for successful "Go" command

# 1.1 Enter a [e]summoner, [e]champ. Press "Go".

# 1.2 Enter a [n]summoner. Press "Go".

# 1.3 Enter a [e]summoner, [n]champ. Press "Go".


# 2. Tests for successful data retention

# 2.1 Enter a [e]summoner, [e]champ, press "Go". Change to another
# [e]champ. Press "Go".

# 2.2 Change that row to [e/n]summoner, press "Go". Change back to
# initial [e]summoner, [e]champ. Press "Go". Check that no RiotAPI
# calls are made; data should be retrieved from the model.


# 3. Tests for "Get All Indiv Stats"

# 3.1 Enter all [e]summoners, and all [e]champs

# 3.2 Change a [e]summoner, press "Go".

# 3.3 Change a [e]summoner, press "Get All Indiv Stats"

# 3.4 Change a [e]champ, press "Go".

# 3.5 Change a [e]champ, press "Get All Indiv Stats"


# 4. Test for "Get Summary Stats"

# 4.1 
