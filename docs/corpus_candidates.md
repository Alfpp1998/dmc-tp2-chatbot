# Corpus Candidates For Chunking

## Purpose

This document lists candidate sources for the phase 1 chatbot corpus.
The goal is to keep the corpus curated, useful for retrieval, and small enough to evaluate and demo reliably.

## Recommended Corpus Strategy

Build the first corpus in three layers:

- project-specific documents
- official marketing and advertising documentation
- optional research papers

For the MVP, start with a compact corpus of around 10 to 15 documents.

## 1. Project Documents

These are the highest-priority sources because they describe the project scope, architecture, and intended behavior.

- [context_report_new.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/context_report_new.md:1)
- [proyecto_final_chatbot_specs.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/proyecto_final_chatbot_specs.md:1)
- [ARCHITECTURE.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/architecture/ARCHITECTURE.md:1)
- [REQUIREMENTS.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/specs/REQUIREMENTS.md:1)
- [rag_pipeline.md](/Users/chperezpelaez/Documents/Github/dmc-tp2-chatbot/docs/specs/rag_pipeline.md:1)

## 2. Official Marketing And Ads Sources

These sources are strong candidates if the chatbot should answer marketing, ad-system, and metric-definition questions.

### Google Ads

- CTR: https://support.google.com/google-ads/answer/2615875?hl=en-EN
- Average CPC: https://support.google.com/google-ads/answer/14074?hl=en-ca
- Conversion rate: https://support.google.com/google-ads/answer/2684489?hl=en-EN
- Quality Score: https://support.google.com/google-ads/answer/6167118?hl=en
- Ad Rank: https://support.google.com/google-ads/answer/1722122?hl=en-001&ref_topic=10549279
- Campaigns overview: https://developers.google.com/google-ads/api/docs/campaigns/overview
- Smart Bidding: https://support.google.com/google-ads/answer/14697340?hl=en-EN
- Build effective keyword lists: https://support.google.com/google-ads/answer/10039665?hl=en

### Meta / Facebook Ads

- Ad objectives: https://www.facebook.com/business/ads/ad-objectives
- Ad auction explained: https://www.facebook.com/business/ads/ad-auction
- Awareness objective: https://www.facebook.com/business/ads/ad-objectives/awareness
- Traffic objective: https://www.facebook.com/business/ads/ad-objectives/traffic
- Sales objective: https://www.facebook.com/business/ads/ad-objectives/sales
- Conversions API: https://www.facebook.com/business/help/AboutConversionsAPI
- Meta Ad Library: https://www.facebook.com/help/259468828226154/

### IAB Glossaries

- IAB Glossary of Terminology: https://www.iab.com/insights/glossary-of-terminology/
- IAB Digital Video Advertising Glossary: https://www.iab.com/insights/digital-video-advertising-glossary/

## 3. Optional Research Papers

These are useful if the chatbot should also explain the theory behind RAG or future recommendation-system extensions.

### RAG

- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks: https://arxiv.org/abs/2005.11401

### Bandits And Recommendation

- A Contextual-Bandit Approach to Personalized News Article Recommendation: https://arxiv.org/abs/1003.0146
- Doubly Robust Policy Evaluation and Learning: https://arxiv.org/abs/1103.4601
- Finite-time Analysis of the Multiarmed Bandit Problem: https://doi.org/10.1023/A:1013689704352

## Suggested MVP Corpus V1

Start with this compact set:

- 5 local project documents
- 5 Google Ads documents: CTR, Average CPC, Conversion rate, Quality Score, Ad Rank
- 3 Meta documents: Ad objectives, Ad auction, Conversions API
- 1 IAB glossary document
- 1 RAG paper

This gives the chatbot a small but high-value corpus that is still easy to chunk, inspect, and evaluate.

## Selection Guidance

- prioritize official sources over blogs or secondary summaries
- avoid adding too many overlapping documents early
- keep the corpus small enough to inspect retrieval quality manually
- prefer documents with stable terminology and clear definitions
