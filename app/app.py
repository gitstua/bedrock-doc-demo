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

if "creds_from_env" not in st.session_state:
    st.session_state.creds_from_env = False

if "kb_id" not in st.session_state:
    st.session_state.kb_id = get_secret("KNOWLEDGE_BASE_ID", "")

if "model_arn" not in st.session_state:
    st.session_state.model_arn = get_secret(
        "BEDROCK_MODEL_ARN",
        "arn:aws:bedrock:ap-southeast-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0",
    )

def initialize_client(access_key_id, secret_access_key, session_token, kb_id, model_arn):
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
        return True
    except Exception as e:
        st.error(f"Failed to update configuration: {e}")
        return False

# Auto-initialize if credentials are provided via secrets/env
if st.session_state.client is None:
    env_access_key = get_secret("AWS_ACCESS_KEY_ID", "")
    env_secret_key = get_secret("AWS_SECRET_ACCESS_KEY", "")
    if env_access_key and env_secret_key:
        if initialize_client(
            env_access_key,
            env_secret_key,
            get_secret("AWS_SESSION_TOKEN", ""),
            st.session_state.kb_id,
            st.session_state.model_arn
        ):
            st.session_state.creds_from_env = True
            st.sidebar.info("Configuration auto-loaded from environment variables.")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    access_key_id_input = st.text_input(
        "AWS Access Key ID",
        type="password",
        value="",
        placeholder="Loaded from environment" if st.session_state.creds_from_env else "Enter Access Key ID",
        help="IAM access key ID with Bedrock permissions",
    )

    secret_access_key_input = st.text_input(
        "AWS Secret Access Key",
        type="password",
        value="",
        placeholder="Loaded from environment" if st.session_state.creds_from_env else "Enter Secret Access Key",
        help="IAM secret access key with Bedrock permissions",
    )

    session_token_input = st.text_input(
        "AWS Session Token (optional)",
        type="password",
        value="",
        placeholder="Loaded from environment" if st.session_state.creds_from_env else "Optional Session Token",
        help="Required for temporary credentials",
    )

    kb_id_input = st.text_input(
        "Knowledge Base ID",
        value=st.session_state.kb_id,
        help="Enter your Knowledge Base ID",
    )

    model_arn_input = st.text_input(
        "Model ARN",
        value=st.session_state.model_arn,
        help="Enter the Bedrock model ARN used for retrieve_and_generate",
    )

    if st.button("Update Configuration"):
        # Fallback to environment variables if inputs are blank and they were loaded correctly
        final_access_key = access_key_id_input or (get_secret("AWS_ACCESS_KEY_ID", "") if st.session_state.creds_from_env else "")
        final_secret_key = secret_access_key_input or (get_secret("AWS_SECRET_ACCESS_KEY", "") if st.session_state.creds_from_env else "")
        final_session_token = session_token_input or (get_secret("AWS_SESSION_TOKEN", "") if st.session_state.creds_from_env else "")
        
        if initialize_client(final_access_key, final_secret_key, final_session_token, kb_id_input, model_arn_input):
            # If user manually provided keys, we are no longer purely "from env" in the sense of the UI placeholder
            if access_key_id_input or secret_access_key_input:
                st.session_state.creds_from_env = False
            st.success("Configuration updated successfully!")

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
