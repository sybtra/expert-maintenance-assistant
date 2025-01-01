import gradio as gr
from ingest import ingest_documents
from chat import chat_with_collection

def create_gradio_app():
    with gr.Blocks() as demo:
        gr.Markdown("# Assistant ChatBot")
        
        # Section d'ingestion
        with gr.Tab("Ingestion de Documents"):
            collection_name = gr.Textbox(label="Nom de la collection", autofocus=True)
            files = gr.File(
                label="Fichiers à ingérer", 
                file_count="multiple",
                type="binary"
            )
            ingest_button = gr.Button("Ingérer")
            ingest_output = gr.Textbox(label="Résultat d'ingestion")
            
            ingest_button.click(
                ingest_documents,
                inputs=[collection_name, files],
                outputs=[ingest_output]
            )
        
        # Section de chat avec ChatInterface
        with gr.Tab("Chat"):
            collection_name_chat = gr.Textbox(label="Nom de la collection", autofocus=True)
            chatbot = gr.ChatInterface(
                title="Chat avec les documents",
                description="Posez vos questions sur les documents ingérés",
                examples=[["Dis-moi en une phrase ce que contiennent les documents ?", "Document de maintenance"]],
                type="messages",
                additional_inputs=[collection_name_chat],
                fn=chat_with_collection,
                autoscroll=True,
                submit_btn="Send Prompt",
                stop_btn="Stop Generation",
                show_progress="minimal"
            )

    demo.launch()

if __name__ == "__main__":
    create_gradio_app()