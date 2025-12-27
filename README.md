# 🚮 Automated Incident Report Workflow

> An intelligent n8n workflow for automated waste management incident reporting with AI-powered duplicate detection and smart routing.

![n8n](https://img.shields.io/badge/n8n-Workflow-EA4B71?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=flat-square&logo=mongodb&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-AI-orange?style=flat-square)
![Gmail](https://img.shields.io/badge/Gmail-Integration-EA4335?style=flat-square&logo=gmail&logoColor=white)

---

## 📋 Overview

This workflow automates the entire lifecycle of citizen-reported waste management incidents. It intelligently processes incoming email reports, extracts structured data using AI, detects duplicates, and routes notifications appropriately—all without manual intervention.

### 🎯 Key Features

- **📧 Email Monitoring**: Automatic polling of Gmail inbox for new incident reports
- **🤖 AI-Powered Extraction**: Uses Groq LLM to extract structured incident data from natural language emails
- **🔍 Duplicate Detection**: Intelligent similarity-based duplicate detection using MongoDB queries
- **📊 Priority Classification**: Automatic incident priority assignment (low/medium/high)
- **🔄 Smart Routing**: Conditional logic to notify admins for new incidents or inform citizens about duplicates
- **💾 MongoDB Integration**: Seamless database queries for duplicate checking
- **✉️ Automated Responses**: AI-generated contextual email replies

---

## 🏗️ Workflow Architecture

```
Gmail Trigger → Get Email → AI Extract Data → Format Fields → 
Duplicate Check (AI + MongoDB) → Format Results → Condition Check
                                                      ↓
                         ┌────────────────────────────┴────────────────────────────┐
                         ↓                                                         ↓
                 [Duplicate Found]                                         [New Incident]
                         ↓                                                         ↓
              Generate Citizen Reply                                  Generate Admin Alert
                         ↓                                                         ↓
                Reply to Citizen Email                               Email Admin Notification
```

---

## 🔧 Prerequisites

Before running this workflow, ensure you have:

- **n8n** installed and running (self-hosted or cloud)
- **Gmail Account** with OAuth2 credentials configured
- **MongoDB** database with an `incidents` collection
- **Groq API** account and API key
- Required n8n nodes:
  - `@n8n/n8n-nodes-langchain` (AI Agent nodes)
  - `n8n-nodes-base.gmail` (Gmail integration)
  - `n8n-nodes-base.mongoDbTool` (MongoDB tool)

---

## ⚙️ Setup Instructions

### 1. Clone or Import Workflow

Import the `incident_report.json` file into your n8n instance:

```bash
# Via n8n UI
Settings → Import from File → Select incident_report.json
```

### 2. Configure Credentials

#### Gmail OAuth2
1. Navigate to the **Gmail Trigger** node
2. Click **Create New Credential**
3. Follow Google OAuth2 setup instructions
4. Grant necessary permissions (read, send, reply)

#### MongoDB Connection
1. Open the **Find documents in MongoDB** node
2. Add MongoDB credentials:
   - Connection String or Host/Port
   - Database name
   - Username/Password (if applicable)

#### Groq API
1. Navigate to the **Groq Chat Model** node
2. Add your Groq API key
3. Select your preferred model (default: llama-based models)

### 3. Update Configuration

Update these values in the workflow:

| Node | Parameter | Description |
|------|-----------|-------------|
| `Find documents in MongoDB` | `collection` | Set to your incidents collection name (e.g., `"incidents"`) |
| `Gmail` (Admin notification) | `sendTo` | Replace `azizmabrouk@ieee.org` with your admin email |
| `Gmail Trigger` | `pollTimes` | Adjust polling frequency (default: every minute) |

---

## 🚀 How It Works

### 1️⃣ **Email Monitoring**
The workflow continuously polls your Gmail inbox for new messages containing incident reports from citizens.

### 2️⃣ **Data Extraction**
When a new email arrives, an AI agent analyzes the content and extracts structured data:

```json
{
  "description": "Extracted incident summary",
  "location": "Street address or landmark",
  "priority": "low | medium | high",
  "reportedAt": "ISO 8601 timestamp",
  "citizenId": "Extracted if mentioned",
  "pickUpPointId": "Extracted if mentioned"
}
```

**Priority Rules**:
- `high` → Fire hazard, health risk, dangerous materials
- `medium` → Road blockage, strong odor, significant obstruction
- `low` → Regular waste accumulation

### 3️⃣ **Duplicate Detection**
The extracted incident is compared against existing MongoDB records using:
- Semantic similarity analysis
- Location matching
- Description comparison

A similarity score is calculated, and incidents with score ≥ 0.75 are flagged as duplicates.

### 4️⃣ **Smart Routing**

**If Duplicate Found** (isDuplicate=true AND similarityScore ≥ 0.75):
- Generate personalized reply to citizen
- Inform them the incident is already being handled
- Reply to their original email thread

**If New Incident**:
- Generate admin notification with incident details
- Send alert email to municipal admin
- Admin can take action on the new report

---

## 📊 Data Schema

### Extracted Incident Format

```json
{
  "_id": null,
  "assignedTo": null,
  "citizenId": "string | null",
  "description": "string",
  "imageUrl": null,
  "location": "string",
  "pickUpPointId": "string | null",
  "priority": "low | medium | high",
  "reportedAt": "2024-12-27T10:30:00.000Z",
  "resolutionNotes": null,
  "resolvedAt": null,
  "status": "new"
}
```

### Duplicate Check Response

```json
{
  "isDuplicate": true,
  "matchedIncidentId": "507f1f77bcf86cd799439011",
  "similarityScore": 0.89,
  "incidentDescription": "...",
  "incidentLocation": "...",
  "priority": "medium",
  "reportedAt": "2024-12-27T10:30:00.000Z"
}
```

---

## 🎨 Customization

### Modify AI System Prompts

Each AI Agent node has a customizable system message. You can adjust:

- **AI Agent2**: Incident extraction logic and field mapping
- **AI Agent**: Duplicate detection criteria and similarity thresholds
- **AI Agent1**: Admin notification email tone and format
- **AI Agent3**: Citizen reply email style and content

### Adjust Duplicate Threshold

In the **If** node, modify the similarity score threshold:

```json
{
  "leftValue": "={{ $json.similarityScore }}",
  "rightValue": 0.75  // Change this value (0.0 - 1.0)
}
```

### Add Additional Workflows

Consider extending with:
- Slack/Discord notifications
- SMS alerts for high-priority incidents
- Automatic ticket creation in project management tools
- Image analysis if attachments are present

---

## 🛡️ Security Considerations

- ✅ Use environment variables for sensitive credentials
- ✅ Implement rate limiting on Gmail API calls
- ✅ Validate and sanitize all email inputs
- ✅ Use MongoDB query filters to prevent injection
- ✅ Regularly rotate API keys
- ✅ Monitor workflow execution logs for anomalies

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Gmail not triggering | Check OAuth2 token expiration; verify polling settings |
| AI extraction fails | Ensure Groq API key is valid; check model availability |
| MongoDB connection error | Verify connection string; check network/firewall rules |
| Duplicates not detected | Confirm collection name is correct; verify data exists |
| Emails not sending | Check Gmail API quotas; verify recipient addresses |

---

## 📈 Performance Optimization

- **Polling Interval**: Adjust based on expected incident volume
- **AI Model Selection**: Choose faster models for lower latency
- **MongoDB Indexing**: Create indexes on `location` and `description` fields
- **Batch Processing**: Consider processing multiple emails in parallel

---

## 🤝 Contributing

Suggestions for improvements:

1. Add image attachment processing
2. Implement multi-language support
3. Create a citizen-facing web form
4. Add analytics dashboard integration
5. Implement incident status update notifications

---

## 📄 License

This workflow is provided as-is for educational and operational purposes.

---

## 👨‍💻 Author

Built with ❤️ for modern municipal waste management

---

## 🔗 Resources

- [n8n Documentation](https://docs.n8n.io/)
- [Groq API Docs](https://console.groq.com/docs)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [Gmail API Reference](https://developers.google.com/gmail/api)

---

**Need help?** Open an issue or contact your system administrator.
