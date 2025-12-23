from gql import gql

GET_QUESTIONS_QUERY = gql(
    """
query QuestionAskeds {
  questionAskeds {
    asker
    blockNumber
    blockTimestamp
    id
    questionId
    questionText
    questionType
    timeout
    transactionHash
  }
}
"""
)

GET_ANSWERS_BY_ID = gql(
    """
query GET_ANSWERS($questionId: BigInt!) {
  answerProvideds(where: { questionId: $questionId }) {
    id
    transactionHash
    answerData
  }
}
    """
)
