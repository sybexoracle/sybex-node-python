from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from src.constants import GRAPHQL_API_URL
from src.resolver.queries import GET_QUESTIONS_QUERY, GET_ANSWERS_QUERY


class GraphQLResolver:
    def __init__(self) -> None:
        self.transport = RequestsHTTPTransport(url=GRAPHQL_API_URL)
        self.client = Client(transport=self.transport)

    def query_questions(self):
        response = self.client.execute(GET_QUESTIONS_QUERY)
        return response.get("questions", [])

    def query_answers(self):
        response = self.client.execute(GET_ANSWERS_QUERY)
        return response.get("answers", [])