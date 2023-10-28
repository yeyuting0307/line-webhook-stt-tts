LINE Webhook for STT and TTS 
===

## Summary 

![architecture](https://github.com/yeyuting0307/line-webhook-stt-tts/assets/35023161/ba34d819-71b7-43ec-8c69-cfdacd6743f0)

This is a simple LINE chatbot webhook integrated with an audio handler for performing Speech-to-Text (STT) and Text-to-Speech (TTS) functions. In this example, the STT, Language Model (LLM), and TTS models are implemented using the GCP Vertex AI APIs; however, you can replace these with your own models.

---

## Prerequisite
- [LINE Messaging API (Chatbot)](https://developers.line.biz/console/)
    - Channel Access Token
    - Channel Secret
- [Google Cloud Platform (GCP)](https://console.cloud.google.com/)
    - [Enable Billing](https://console.cloud.google.com/billing/projects)
    - [Create Cloud Storage Buckets](https://console.cloud.google.com/storage/browser)
    - [Enable Cloud Speech-to-Text API](https://console.cloud.google.com/marketplace/product/google/speech.googleapis.com)
    - [Enable Cloud Text-to-Speech API](https://console.cloud.google.com/marketplace/product/google/texttospeech.googleapis.com)
    - [Enable Vertex AI PaLM2 API](https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/chat-bison)
    - [Enable Cloud Build API](https://console.cloud.google.com/marketplace/product/google/cloudbuild.googleapis.com)
    - [Enable Google Container Registry API](https://console.cloud.google.com/marketplace/product/google/containerregistry.googleapis.com)
    - [(For Docker) Enable Artifact Registry API](https://console.cloud.google.com/marketplace/product/google/artifactregistry.googleapis.com)
    - [(For Docker) Create a Docker repository of Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/store-docker-container-images)
- [gcloud CLI](https://cloud.google.com/sdk/docs/install)
    - `gcloud auth login`
    - `gcloud auth application-default login`
---

## Deploy to GCP Cloud Run (MacOS/Linux)

1. Fill out the `Basic Settings` in the `Makefile` and save it
2. Open a terminal in your working directory, execute the command below, and follow the instructions:
```
make deploy
```
> Note : If you have not installed [Docker](https://www.docker.com/products/docker-desktop/),utilize the `gcloud builds submit`(option 2) instead. Monitor the build process on [Cloud Build](https://console.cloud.google.com/cloud-build) and verify the images on [Container Registry](https://console.cloud.google.com/gcr).
3. After a successful deployment, ensure that the service URL is functioning correctly. If necessary, trace debugging information using the [GCP Cloud Run console](https://console.cloud.google.com/run). Remember to [configure the environment parameters](https://cloud.google.com/run/docs/configuring/services/environment-variables) being used.
4. Enter the URL as the webhook on the [LINE Developer Messaging API Console](https://developers.line.biz/console/).
5. Send voice recordings through your LINE Chatbot and test the performance of STT, LLM, TTS.

---
