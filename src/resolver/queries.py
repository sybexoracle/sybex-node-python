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

GET_ANSWERS_QUERY = gql(
    """
query AnswerProvideds {
    answerProvideds {
        questionId
        resolver
        transactionHash
        id
        blockTimestamp
        blockNumber
        answerData
    }
  }
    """
)

