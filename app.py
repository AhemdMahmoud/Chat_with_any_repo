import gradio as gr

def chat_with_repo(repo_url, query):
    try:
        # Load documents
        docs = load_github_repo(repo_url)
        if not docs:
            return "❌ Could not load documents from the provided repository URL."

        # Split documents
        split_documents_list = split_documents(docs)
        if not split_documents_list:
             return "❌ Could not split documents. Check if supported file types are present."

        # Create vector store (using a temporary path for demonstration)
        faiss_index_path = "./faiss_index_temp"
        vectorstore = store_in_faiss(split_documents_list, faiss_index_path)

        # Create conversation chain
        chain = load_conversation_chain(vectorstore)

        # Get response from the chain
        response = chain({"question": query})
        answer = response["answer"]

        # Beautify output with Markdown
        formatted_answer = f"### 💡 Answer\n\n{answer}"

        return formatted_answer

    except Exception as e:
        return f"❌ An error occurred:\n\n```\n{str(e)}\n```"

# Gradio interface with Markdown output
iface = gr.Interface(
    fn=chat_with_repo,
    inputs=[
        gr.Textbox(label="GitHub Repository URL"),
        gr.Textbox(label="Your Question")
    ],
    outputs=gr.Markdown(),
    title="🧠 Codebase Chatbot",
    description="Enter a GitHub repository URL and ask questions about its code."
)

iface.launch(debug=True)
