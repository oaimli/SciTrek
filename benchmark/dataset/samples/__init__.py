# our final data samples for SciTrek
# download from https://drive.google.com/file/d/15JsYlFMbmo0e2du4XZysWvKVF_8lNrGi/view?usp=drive_link

# keys in each data sample: 'articles', 'sample_level', 'sql_type', 'focus', 'sql', 'template', 'question', 'answer', 'label'
# 'articles': article ids that comprise the context
# 'sample_level': the level of the sample and how we concatenate the articles, e.g., multi_ran_64, multi_dfs_64, and multi_bfs_64 (ran: random, bfs: breadth first traversal, dfs: depth first traversal)
# 'sql_type': corresponding reasoning skill, e.g., multi_graph_filtering (relational filtering)
# 'focus': the question focus, e.g, reference_count
# 'sql': the SQL query
# 'template': the original template of the SQL query
# 'question': the question generated from the SQL query
# 'answer': the answer from the SQL query execution
# 'label': the label of the sample, e.g., training, dev, test

# sql_type interpretation
# "multi_graph_filtering" -> "Graph Filtering"
# "multi_ran_aggregating" -> "Aggregating"
# "multi_ran_filtering_foa" -> "Filtering+Aggregating"
# "multi_ran_filtering_foo" -> "Filtering+Sorting"
# "multi_ran_filtering_ofo" -> "Filtering"
# "multi_ran_organizing" -> "Sorting"