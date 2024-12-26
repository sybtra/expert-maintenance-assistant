import gradio as gr
from ingest import ingest_documents
from chat import chat_with_collection

def create_gradio_app():
    with gr.Blocks() as demo:
        gr.Markdown("# Assistant de Gestion de l'Eau Potable")
        
        # Section d'ingestion
        with gr.Tab("Ingestion de Documents"):
            collection_name = gr.Textbox(label="Nom de la collection")
            uid = gr.Textbox(label="Identifiant utilisateur")
            files = gr.File(label="Fichiers à ingérer", file_types=[".txt"], file_count="multiple")
            ingest_button = gr.Button("Ingérer")
            ingest_output = gr.Textbox(label="Résultat d'ingestion")
            ingest_button.click(
                ingest_documents,
                inputs=[collection_name, uid, files],
                outputs=[ingest_output]
            )
        
        # Section de chat
        with gr.Tab("Chat Contextuel"):
            collection_name_chat = gr.Textbox(label="Nom de la collection")
            messages = gr.Textbox(label="Messages (séparés par des retours à la ligne)", lines=5)
            chat_button = gr.Button("Envoyer")
            chat_output = gr.Textbox(label="Réponse")
            chat_button.click(
                chat_with_collection,
                inputs=[collection_name_chat, messages],
                outputs=[chat_output]
            )
    
    demo.launch()

create_gradio_app()