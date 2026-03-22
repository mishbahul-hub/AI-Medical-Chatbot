from logger import logger

def query_chain(chain, user_input:str):
    try:
        logger.debug(f"Running query chain for input: {user_input}")
        result = chain.invoke({"query": user_input})
        response ={
            "response" : result["result"],
            "sources" : [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
        }
        logger.debug(f"Chain response: {response}")
        return response
    except Exception as e:
        logger.exception(f"Error running query chain: {e}")
        raise

def clean_response_text(text: str) -> str:
    """
    Clean response text from markdown and formatting characters.
    """
    if not text:
        return text
    
    import re
    
    # Remove markdown bold (**text**)
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Remove markdown italic (*text*)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Remove code blocks (```code```)
    text = text.replace('| ', ' • ')
    text = text.replace('|', ' • ')
    # Remove excessive spaces
    text = re.sub(r'\s{2,}', ' ', text)
    
    return text.strip()