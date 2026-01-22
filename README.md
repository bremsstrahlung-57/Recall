# Recall

Recall is a personal knowledge retrieval tool.
Users can upload files, text, and bookmarks and search them later using semantic search instead of exact filenames or keywords, or going to different websites or digging in folders.

## Current Version - 0.2.0
`❯ uv run app/debug/vector_roundtrip.py`

`Enter Query: souls like set in japan`

`Enter Limit: 5`

```
Query: souls like set in japan
Doc ID: 37daa4bacd7ef4c2c9779b6c1917a25891cf8ea5eeffe4204c73978f2628be18
Score: 0.4450
Max Score: 0.4759
All Scores: [0.47594297, 0.41399783]
Stats: {'mean': 0.4449704, 'median': 0.4449704, 'mode': 0.4449704}
Source: user
Doc: Sekiro: Shadows Die Twice is an action game built around precision, discipline, and mastery. Unlike ...
Chunk Doc: Sekiro: Shadows Die Twice is an action game built around precision, discipline, and mastery. Unlike ...
Chunk ID: 0
Total Chunks: 4
Created At: 2026-01-22 20:57:49

Doc ID: 561c5e2415586a138733becd1cfd67ab8bbcbcc8e1013fefffadca75968cf8a4
Score: 0.3695
Max Score: 0.4619
All Scores: [0.46190268, 0.33116657, 0.3152845]
Stats: {'mean': 0.36945125, 'median': 0.33116657, 'mode': 0.33116657}
Source: user
Doc: Bloodborne shifts the Souls formula toward aggressive, fast-paced combat. Set in the gothic city of ...
Chunk Doc:  Enemy design reinforces constant pressure, forcing players to stay alert and decisive. Healing is l...
Chunk ID: 1
Total Chunks: 3
Created At: 2026-01-22 20:57:49
```
