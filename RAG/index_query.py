from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import StuffDocumentsChain, LLMChain
import os

llm_name = "gpt-3.5-turbo"
key = os.environ["OPENAI_API_KEY"]
template = "Summarize and Order this content: {context}"

llm = ChatOpenAI(model_name=llm_name, temperature=0, openai_api_key=key)
prompt = PromptTemplate.from_template(template)
llm_chain = LLMChain(llm=llm, prompt=prompt)
# define embedding
embeddings = OpenAIEmbeddings(openai_api_key=key)
# load vector database
db = FAISS.load_local("RAG/index", embeddings, allow_dangerous_deserialization=True)
# create a stuff documents chain.
sd = StuffDocumentsChain(llm_chain=llm_chain)


# obtain relevant documents from db
def search(query, k, score_threshold):
    # define retriever
    retriever = db.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": k, "score_threshold": score_threshold},
    )
    docs = retriever.get_relevant_documents(query)
    return docs


def get_docs(query, k=4, score_threshold=0.5):
    docs = search(query, k, score_threshold)
    return sd._get_inputs(docs)["context"]  # pylint: disable=protected-access
