const { useState, useRef, useEffect } = React;

const MedicalAssistant = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [showUploadModal, setShowUploadModal] = useState(false);
    const [uploadedFiles, setUploadedFiles] = useState([]);
    const [alert, setAlert] = useState(null);
    const messagesEndRef = useRef(null);
    const fileInputRef = useRef(null);

    // API Configuration
    const API_BASE_URL = "http://localhost:8000"; // Change to your API URL
    const ASK_ENDPOINT = "/ask/";
    const UPLOAD_ENDPOINT = "/upload_pdfs/";

    // Clean response text from markdown formatting
    const cleanText = (text) => {
        return text
            // Remove markdown bold (**text**)
            .replace(/\*\*(.*?)\*\*/g, '$1')
            // Remove markdown italic (*text*)
            .replace(/\*(.*?)\*/g, '$1')
            // Remove markdown code (```code```)
            .replace(/```(.*?)```/gs, '$1')
            // Remove extra pipes and formatting
            .replace(/\|\s*/g, ' • ')
            // Remove excessive spaces
            .replace(/\s{2,}/g, ' ')
            .trim();
    };

    // Show alert message
    const showAlert = (message, type = "success") => {
        setAlert({ message, type });
        setTimeout(() => setAlert(null), 4000);
    };

    // Handle question submission
    const handleSubmitQuestion = async (e) => {
        e.preventDefault();

        if (!input.trim()) return;

        // Add user message
        const userMessage = {
            id: Date.now(),
            type: "user",
            content: input,
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput("");
        setLoading(true);

        try {
            // Create FormData for the request
            const formData = new FormData();
            formData.append("question", input);

            const response = await fetch(`${API_BASE_URL}${ASK_ENDPOINT}`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const data = await response.json();

            // Add assistant message
            const assistantMessage = {
                id: Date.now() + 1,
                type: "assistant",
                content: data.response || "No response received",
                sources: data.sources || [],
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, assistantMessage]);
        } catch (error) {
            console.error("Error:", error);
            showAlert(
                `Error: ${error.message || "Failed to get response"}`,
                "error"
            );

            // Add error message
            const errorMessage = {
                id: Date.now() + 1,
                type: "assistant",
                content: `Sorry, there was an error processing your question. ${error.message}`,
                sources: [],
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    // Handle file selection
    const handleFileSelect = (e) => {
        const files = Array.from(e.target.files || []);
        files.forEach((file) => {
            if (file.type === "application/pdf") {
                setUploadedFiles((prev) => [...prev, file]);
            } else {
                showAlert("Only PDF files are supported", "warning");
            }
        });
        // Reset input
        e.target.value = "";
    };

    // Handle upload zone drag over
    const handleDragOver = (e) => {
        e.preventDefault();
        e.currentTarget.classList.add("dragover");
    };

    const handleDragLeave = (e) => {
        e.currentTarget.classList.remove("dragover");
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.currentTarget.classList.remove("dragover");
        const files = Array.from(e.dataTransfer.files || []);
        files.forEach((file) => {
            if (file.type === "application/pdf") {
                setUploadedFiles((prev) => [...prev, file]);
            }
        });
    };

    // Remove uploaded file
    const removeFile = (fileName) => {
        setUploadedFiles((prev) =>
            prev.filter((file) => file.name !== fileName)
        );
    };

    // Upload files
    const handleUploadFiles = async () => {
        if (uploadedFiles.length === 0) {
            showAlert("Please select at least one PDF", "warning");
            return;
        }

        setLoading(true);

        try {
            const formData = new FormData();
            uploadedFiles.forEach((file) => {
                formData.append("files", file);
            });

            const response = await fetch(`${API_BASE_URL}${UPLOAD_ENDPOINT}`, {
                method: "POST",
                body: formData,
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.status}`);
            }

            const data = await response.json();

            showAlert(
                `Successfully uploaded ${uploadedFiles.length} file(s)`,
                "success"
            );

            setUploadedFiles([]);
            setShowUploadModal(false);

            // Add system message about upload
            const systemMessage = {
                id: Date.now(),
                type: "system",
                content: `✓ Uploaded ${uploadedFiles.length} file(s). You can now ask questions about them!`,
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, systemMessage]);
        } catch (error) {
            console.error("Upload error:", error);
            showAlert(
                `Upload failed: ${error.message || "Please try again"}`,
                "error"
            );
        } finally {
            setLoading(false);
        }
    };

    // Quick prompts
    const quickPrompts = [
        "What is diabetes?",
        "How to prevent heart disease?",
        "Explain hypertension symptoms",
        "What causes asthma?",
    ];

    const handleQuickPrompt = (prompt) => {
        setInput(prompt);
    };

    return (
        <div className="medical-chat">
            {/* Sidebar */}
            <aside className="sidebar">
                <div className="sidebar-header">
                    <div className="logo">
                        🏥 <span className="logo-text">MediAI</span>
                    </div>
                    <div className="tagline">Your Medical Assistant</div>
                </div>

                <ul className="sidebar-nav">
                    <li
                        className="nav-item"
                        onClick={() => setMessages([])}
                    >
                        ➕ New Chat
                    </li>
                    <li className="nav-item" onClick={() => setShowUploadModal(true)}>
                        📤 Upload Documents
                    </li>
                    <li className="nav-item">⚙️ Settings</li>
                    <li className="nav-item">ℹ️ About</li>
                </ul>

                <div className="sidebar-footer">
                    <p>Made with ❤️ for medical professionals</p>
                </div>
            </aside>

            {/* Main Chat Area */}
            <div className="chat-container">
                {/* Alert Messages */}
                {alert && (
                    <div className="input-area" style={{ paddingBottom: 0 }}>
                        <div className={`alert alert-${alert.type}`}>
                            {alert.message}
                        </div>
                    </div>
                )}

                {/* Messages Area */}
                <div className="messages-area">
                    {messages.length === 0 ? (
                        <div className="empty-state">
                            <div className="empty-icon">🏥</div>
                            <h1 className="empty-title">
                                Hi there, <span style={{ color: "var(--secondary)" }}>User</span>
                            </h1>
                            <p className="empty-subtitle">
                                Ask me anything about medical conditions, symptoms, or upload your
                                medical documents for analysis
                            </p>
                            <div className="quick-prompts">
                                {quickPrompts.map((prompt, idx) => (
                                    <button
                                        key={idx}
                                        className="prompt-btn"
                                        onClick={() => handleQuickPrompt(prompt)}
                                    >
                                        {prompt}
                                    </button>
                                ))}
                            </div>
                        </div>
                    ) : (
                        <>
                            {messages.map((message) => (
                                <div key={message.id} className={`message ${message.type}`}>
                                    <div className="message-avatar">
                                        {message.type === "user" ? "👤" : "🤖"}
                                    </div>
                                    <div>
                                        <div className="message-bubble">
                                            {/* Format response text with proper paragraph breaks */}
                                            {cleanText(message.content).split('\n').map((paragraph, idx) => (
                                                paragraph.trim() && (
                                                    <p key={idx} style={{ marginBottom: '12px', lineHeight: '1.6' }}>
                                                        {paragraph}
                                                    </p>
                                                )
                                            ))}
                                        </div>
                                        {message.sources &&
                                            message.sources.length > 0 && (
                                                <div className="message-sources">
                                                    <strong>Sources:</strong>
                                                    {message.sources.map(
                                                        (source, idx) => (
                                                            <span
                                                                key={idx}
                                                                className="source-badge"
                                                            >
                                                                📄 {source.split("\\").pop()}
                                                            </span>
                                                        )
                                                    )}
                                                </div>
                                            )}
                                    </div>
                                </div>
                            ))}

                            {loading && (
                                <div className="message assistant">
                                    <div className="message-avatar">🤖</div>
                                    <div className="message-bubble">
                                        <div className="loading-dots">
                                            <div className="loading-dot"></div>
                                            <div className="loading-dot"></div>
                                            <div className="loading-dot"></div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="input-area">
                    <div className="input-wrapper">
                        <form className="input-form" onSubmit={handleSubmitQuestion}>
                            <div className="input-field">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    placeholder="Ask your medical question here..."
                                    disabled={loading}
                                    autoFocus
                                />
                            </div>

                            <div className="input-actions">
                                <button
                                    type="button"
                                    className="action-btn"
                                    onClick={() => setShowUploadModal(true)}
                                    title="Upload Documents"
                                    disabled={loading}
                                >
                                    📎
                                </button>

                                <button
                                    type="submit"
                                    className="send-btn"
                                    disabled={loading || !input.trim()}
                                >
                                    {loading ? "..." : "Send"}
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

            {/* Upload Modal */}
            {showUploadModal && (
                <div className="upload-modal">
                    <div className="modal-content">
                        <div className="modal-header">📤 Upload Medical Documents</div>
                        <div className="modal-description">
                            Upload PDF documents to analyze and ask questions about them
                        </div>

                        {/* Upload Zone */}
                        <div
                            className="upload-zone"
                            onClick={() => fileInputRef.current?.click()}
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                            onDrop={handleDrop}
                        >
                            <div className="upload-icon">📄</div>
                            <div className="upload-text">Click to upload or drag and drop</div>
                            <div className="upload-subtext">PDF files only</div>
                            <input
                                ref={fileInputRef}
                                type="file"
                                multiple
                                accept=".pdf"
                                onChange={handleFileSelect}
                                className="file-input"
                            />
                        </div>

                        {/* Uploaded Files List */}
                        {uploadedFiles.length > 0 && (
                            <div className="uploaded-files">
                                <strong style={{ fontSize: "13px" }}>
                                    Selected Files ({uploadedFiles.length}):
                                </strong>
                                {uploadedFiles.map((file, idx) => (
                                    <div key={idx} className="file-item">
                                        <span className="file-item-icon">📄</span>
                                        <span className="file-item-name">{file.name}</span>
                                        <button
                                            type="button"
                                            className="file-item-remove"
                                            onClick={() => removeFile(file.name)}
                                        >
                                            ✕
                                        </button>
                                    </div>
                                ))}
                            </div>
                        )}

                        {/* Actions */}
                        <div className="modal-actions">
                            <button
                                className="btn-secondary"
                                onClick={() => {
                                    setShowUploadModal(false);
                                    setUploadedFiles([]);
                                }}
                                disabled={loading}
                            >
                                Cancel
                            </button>
                            <button
                                className="btn-primary"
                                onClick={handleUploadFiles}
                                disabled={uploadedFiles.length === 0 || loading}
                            >
                                {loading ? "Uploading..." : "Upload"}
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

// Render app
ReactDOM.createRoot(document.getElementById("root")).render(<MedicalAssistant />);
