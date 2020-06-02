import rdflib
from rdflib.resource import Resource

class SDGIO():

    # Parse the SDGIO Ontology
    def __init__(self):
        self.sdgio_graph = rdflib.Graph().parse("http://purl.unep.org/sdg/sdgio.owl", format='xml')

    # Return parsed sdgio graph
    def getGraph(self):
        return self.sdgio_graph

    # Return a list of goals sorted by uri
    def getGoals(self):

        goal_results = self.sdgio_graph.query(
            """PREFIX sdg: <http://purl.unep.org/sdg/>
               PREFIX oboInOwl: <http://www.geneontology.org/formats/oboInOwl#>
               SELECT ?uri ?goal_long ?goal_short ?label
               WHERE {
                   ?uri rdf:type <http://purl.unep.org/sdg/SDGIO_00000000>.
                   ?uri oboInOwl:hasExactSynonym ?goal_long.
                   ?uri oboInOwl:hasExactSynonym ?goal_short.
                   ?uri rdfs:label ?label.
                   FILTER(?goal_long != ?goal_short).
                   FILTER(?goal_long > ?goal_short).
               }""")

        goals = list(map(lambda g: {"uri": ("%s" % g[0]), "goal_long": ("%s" % g[1]), "goal_short": ("%s" % g[2]), "description": ("%s" % g[3])}, goal_results))

        return sorted(goals, key=lambda g: g["uri"])

    # Return a list of targets sorted by uri
    def getTargets(self):

        target_results = self.sdgio_graph.query(
            """PREFIX sdg: <http://purl.unep.org/sdg/>
               SELECT ?uri ?target ?label
               WHERE {
                   ?uri rdf:type <http://purl.unep.org/sdg/SDGIO_00000001>.
                   ?uri sdg:SDGIO_00000074 ?target.
                   ?uri rdfs:label ?label.
               }""")

        targets = list(map(lambda t: {"uri": ("%s" % t[0]), "target": ("%s" % t[1]), "description": ("%s" % t[2])}, target_results))

        return sorted(targets, key=lambda t: t["uri"])

    # Return a list of goals sorted by uri
    def getIndicators(self):

        indicator_results = self.sdgio_graph.query(
            """PREFIX sdg: <http://purl.unep.org/sdg/>
               SELECT ?uri ?indicator ?label
               WHERE {
                   ?uri rdfs:subClassOf <http://purl.unep.org/sdg/SDGIO_00000003>.
                   ?uri sdg:SDGIO_00000242 ?indicator.
                   ?uri rdfs:label ?label.
               }""")

        indicators = list(map(lambda i: {"uri": ("%s" % i[0]), "indicator": ("%s" % i[1]), "description": ("%s" % i[2])}, indicator_results))

        return sorted(indicators, key=lambda i: i["uri"])

if __name__ == "__main__":

    sdgio = SDGIO()

    goals = sdgio.getGoals()
    targets = sdgio.getTargets()
    indicators = sdgio.getIndicators()

    print("Sample Goal:")
    print(goals[0])
    print()

    print("Sample Target:")
    print(targets[0])
    print()

    print("Sample Goal:")
    print(indicators[0])
    print()

