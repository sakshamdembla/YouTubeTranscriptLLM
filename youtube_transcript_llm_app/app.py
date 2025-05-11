# Main Streamlit application
import streamlit as st
from utils import transcript_utils

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("YouTube Transcript LLM App")

st.write("Welcome to the YouTube Transcript LLM App. This application allows you to analyze YouTube video transcripts using LLM technology.")

# Add YouTube URL input
st.subheader("Enter YouTube Video URL")
youtube_url = st.text_input("YouTube URL", "")

if youtube_url:
    # Extract video ID
    try:
        video_id = transcript_utils.get_video_id(youtube_url)
        
        # Try to get video title
        video_title = transcript_utils.get_video_title(youtube_url)
        st.subheader(f"Video: {video_title}")
        
        # Get transcript
        transcript = transcript_utils.get_transcript(video_id)
        
        # Check if transcript is an error message
        transcript_available = not (transcript.startswith("Error fetching transcript") or 
                                   transcript.startswith("No transcript available") or
                                   transcript.startswith("Transcripts are disabled"))
        
        # Display transcript or error message
        if transcript_available:
            st.subheader("Transcript")
            with st.expander("Show Transcript"):
                # Make transcript scrollable if it's long
                st.markdown(
                    f"""
                    <div style="max-height: 300px; overflow-y: auto; border: 1px solid #e6e6e6; padding: 15px; border-radius: 5px; background-color: #f9f9f9;">
                        {transcript}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
            
            # Chat interface section
            st.subheader("Chat with the Transcript")
            st.markdown("Ask questions about the transcript or request analysis. The AI has access to the full transcript content.")
            
            # Display chat history
            chat_container = st.container()
            with chat_container:
                for i, message in enumerate(st.session_state.chat_history):
                    role = message["role"]
                    content = message["content"]
                    
                    # Display the message with appropriate styling
                    with st.chat_message(role):
                        if role == "assistant":
                            # Make assistant responses scrollable if they're long
                            if len(content) > 500:  # If content is long
                                st.markdown(
                                    f"""
                                    <div style="max-height: 300px; overflow-y: auto;">
                                        {content}
                                    </div>
                                    """, 
                                    unsafe_allow_html=True
                                )
                            else:
                                st.write(content)
                        else:
                            st.write(content)
            
            # Chat input
            user_input = st.chat_input("Ask a question about the transcript...")
            
            if user_input:
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                
                # Process the user input with LLM
                try:
                    # Import LLM module here
                    from llm import interactions
                    
                    with st.spinner("Thinking..."):
                        # Create context for the LLM
                        context = f"The following is a conversation about a YouTube video transcript. Here's the transcript:\n\n{transcript}\n\nAnswer questions about this content."
                        
                        # Create a combined prompt with context, chat history, and new question
                        chat_history_text = ""
                        for msg in st.session_state.chat_history[:-1]:  # Exclude the most recent user message
                            prefix = "User: " if msg["role"] == "user" else "Assistant: "
                            chat_history_text += f"{prefix}{msg['content']}\n\n"
                        
                        # Combine everything into one prompt
                        full_prompt = f"{context}\n\nPrevious conversation:\n{chat_history_text}\n\nUser: {user_input}\n\nAssistant:"
                        
                        # Get response from LLM
                        result = interactions.analyze_transcript(transcript, full_prompt)
                        
                        # Add assistant response to chat history
                        st.session_state.chat_history.append({"role": "assistant", "content": result})
                        
                        # Rerun to update the UI with the new message
                        st.rerun()
                except Exception as e:
                    # Add error message to chat history
                    error_msg = f"I'm sorry, I encountered an error: {str(e)}"
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
                    st.rerun()
        else:
            # Display a more helpful error message when transcript isn't available
            st.error(transcript)
            st.info("💡 Try a different YouTube video that has captions or transcripts available. Popular videos, educational content, and videos from major channels are more likely to have transcripts.")
            
            # Display some example URLs that are known to have transcripts
            st.subheader("Try these examples:")
            st.markdown("- [TED Talk: The danger of AI is weirder than you think](https://www.youtube.com/watch?v=OhCzX0iLnOc)")
            st.markdown("- [Khan Academy: Introduction to the atom](https://www.youtube.com/watch?v=1xSQlwWGT8M)")
            st.markdown("- [NASA: Overview of the James Webb Space Telescope](https://www.youtube.com/watch?v=4P8fKd0IVOs)")
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
