import streamlit as st
import boto3
import json
import os
from typing import Dict, Any
from streamlit.errors import StreamlitSecretNotFoundError

st.set_page_config(
    page_title="Bedrock Doc Assistant", page_icon="🤖", layout="wide"
)

st.title("🤖 Bedrock Doc Assistant")
st.markdown("Chat with Amazon Bedrock for Doc assistance")

def get_secret(key: str, default: str = "") -> str:
    try:
        return st.secrets.get(key, os.environ.get(key, default))
    except (StreamlitSecretNotFoundError, FileNotFoundError):
        return os.environ.get(key, default)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "client" not in st.session_state:
    st.session_state.client = None

if "kb_id" not in st.session_state:
    st.session_state.kb_id = get_secret("KNOWLEDGE_BASE_ID", "")

if "model_arn" not in st.session_state:
    st.session_state.model_arn = get_secret(
        "BEDROCK_MODEL_ARN",
        "arn:aws:bedrock:ap-southeast-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
    )

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    access_key_id = st.text_input(
        "AWS Access Key ID",
        type="password",
        value=get_secret("AWS_ACCESS_KEY_ID", ""),
        help="IAM access key ID with Bedrock permissions",
    )

    secret_access_key = st.text_input(
        "AWS Secret Access Key",
        type="password",
        value=get_secret("AWS_SECRET_ACCESS_KEY", ""),
        help="IAM secret access key with Bedrock permissions",
    )

    session_token = st.text_input(
        "AWS Session Token (optional)",
        type="password",
        value=get_secret("AWS_SESSION_TOKEN", ""),
        help="Required for temporary credentials",
    )

    kb_id = st.text_input(
        "Knowledge Base ID",
        value=st.session_state.kb_id,
        help="Enter your Knowledge Base ID",
    )

    model_arn = st.text_input(
        "Model ARN",
        value=st.session_state.model_arn,
        help="Enter the Bedrock model ARN used for retrieve_and_generate",
    )

    if st.button("Update Configuration"):
        try:
            if not access_key_id or not secret_access_key:
                raise ValueError(
                    "AWS Access Key ID and Secret Access Key are required."
                )
            st.session_state.client = boto3.client(
                "bedrock-agent-runtime",
                region_name="ap-southeast-2",
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key,
                aws_session_token=session_token or None,
            )
            st.session_state.kb_id = kb_id or st.session_state.kb_id
            st.session_state.model_arn = model_arn or st.session_state.model_arn
            st.success("Configuration updated successfully!")
        except Exception as e:
            st.error(f"Failed to update configuration: {e}")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about Doc..."):
    if not st.session_state.client:
        st.error("Please configure your AWS access key and secret in the sidebar first.")
        st.stop()

    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.client.retrieve_and_generate(
                    input={"text": prompt},
                    retrieveAndGenerateConfiguration={
                        "type": "KNOWLEDGE_BASE",
                        "knowledgeBaseConfiguration": {
                            "knowledgeBaseId": st.session_state.kb_id,
                            "modelArn": st.session_state.model_arn,
                        },
                    },
                )

                completion = response.get("output", {}).get(
                    "text", "No response received"
                )

                st.markdown(completion)
                st.session_state.messages.append(
                    {"role": "assistant", "content": completion}
                )

            except Exception as e:
                error_msg = f"Error calling Bedrock: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

# Clear chat button
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()
