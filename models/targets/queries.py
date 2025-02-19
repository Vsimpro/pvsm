#
#   Targets
#

create_targets_table = \
"""CREATE TABLE IF NOT EXISTS Targets (

    id   INTEGER   PRIMARY KEY AUTOINCREMENT,
    host TEXT      NOT NULL --

);
"""

insert_into_targets = """
INSERT INTO Targets (
 
    host

) 
VALUES (?);
"""

get_target_by_host = """
SELECT * FROM Targets WHERE host = ?;
"""

get_targets = """
SELECT * FROM Targets;
"""
