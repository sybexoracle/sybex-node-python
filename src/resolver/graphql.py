from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from src.constants import GRAPHQL_API_URL
from src.resolver.queries import GET_QUESTIONS_QUERY, GET_ANSWERS_BY_ID


class GraphQLResolver:
    def __init__(self) -> None:
        self.transport = RequestsHTTPTransport(url=GRAPHQL_API_URL)
        self.client = Client(transport=self.transport)

    def query_questions(self):
        response = self.client.execute(GET_QUESTIONS_QUERY)
        return response.get("questionAskeds", [])

    def query_answers(self, questionId: str):
        GET_ANSWERS_BY_ID.variable_values = {"questionId": questionId}
        response = self.client.execute(GET_ANSWERS_BY_ID)
        return response.get("answerProvideds", [])
