LINE Webhook for STT and TTS 
===

## Summary 

This is a LINE chatbot webhook that integrates with an audio handler to perform STT and TTS. 
The STT and TTS models are implemented using the GCP Vertex AI API and LLM specifically employs the Google PaLM2 model.

---

## Prerequisite
- [LINE Messaging API (Chatbot)](https://developers.line.biz/console/)
    - Channel Access Token
    - Channel Secret
- [Google Cloud Platform (GCP)](https://console.cloud.google.com/)
    - Billing
    - Cloud Run
    - Cloud Storage
    - STT API
    - TTS API
    - PaLM2 API
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)
    - gcloud command
---


## Deploy to GCP Cloud Run (MacOS/Linux)

>1. Fill `Basic Settings` in `Makefile` and save.

>2. Open termainal in your working directory, exec the below and follow the instruction
```
make deploy
```

>3. After a successful deployment, verify if the service URL is working and trace debug info using the GCP Cloud Run console if necessary.

>4. Fill the url as webhook on LINE Developer Messaging API Console.

> 5. Send an voice records in your LINE Chatbot and test STT, LLM, TTS performance.
---