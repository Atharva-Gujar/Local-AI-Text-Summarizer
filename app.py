import gradio as gr
import requests
import PyPDF2
import docx
import os
from typing import Optional

class TextSummarizer:
    """Text summarizer with API key support"""
    
    def __init__(self, api_key: str = ""):
        # Using Hugging Face Inference API
        self.api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        
    def set_api_key(self, api_key: str):
        """Update API key"""
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        
    def summarize_text(self, text: str, max_length: int = 150, min_length: int = 50, api_key: str = "") -> dict:
        """
        Summarize the given text using Hugging Face API
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of summary
            min_length: Minimum length of summary
            api_key: Optional Hugging Face API key
            
        Returns:
            Dictionary with summary or error message
        """
        if not text or len(text.strip()) < 50:
            return {"error": "Text is too short to summarize. Please provide at least 50 characters."}
        
        # Update headers if API key provided
        headers = {"Authorization": f"Bearer {api_key}"} if api_key else self.headers
        
        if not api_key and not self.api_key:
            return {
                "error": "API key required. Get a free key at https://huggingface.co/settings/tokens"
            }
        
        payload = {
            "inputs": text,
            "parameters": {
                "max_length": max_length,
                "min_length": min_length,
                "do_sample": False
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    summary = result[0].get('summary_text', '')
                    return {
                        "summary": summary,
                        "original_length": len(text),
                        "summary_length": len(summary),
                        "compression_ratio": f"{(len(summary) / len(text) * 100):.1f}%"
                    }
                else:
                    return {"error": "Unexpected response format from API"}
            elif response.status_code == 401:
                return {"error": "Invalid API key. Get a free key at: https://huggingface.co/settings/tokens"}
            elif response.status_code == 503:
                return {"error": "Model is loading. Please wait a moment and try again."}
            else:
                return {"error": f"API Error: {response.status_code} - {response.text[:200]}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Request timed out. Please try again."}
        except Exception as e:
            return {"error": f"Error: {str(e)}"}

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    def extract_text_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise Exception(f"Error reading TXT: {str(e)}")


# Initialize summarizer
summarizer = TextSummarizer()


def process_input(text_input: str, file_input, max_len: int, min_len: int, api_key: str):
    """Process text or file input and return summary"""
    
    # Determine input source
    input_text = ""
    
    if file_input is not None:
        # File uploaded
        file_path = file_input.name
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                input_text = summarizer.extract_text_from_pdf(file_path)
            elif file_ext == '.docx':
                input_text = summarizer.extract_text_from_docx(file_path)
            elif file_ext == '.txt':
                input_text = summarizer.extract_text_from_txt(file_path)
            else:
                return "❌ Unsupported file format. Please upload PDF, DOCX, or TXT files.", ""
        except Exception as e:
            return f"❌ Error processing file: {str(e)}", ""
    
    elif text_input and text_input.strip():
        # Text input provided
        input_text = text_input
    
    else:
        return "⚠️ Please provide text or upload a file to summarize.", ""
    
    # Truncate if text is too long (model limit ~1024 tokens)
    if len(input_text) > 4000:
        input_text = input_text[:4000]
        warning = "⚠️ Text was truncated to 4000 characters due to model limitations.\n\n"
    else:
        warning = ""
    
    # Get summary
    result = summarizer.summarize_text(input_text, max_length=max_len, min_length=min_len, api_key=api_key)
    
    if "error" in result:
        return f"❌ {result['error']}", ""
    
    # Format output
    summary_output = f"""
✨ **Summary Generated Successfully!**

{result['summary']}

---
📊 **Statistics:**
- Original Length: {result['original_length']:,} characters
- Summary Length: {result['summary_length']:,} characters
- Compression Ratio: {result['compression_ratio']}
    """
    
    return warning + summary_output, input_text[:500] + "..." if len(input_text) > 500 else input_text


# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft(), title="AI Text Summarizer") as demo:
    
    gr.Markdown("""
    # 🤖 AI Text Summarizer
    ### Powered by Hugging Face's BART Model
    
    Summarize long texts, documents, or articles instantly using state-of-the-art AI.
    Supports text input, PDF, DOCX, and TXT files.
    
    **⚠️ API Key Required:** Get your free API key at [Hugging Face](https://huggingface.co/settings/tokens)
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🔑 API Key")
            
            api_key_input = gr.Textbox(
                label="Hugging Face API Key",
                placeholder="hf_...",
                type="password",
                info="Get your free key at https://huggingface.co/settings/tokens"
            )
            
            gr.Markdown("### 📝 Input")
            
            text_input = gr.Textbox(
                label="Paste your text here",
                placeholder="Enter the text you want to summarize...",
                lines=10,
                max_lines=15
            )
            
            file_input = gr.File(
                label="Or upload a document",
                file_types=[".pdf", ".docx", ".txt"]
            )
            
            with gr.Row():
                max_length = gr.Slider(
                    minimum=50,
                    maximum=500,
                    value=150,
                    step=10,
                    label="Maximum Summary Length"
                )
                
                min_length = gr.Slider(
                    minimum=10,
                    maximum=100,
                    value=50,
                    step=10,
                    label="Minimum Summary Length"
                )
            
            summarize_btn = gr.Button("✨ Generate Summary", variant="primary", size="lg")
            
            gr.Markdown("""
            ---
            **Tips:**
            - Get a free API key at [Hugging Face](https://huggingface.co/settings/tokens)
            - For best results, provide texts with at least 200 characters
            - The model works best with articles, reports, and structured text
            - Files are limited to ~4000 characters due to API constraints
            """)
        
        with gr.Column(scale=1):
            gr.Markdown("### 📄 Output")
            
            summary_output = gr.Markdown(
                label="Summary",
                value="Your summary will appear here..."
            )
            
            with gr.Accordion("📋 View Original Text Preview", open=False):
                original_preview = gr.Textbox(
                    label="First 500 characters of input",
                    lines=5,
                    interactive=False
                )
    
    # Examples
    gr.Examples(
        examples=[
            ["Artificial intelligence (AI) is intelligence demonstrated by machines, in contrast to the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of intelligent agents: any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term artificial intelligence is often used to describe machines that mimic cognitive functions that humans associate with the human mind, such as learning and problem solving."],
            ["Climate change refers to long-term shifts in temperatures and weather patterns. These shifts may be natural, such as through variations in the solar cycle. But since the 1800s, human activities have been the main driver of climate change, primarily due to burning fossil fuels like coal, oil and gas. Burning fossil fuels generates greenhouse gas emissions that act like a blanket wrapped around the Earth, trapping the sun's heat and raising temperatures."]
        ],
        inputs=[text_input],
        label="Try these examples:"
    )
    
    # Connect the button
    summarize_btn.click(
        fn=process_input,
        inputs=[text_input, file_input, max_length, min_length, api_key_input],
        outputs=[summary_output, original_preview]
    )
    
    gr.Markdown("""
    ---
    <div style='text-align: center; color: #666;'>
        <p>🔑 <strong>How to get a free API key:</strong></p>
        <ol style='text-align: left; display: inline-block;'>
            <li>Go to <a href="https://huggingface.co/settings/tokens" target="_blank">https://huggingface.co/settings/tokens</a></li>
            <li>Sign up or log in (it's free!)</li>
            <li>Click "New token"</li>
            <li>Give it a name and select "Read" role</li>
            <li>Copy the token and paste it above</li>
        </ol>
        <p>⚠️ Your API key is only used for this session and is not stored</p>
    </div>
    """)


if __name__ == "__main__":
    print("🚀 Starting AI Text Summarizer...")
    print("📱 Open the URL shown below in your browser")
    print("🔑 You'll need a Hugging Face API key (free)")
    print("   Get one at: https://huggingface.co/settings/tokens")
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )
