DELIMITER //

DROP PROCEDURE IF EXISTS GetMostOverlap//
CREATE PROCEDURE GetMostOverlap(
IN id VARCHAR(40)
)
BEGIN
PREPARE statement FROM "SELECT read2_id FROM Alignments WHERE read1_id = ? ORDER BY similarity DESC LIMIT 1;";
SET @p1 = id;
EXECUTE statement USING @p1;
END;
//

DROP PROCEDURE IF EXISTS GetExactMatch//
CREATE PROCEDURE GetExactMatch(
)
BEGIN
PREPARE statement FROM "SELECT read1_id FROM Alignments WHERE similarity / alignment_length * 100 = 100;";
EXECUTE statement;
END;
//

DROP PROCEDURE IF EXISTS GetOneSNP//
CREATE PROCEDURE GetOneSNP(
)
BEGIN
PREPARE statement FROM "SELECT read1_id FROM Alignments WHERE alignment_length - identity = 1 AND gaps = 0;";
EXECUTE statement;
END;
//

DELIMITER ;
