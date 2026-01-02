# 🤖 AI Text Summarizer

A beautiful, locally-running text summarizer powered by Hugging Face's free AI models.

## ✨ Features

- 📝 **Text Input**: Paste any text directly
- 📄 **File Upload**: Support for PDF, DOCX, and TXT files
- 🎨 **Beautiful UI**: Clean, modern interface built with Gradio
- 🆓 **Free API**: Uses Hugging Face's free inference API (no API key needed)
- 🏠 **Runs Locally**: Everything runs on your machine
- 📊 **Statistics**: View compression ratio and text lengths

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /Users/avi/Desktop/AI/summarizer
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Open in Browser

The app will automatically open at: `http://127.0.0.1:7860`

## 📖 How to Use

1. **Text Input**: 
   - Paste your text in the text box, OR
   - Upload a PDF, DOCX, or TXT file

2. **Adjust Settings** (optional):
   - Set maximum summary length (50-500 words)
   - Set minimum summary length (10-100 words)

3. **Generate Summary**:
   - Click "✨ Generate Summary"
   - View your summary with statistics

## 🎯 Use Cases

- Summarize research papers and articles
- Condense long emails or reports
- Create executive summaries
- Extract key points from documents
- Quick document reviews

## 🛠️ Technical Details

- **Model**: Facebook's BART (bart-large-cnn)
- **API**: Hugging Face Inference API (free tier)
- **Framework**: Gradio for UI
- **Supported Files**: PDF, DOCX, TXT

## ⚠️ Limitations

- Free API has rate limits (if you hit them, wait a moment)
- Text is truncated to ~4000 characters due to model constraints
- Model may take a few seconds to load on first use
- Best results with well-structured text (articles, reports)

## 🔧 Troubleshooting

### Model is Loading Error
The model needs to warm up on first use. Wait 10-20 seconds and try again.

### Rate Limit Error
The free API has limits. Wait a minute or two before trying again.

### File Upload Issues
Make sure your file is:
- PDF, DOCX, or TXT format
- Contains readable text (not scanned images)
- Under a few MB in size

## 🎨 Customization

You can modify `app.py` to:
- Change the AI model (see Hugging Face model hub)
- Adjust the UI theme
- Add more file format support
- Change max character limits

## 📝 Example

**Original Text** (300 words) ➡️ **Summary** (50-150 words)

The summarizer intelligently extracts the most important information while maintaining coherence.

## 🙏 Credits

- Built with [Gradio](https://gradio.app/)
- Powered by [Hugging Face](https://huggingface.co/)
- Uses Facebook's BART model

---

**Enjoy summarizing! 🎉**
