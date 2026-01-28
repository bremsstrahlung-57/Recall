# Recall

Recall is a personal knowledge retrieval tool.
Users can upload files, text, and bookmarks and search them later using semantic search instead of exact filenames or keywords, or going to different websites or digging in folders.

## Current Version - 0.3.1
Now we can get both whole document and a AI response or summary

```
❯ uv run app/debug/vector_roundtrip.py

Enter Query: souls like set in japan
Enter Limit: 5

Query: souls like set in japan
API Available
1.Gemini
2.LLama(Groq)
Choose provider: 2
Sekiro is set in Sengoku-era Japan.
```
```
❯ uv run app/debug/vector_roundtrip.py

Enter Query: how do i make Grilled Shrimp Tacos
Enter Limit: 5

Query: how do i make Grilled Shrimp Tacos
API Available
1.Gemini
2.LLama(Groq)
Choose provider: 2
To make Grilled Shrimp Tacos, heat an outdoor grill to high, whisk lime juice, oil, chipotle powder, salt, and cumin together, add the shrimp and toss to combine, then skewer each shrimp through the tail and head ends. Place the skewers on the grill, cook until grill marks appear, flip and cook until the shrimp are just firm. Remove the shrimp from the skewers, coarsely chop, and serve with tortillas and salsa. Also, make Avocado-Corn Salsa by removing corn kernels from cobs, combining with scallions, tomatoes, lime juice, cilantro, serrano, and salt, then folding in avocado pieces.
```
```
❯ uv run app/debug/vector_roundtrip.py

Enter Query: something about pompeii
Enter Limit: 5

Query: something about pompeii
API Available
1.Gemini
2.LLama(Groq)
Choose provider: 1
In Pompeii, waste was collected and sorted for recycling, indicating a different priority regarding trash management compared to modern practices. The residents had a much closer relationship with their garbage, which often littered the streets and was piled in and on tombs. This was not due to a lack of infrastructure, but because their urban management systems were organized around different principles.

Nineteenth-century archaeologists initially interpreted these trash mounds as a sign that the city fell into disrepair after the 62 A.D. earthquake. However, researcher Emmerson challenged this view, presenting evidence that the city was in a "period of rejuvenation" by 79 A.D. Attitudes towards sanitation, death, and cleanliness in Pompeii were culturally defined and different from what 19th-century archaeologists assumed. For example, tombs were built in high-traffic areas to ensure the deceased would be remembered, which meant they were directly in the path of the city's inhabitants leaving litter. Excavations in Pompeii have uncovered rooms containing cesspits filled with animal bones and olive pits, located alongside cisterns used for storing drinking and washing water. Waste sites developed in busy suburban areas, serving as staging grounds for recycling and reuse processes.
```
