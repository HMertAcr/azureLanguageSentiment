import graphviz

# Create a new graph
graph = graphviz.Digraph()

# Define the components
components = [
    'Google Form',
    'Google Sheets',
    'Google Service Account',
    'Python Script',
    'Azure Cognitive Service',
    'Power BI'
]

# Add components to the graph
for component in components:
    graph.node(component)

# Define the relationships between components
relationships = [
    ('Google Form', 'Google Sheets'),
    ('Google Service Account', 'Google Sheets'),
    ('Google Service Account', 'Python Script'),
    ('Azure Cognitive Service', 'Python Script'),
    ('Python Script', 'Power BI'),
]

# Add relationships to the graph
for relationship in relationships:
    graph.edge(*relationship)

# Render the graph to a file
graph.format = 'png'
graph.render('solution_infrastructure_diagram', view=True)
