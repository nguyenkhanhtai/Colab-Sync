# Guide: Obtaining credentials.json from Google Cloud

For this toolset (CLI and MCP Server) to connect to your Google Drive, you need to create an OAuth 2.0 application on Google Cloud and download the `credentials.json` file.

Here are the detailed steps (takes about 3-5 minutes):

## Step 1: Create a Project on Google Cloud
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Sign in with your Google account (the account containing the Drive where you want to store your notebooks).
3. In the top-left corner (next to the Google Cloud logo), click the Project dropdown menu and select **New Project**.
4. Enter a project name (e.g., `Colab Sync App`) and click **Create**. Wait a moment for the project to be created and ensure you have selected that project.

## Step 2: Enable the Google Drive API
1. In the left navigation menu, go to **APIs & Services** > **Library**.
2. Search for `Google Drive API`.
3. Click on the **Google Drive API** result and click the **Enable** button.

## Step 3: Configure the OAuth Consent Screen
1. Go back to the left menu: **APIs & Services** > **OAuth consent screen**.
2. Choose **External** for the User Type and click **Create**.
3. Fill in the required information (marked with a red asterisk):
   - **App name**: `Colab Sync` (or any name you prefer)
   - **User support email**: Select your email
   - **Developer contact information**: Enter your email
4. Click **Save and Continue** through the Scopes and Test users steps (you can leave them blank, or for safety, add your own email to the Test users section). Finally, click **Back to Dashboard**.
5. *(Important)* On the Dashboard, click **PUBLISH APP** and confirm. This prevents you from having to re-verify constantly (even though Google will warn that the app is unverified during login, you can safely click "Continue").

## Step 4: Create Credentials
1. In the left navigation menu, select **Credentials**.
2. Click the **+ CREATE CREDENTIALS** button at the top and select **OAuth client ID**.
3. Under **Application type**, choose **Desktop app**.
4. Enter a name (e.g., `Colab CLI`) and click **Create**.
5. A dialog box will appear; click **DOWNLOAD JSON** to download the file to your computer.
6. Rename the downloaded file to **`credentials.json`** and copy it into the `e:\Documents\Programming\AI\Colab MCP\` directory.

---

Once you have the `credentials.json` file in this directory, the system is ready to be installed and used!
