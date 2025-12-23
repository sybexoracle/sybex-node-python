from src.resolver.graphql import GraphQLResolver
from src.resolver.agentic import AgenticResolver

class Resolver:
    def __init__(self) -> None:
        self.agentic = AgenticResolver()
        self.graph = GraphQLResolver()

    def query_questions(self):
        return self.graph.query_questions()
    
    def query_answers(self, questionId: str):
        return self.graph.query_answers(questionId=questionId)
    
    def try_resolve(self, question: dict) -> None:
        print (question)