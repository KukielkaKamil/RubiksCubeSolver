-- SQLite
SELECT DISTINCT edge_state, MIN(depth)
FROM pruning_table GROUP BY edge_state; 