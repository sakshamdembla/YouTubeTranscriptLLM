# Deployment Guide for Streamlit Cloud

This guide will help you deploy your YouTube Transcript AI application to Streamlit Cloud.

## Prerequisites

1. A GitHub repository with your code
2. An OpenAI API key
3. A Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

## Step 1: Prepare Your Repository

1. Make sure all your code is committed to GitHub
2. Ensure your `requirements.txt` file includes all necessary dependencies
3. Verify that sensitive files (`.env`, `.streamlit/secrets.toml`) are in `.gitignore`

## Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository
5. Choose the main branch
6. Set the main file path to `app.py` (or your main Streamlit file)
7. Click "Deploy"

## Step 3: Configure Secrets

1. Once your app is deployed, go to your app's dashboard
2. Click on "Settings" (gear icon)
3. Go to the "Secrets" tab
4. Add your secrets in TOML format:

```toml
OPENAI_API_KEY = "your-actual-openai-api-key-here"
```

5. Click "Save"

## Step 4: Test Your Deployment

1. Your app should automatically redeploy after adding secrets
2. Test all functionality to ensure everything works correctly
3. Check the logs if there are any issues

## Local Development with Secrets

For local development, you can create a `.streamlit/secrets.toml` file:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

**Important**: This file is already in `.gitignore` to prevent accidental commits.

## Troubleshooting

### Common Issues:

1. **Missing dependencies**: Make sure all packages are in `requirements.txt`
2. **API key not found**: Verify the secret is correctly set in Streamlit Cloud
3. **Import errors**: Check that all relative imports are correct

### Checking Logs:

1. Go to your app dashboard on Streamlit Cloud
2. Click on "Manage app"
3. View the logs to see any error messages

## Security Best Practices

1. Never commit API keys or secrets to your repository
2. Use Streamlit's secrets management for sensitive data
3. Regularly rotate your API keys
4. Monitor your OpenAI usage to detect any unusual activity

## Updating Your App

1. Push changes to your GitHub repository
2. Streamlit Cloud will automatically detect changes and redeploy
3. You can also manually trigger a reboot from the app dashboard

## Support

- Streamlit Cloud documentation: [docs.streamlit.io](https://docs.streamlit.io)
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- OpenAI API documentation: [platform.openai.com/docs](https://platform.openai.com/docs) 