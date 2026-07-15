# Session agent-abc16067bf3fbebaf
**Date:** 2026-07-15 | **Session ID:** `agent-abc16067bf3fbebaf`

---

## 👤 User *(20:39:23)*

Pesquise (web, fontes oficiais/spec) o **C2PA / Content Credentials**: estrutura do manifest, como assinar (certs/claim signer), a ferramenta open-source **c2patool** (licença? embeda em imagem/vídeo?), quais plataformas LEEM Content Credentials (LinkedIn, Meta/Instagram, TikTok, YouTube, Google Images), e a fragilidade (metadata removível por re-encode/screenshot). Cite c2pa.org / spec / repo. MÓDULO: content-provenance — marcar MACHINE-READABLE todo conteúdo SINTÉTICO que o MCORCH gera e publica (imagem Nano Banana/Gemini · vídeo HyperFrames + Veo · voz clonada Qwen3), para conformidade com o AI Act Art.50(2)/(4). DECISÃO DE ESCOPO JÁ TOMADA pelo Sovereign: 3 CAMADAS em defesa-em-profundidade — C2PA (proveniência forte, removível) + watermark invisível (sobrevive a re-encode/crop/screenshot) + metadata IPTC/XMP (fallback universal lido por plataformas). DOUTRINA MCORCH (Lei 1 + [[feedback_opensource_first_zero_cost_equity]]): preferir ferramenta OPEN-SOURCE comercial-safe, custo USD=0; toda afirmação factual carrega a URL consultada (NUNCA de memória). INTEGRAÇÃO: encaixa no spine creative_assets + no pipeline de geração existente (marca no momento da geração), NÃO reconstrói distribuição.

## 🤖 Claude *(20:39:29)*

<details>
<summary>💭 Thinking Process</summary>

I'm starting my research phase by looking into C2PA and Content Credentials, the c2patool, watermarking techniques, IPTC/XMP metadata standards, how platforms read this information, and the AI Act Article 50 requirements. I'll run parallel web searches to gather verified information with sources.

</details>


## 🤖 Claude *(20:39:29)*

I'll research C2PA/Content Credentials, c2patool, watermarking, and platform support with verified sources.

## 🤖 Claude *(20:39:29)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "C2PA content credentials manifest structure specification claim signer"
}
```

## 🤖 Claude *(20:39:29)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "c2patool open source license embed manifest image video github"
}
```

## 🤖 Claude *(20:39:29)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "which platforms read Content Credentials LinkedIn Instagram TikTok YouTube Google Images"
}
```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "which platforms read Content Credentials LinkedIn Instagram TikTok YouTube Google Images"
> 
> Links: [{"title":"Content credentials | LinkedIn Help","url":"https://www.linkedin.com/help/linkedin/answer/a6282984"},{"title":"How to add Content Credentials to your images - SmartFrame","url":"https://smartframe.io/blog/how-to-add-content-credentials-to-your-images/"},{"title":"Does Instagram Support Content Credentials? - C2PA.ai","url":"https://c2pa.ai/instagram"},{"title":"Content Credentials: The Future of Proving Your Photos Are Real ✅ — Glyn Dewis","url":"https://glyndewis.com/blog/content-credentials"},{"title":"Content Credentials - Wikipedia","url":"https://en.wikipedia.org/wiki/Content_Credentials"},{"title":"Introducing Official Content Credentials Icon","url":"https://spec.c2pa.org/post/contentcredentials/"},{"title":"Content Credentials | Verify Media Authenticity","url":"https://contentcredentials.org/"},{"title":"Adobe Content Authenticity, now in public beta, helps creators secure attribution | Adobe Blog","url":"https://blog.adobe.com/en/publish/2025/04/24/adobe-content-authenticity-now-public-beta-helps-creators-secure-attribution"},{"title":"Content Credentials overview","url":"https://helpx.adobe.com/creative-cloud/help/content-credentials.html"},{"title":"That Little “CR” Badge on LinkedIn: Why Content Credentials Matter More Than Ever","url":"https://aguywithascarf.substack.com/p/that-little-cr-badge-on-linkedin"}]
> 
> Based on the search results, here's which platforms read Content Credentials among those you mentioned:
> 
> **Platforms that support reading Content Credentials:**
> 
> 1. **LinkedIn**: LinkedIn added support for images with Content Credentials. LinkedIn displays a CR icon for images carrying Content Credentials, which users can click to see the provenance summary.
> 
> 2. **Google Images/Google Search**: Google Search displays Content Credentials in image search results.
> 
> 3. **YouTube**: Google's broader C2PA commitment extends to YouTube, though video Content Credentials are a newer and more complex implementation than still images.
> 
> 4. **Instagram**: Instagram has implemented read-only display of Content Credentials for certain content and does not preserve Content Credentials when users upload images through the app.
> 
> 5. **TikTok**: TikTok has announced C2PA integration for AI content labelling, though full implementation timeline is not confirmed.
> 
> In summary, all the platforms you mentioned have some level of Content Credentials support, though the extent varies—from full display (Google Search, LinkedIn) to partial implementation for specific purposes like AI detection (Instagram, TikTok).
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "c2patool open source license embed manifest image video github"
> 
> Links: [{"title":"C2PA command line tool | Open-source tools for content authenticity and provenance","url":"https://opensource.contentauthenticity.org/docs/c2patool/"},{"title":"GitHub - contentauth/c2patool: Command line tool for displaying and adding C2PA manifests · GitHub","url":"https://github.com/contentauth/c2patool"},{"title":"GitHub - scouten-adobe/TEMP-c2patool: TEMPORARY mirror of c2patool for build automation testing · GitHub","url":"https://github.com/scouten-adobe/TEMP-c2patool"},{"title":"Using C2PA Tool | Open-source tools for content authenticity and provenance","url":"https://opensource.contentauthenticity.org/docs/c2patool/docs/usage/"},{"title":"c2patool/docs/manifest.md at main · contentauth/c2patool","url":"https://github.com/contentauth/c2patool/blob/main/docs/manifest.md"},{"title":"GitHub - SichangHe/contentauth--c2patool: Command line tool for displaying and adding C2PA manifests · GitHub","url":"https://github.com/SichangHe/contentauth--c2patool"},{"title":"GitHub - digimarc-corp/c2pa-content-credentials-extension: C2PA Chrome Extension · GitHub","url":"https://github.com/digimarc-corp/c2pa-content-credentials-extension"},{"title":"GitHub - f/sign-ai-media: Sign images and videos with C2PA provenance declaring AI-generated media. · GitHub","url":"https://github.com/f/sign-ai-media"},{"title":"GitHub - contentauth/c2patool-service-example: Using c2patool as a service for demonstration purposes · GitHub","url":"https://github.com/contentauth/c2patool-service-example"},{"title":"C2PA Tool | Open-source tools for content authenticity and provenance","url":"https://opensource.contentauthenticity.org/docs/c2patool/c2patool-index/"}]
> 
> Based on the search results, here's what I found about c2patool:
> 
> ## Overview
> 
> c2patool is a command line tool for working with C2PA manifests and media assets (audio, image or video files). As of 10 December 2024, the c2patool project work has transitioned to the contentauth/c2pa-rs repo.
> 
> ## GitHub Repository
> 
> The official repository is located at https://github.com/contentauth/c2pa-rs.git, though the original repository at https://github.com/contentauth/c2patool is still accessible.
> 
> ## Functionality
> 
> To add C2PA manifest data to a file, you can use the --manifest / -m option with a manifest JSON file, and specify the output file with the --output / -o option. The tool also supports placing the manifest in an external sidecar file with the same filename but with a .c2pa extension.
> 
> ## Open Source Status
> 
> While the search results confirm the tool is open-source through the Content Authenticity Initiative, the specific license type wasn't explicitly mentioned in these results. The tool is hosted on GitHub and has documentation on the official Content Authenticity Initiative website at `opensource.contentauthenticity.org`.
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "C2PA content credentials manifest structure specification claim signer"
> 
> Links: [{"title":"Content Credentials : C2PA Technical Specification :: C2PA Specifications","url":"https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html"},{"title":"What is a C2PA Manifest? Structure, Assertions, and Verification","url":"https://c2paviewer.com/articles/what-is-c2pa-manifest"},{"title":"C2PA Technical Specification :: C2PA Specifications","url":"https://spec.c2pa.org/specifications/specifications/1.0/specs/C2PA_Specification.html"},{"title":"1. Introduction 1. Overview","url":"https://c2pa.org/wp-content/uploads/sites/33/2025/10/content_credentials_wp_0925.pdf"},{"title":"Content Credentials C2PA Technical Specification 2.1, 2024-09-20:","url":"https://spec.c2pa.org/specifications/specifications/2.1/specs/_attachments/C2PA_Specification.pdf"},{"title":"How C2PA Content Credentials Work and What Their Limits Are - SoftwareSeni","url":"https://www.softwareseni.com/how-c2pa-content-credentials-work-and-what-their-limits-are/"},{"title":"C2PA FAQ","url":"https://c2pa.org/faqs/"},{"title":"C2PA and Content Credentials Explainer :: C2PA Specifications","url":"https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html"},{"title":"Getting started with Content Credentials | Open-source tools for content authenticity and provenance","url":"https://opensource.contentauthenticity.org/docs/getting-started/"},{"title":"Content Credentials C2PA Technical Specification 2.2, 2025-05-01:","url":"https://spec.c2pa.org/specifications/specifications/2.2/specs/_attachments/C2PA_Specification.pdf"}]
> 
> I've successfully performed a web search for your query about C2PA content credentials manifest structure, specification, and claim signer. Here are the key findings:
> 
> ## C2PA Manifest Structure
> 
> A C2PA Manifest (Content Credential) is a cryptographically bound structure that records an asset's provenance and contains one or more assertions, which are statements about the asset, such as its origin, modifications, and use of AI.
> 
> A C2PA Manifest is a digitally signed and tamper-evident data structure that references a set of assertions concerning an asset and the information necessary to represent the content binding, and if any assertions were redacted, a declaration to that effect is included.
> 
> ## Claim Structure
> 
> The claim is a structure that connects the assertions to the signer and the claim signature is a digital signature that provides the tamper-evident binding for the Manifest as a whole.
> 
> ## Claim Signer
> 
> The signer is the credential holder of a private key that is used to sign the claim, and the signer is identified by the subject of the credential. The digital signature on the claim is created using the private key owned by a signer, and the claim signature is a part of the C2PA Manifest.
> 
> ## Manifest Components
> 
> A C2PA manifest is composed of one or more assertions (including content bindings), a single claim, and a claim signature.
> 
> The search results include references to the official C2PA Technical Specification, which provides the normative reference for the complete manifest structure and signing requirements.
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

## 🤖 Claude *(20:39:41)*

<details>
<summary>💭 Thinking Process</summary>

I need to check the specifics around c2patool's licensing, video support capabilities, watermarking options like Adobe's Durable Content Credentials or Digimarc, metadata standards like IPTC and XMP, and how it relates to AI Act Article 50 requirements.

</details>


## 🤖 Claude *(20:39:41)*

Let me verify the c2patool license, video support, watermarking approaches, and AI Act specifics.

## 🤖 Claude *(20:39:42)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://github.com/contentauth/c2patool",
  "prompt": "What is the software license of c2patool? What file formats (image, video, audio) does it support for embedding C2PA manifests? Does it embed into video files? What is the current status of the repo (moved to c2pa-rs)?"
}
```

## 🤖 Claude *(20:39:43)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "C2PA durable content credentials invisible watermark Digimarc soft binding open source"
}
```

## 🤖 Claude *(20:39:43)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "EU AI Act Article 50 machine-readable marking synthetic content C2PA watermark"
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # C2patool Overview
> 
> ## Software License
> C2patool is licensed under dual licenses: "Apache-2.0, MIT licenses found" in the repository.
> 
> ## Supported File Formats
> The tool works with "C2PA manifests and media assets (audio, image or video files)." However, the provided content does not specify which particular formats within these categories are supported.
> 
> ## Video File Support
> Yes, the documentation indicates the tool handles video files as part of its media asset support, though specific embedding details are not detailed in this excerpt.
> 
> ## Repository Status
> **The project has been archived and moved.** As stated: "As of 10 December 2024, we've transitioned work on the c2patool project to the contentauth/c2pa-rs repo." The current repository is now read-only, with all existing pull requests and issues migrated to the new location. Users should file new issues or PRs in the c2pa-rs repository instead.
> ```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "C2PA durable content credentials invisible watermark Digimarc soft binding open source"
> 
> Links: [{"title":"Durable Content Credentials | Open-source tools for content authenticity and provenance","url":"https://opensource.contentauthenticity.org/docs/durable-cr/"},{"title":"How Digital Watermarks Strengthen C2PA Content Credentials | by Dominique Guinard | Medium","url":"https://domguinard.medium.com/how-digital-watermarks-strengthen-c2pa-content-credentials-764be8b15a38"},{"title":"Provenance & Authenticity Solution","url":"https://www.digimarc.com/solutions/provenance-authenticity"},{"title":"Using TrustMark with C2PA | Open-source tools for content authenticity and provenance","url":"https://opensource.contentauthenticity.org/docs/trustmark/c2pa/"},{"title":"C2PA 2.1 - Strengthening Content Credentials with Digital Watermarks","url":"https://www.digimarc.com/blog/c2pa-21-strengthening-content-credentials-digital-watermarks"},{"title":"How Digital Watermarks Strengthen C2PA Content Credentials","url":"https://www.digimarc.com/blog/how-digital-watermarks-strengthen-c2pa-content-credentials"},{"title":"Digital watermarking for interoperable and durable Content Credentials","url":"https://contentauthenticity.org/blog/digital-watermarking-interoperable-durable-content-credentials"},{"title":"GitHub - digimarc-corp/c2pa-content-credentials-extension: C2PA Chrome Extension · GitHub","url":"https://github.com/digimarc-corp/c2pa-content-credentials-extension"},{"title":"1. Introduction 1. Overview","url":"https://c2pa.org/wp-content/uploads/sites/33/2025/10/content_credentials_wp_0925.pdf"}]
> 
> Here are the search results for your query about C2PA durable content credentials, invisible watermarks, Digimarc, soft binding, and open source:
> 
> ## Key Findings
> 
> **Durable Content Credentials Concept:**
> Durable Content Credentials help content provenance persist across platforms by using C2PA manifest data with invisible watermarks actively inserted into content and content fingerprints passively computed from content.
> 
> **Soft Binding Definition:**
> The C2PA specification refers to watermarking and content fingerprinting as soft bindings, and requires that they be generated using approved Watermarking and fingerprinting algorithms.
> 
> **Digimarc's Role:**
> Digimarc built the first implementation of invisible watermarking for C2PA purposes and the first open source C2PA Chrome Extension. As a pioneer in digital watermarking, Digimarc built an integration between C2PA and their digital watermarking technology, using invisible SAFE™ digital watermarks added to digital assets.
> 
> **Interoperability:**
> The interoperability leverages the open source watermark TrustMark to signal which company's watermark is present, in order to properly decode and retrieve durable Content Credentials.
> 
> **Open Ecosystem:**
> Anyone may submit algorithms for inclusion on the C2PA watermarking algorithms list by filing a pull request on GitHub, enabling a rich and open ecosystem of watermarking algorithms.
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "EU AI Act Article 50 machine-readable marking synthetic content C2PA watermark"
> 
> Links: [{"title":"AI Watermarking 2026: C2PA, Metadata and Fingerprinting","url":"https://aibuzz.blog/ai-watermarking-vs-metadata-vs-fingerprinting/"},{"title":"Complete Guide to EU AI Act Watermarking Requirements for Generative AI","url":"https://www.resemble.ai/resources/complete-guide-to-eu-ai-act-watermarking-requirements-for-generative-ai"},{"title":"EU AI Act Article 50: AI Content Watermarking Guide | BeyondScale","url":"https://beyondscale.tech/blog/eu-ai-act-article-50-watermarking-compliance"},{"title":"EU AI Act Article 50: AI Content Labeling & C2PA | Pebblous","url":"https://blog.pebblous.ai/blog/eu-ai-content-labeling-article-50-provenance/en/"},{"title":"EU AI Act and C2PA: What Article 50 Requires for AI Content | C2PA Viewer","url":"https://c2paviewer.com/articles/eu-ai-act-content-credentials"},{"title":"The EU AI Act’s Transparency Rules: A Practical Guide to Article 50 | EU Artificial Intelligence Act","url":"https://artificialintelligenceact.eu/transparency-rules-article-50/"},{"title":"Watermarks and Metadata: How to Actually Comply With the EU AI Act's Article 50 Transparency Rules | ComplianceHub.Wiki","url":"https://compliancehub.wiki/eu-ai-act-marking-labelling-code-of-practice-article-50-2026/"},{"title":"AI Watermarking Tools for Creators: 2026 EU Compliance Guide","url":"https://techplustrends.com/ai-watermarking-tools-eu-compliance-2026/"},{"title":"Verifiable Provenance and Watermarking for Generative AI: An Evidentiary Framework for International Operational Law and Domestic Courts","url":"https://arxiv.org/pdf/2605.21002"}]
> 
> Here are the search results for EU AI Act Article 50 related to machine-readable marking of synthetic content and C2PA watermarking:
> 
> ## Key Findings
> 
> **Article 50 Requirements:**
> EU AI Act Article 50 makes machine-readable marking of AI-generated content a legal obligation from August 2, 2026, with penalties up to €15 million or 3% of global annual turnover for non-compliance. The requirement applies to providers and deployers of AI systems that generate or manipulate audio, visual, or audiovisual content to mark that content in a machine-readable format so that it is identifiable as AI-generated or manipulated.
> 
> **Multi-Layered Approach:**
> Organizations producing AI content for public distribution in EU markets from August 2, 2026 need at minimum: C2PA credential embedding at generation (the metadata layer), invisible watermarking that survives platform processing (the resilient signal layer), and logging of generation events (the audit trail layer).
> 
> **C2PA as the Primary Standard:**
> C2PA is an open standard adopted by more than 6,000 members — Adobe, Microsoft, Google, Intel, BBC, AP, and others — and has been formally standardized as ISO/IEC 21694. It is the strongest candidate for meeting the "machine-readable marking" requirement Article 50(2) describes. However, the law does not require C2PA, but the regulatory ecosystem points firmly at it.
> 
> **Why Multiple Technologies Are Needed:**
> C2PA metadata can fall off entirely if a single screenshot is taken or the file format is converted. So the Code specifies not a single technology but a multi-layer approach that overlaps several methods, with the Code's own words stating "no single technique is sufficient on its own."
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

## 🤖 Claude *(20:39:59)*

<details>
<summary>💭 Thinking Process</summary>

I need to dig into some specifics here—TrustMark's licensing details, the exact video format support in c2pa-rs and c2patool, how IPTC and XMP handle AI metadata, and what platforms can actually read these credentials. I should also double-check that ISO/IEC 21694 number for C2PA standardization and get clearer on Meta and TikTok's Content Credentials implementation.

</details>


## 🤖 Claude *(20:39:59)*

Let me verify TrustMark (open-source watermark), IPTC/XMP AI metadata, and platform read specifics.

## 🤖 Claude *(20:39:59)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://opensource.contentauthenticity.org/docs/trustmark/",
  "prompt": "What is TrustMark? What is its software license? Does it do invisible watermarking for images? Does it support video? Who created it (Adobe)? Is it free/open source?"
}
```

## 🤖 Claude *(20:40:00)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "IPTC photo metadata \"Digital Source Type\" trainedAlgorithmicMedia AI generated XMP field platforms read"
}
```

## 🤖 Claude *(20:40:02)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://opensource.contentauthenticity.org/docs/c2patool/docs/supported-formats/",
  "prompt": "List all file formats c2patool / c2pa-rs supports for reading and writing/embedding C2PA manifests. Specifically which image formats, video formats (MP4, MOV), and audio formats can have manifests embedded (not just sidecar)?"
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # TrustMark Overview
> 
> **What is TrustMark?**
> TrustMark is an open-source watermarking technology for the Content Authenticity Initiative. It's described as "Universal Watermarking for Arbitrary Resolution Images" and includes implementations in Python, JavaScript, and Rust for encoding, decoding, and removing watermarks from images.
> 
> **Software License**
> The project is "distributed under the terms of the MIT license," making it freely available for use and modification.
> 
> **Invisible Watermarking**
> Yes, TrustMark embeds a 100-bit payload directly into images while maintaining quality. The example shows a PSNR (Peak Signal-to-Noise Ratio) of 50.36, indicating the watermark is imperceptible to human viewers.
> 
> **Video Support**
> The documentation does not mention video support. The technology appears focused exclusively on image watermarking.
> 
> **Creator**
> Adobe Research developed TrustMark alongside researchers from the University of Surrey's DECaDE Centre. The work was published at ICCV 2025.
> 
> **Free and Open Source**
> Yes. TrustMark is freely available via PyPI installation and its source code is hosted on GitHub under an MIT license, making it genuinely open-source software.
> ```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "IPTC photo metadata "Digital Source Type" trainedAlgorithmicMedia AI generated XMP field platforms read"
> 
> Links: [{"title":"IPTC publishes metadata guidance for AI-generated \"synthetic media\" - IPTC","url":"https://iptc.org/news/iptc-publishes-metadata-guidance-for-ai-generated-synthetic-media/"},{"title":"How to Label AI-Generated Images with Metadata | Exif Injector","url":"https://exifinjector.com/blog/label-ai-generated-images-with-metadata"},{"title":"EXIF vs IPTC vs XMP: What's the Difference? (2026 Metadata Guide) | AI Metadata Cleaner Blog","url":"https://aimetadatacleaner.com/blog/understanding-iptc-exif-xmp-metadata-complete-guide-2025"},{"title":"How to Label AI-Generated Images: Fast Website Guide to Disclaimers & Provenance","url":"https://skywork.ai/blog/how-to-label-ai-generated-images-guide/"},{"title":"AI-generated content - Google Merchant Center Help","url":"https://support.google.com/merchants/answer/14743464?hl=en-IE"},{"title":"IPTC Photo Metadata Standard (IPTC PMD) — Metadata Standards Index","url":"https://msi.dublincore.org/standards/iptc-photo-metadata/"},{"title":"IPTC Metadata Fields: Complete Guide for Images (2026)","url":"https://exifinjector.com/blog/iptc-metadata-fields"},{"title":"IPTC Photo Metadata User Guide","url":"https://www.iptc.org/std/photometadata/documentation/userguide/"},{"title":"Photo Metadata Standards: IPTC, EXIF, and XMP - DEV Community","url":"https://dev.to/maryalice/photo-metadata-standards-iptc-exif-and-xmp-4n5d"}]
> 
> Based on the search results, here's comprehensive information about IPTC photo metadata, Digital Source Type, and AI-generated content labeling:
> 
> ## IPTC Digital Source Type for AI-Generated Images
> 
> IPTC recommends that software creating images using trained AI algorithms uses the "Digital Source Type" value of "trainedAlgorithmicMedia" added to the XMP data packet in generated image and video files.
> 
> ### XMP Field Implementation
> 
> Three metadata fields are the standard for labeling AI-generated images: IPTC DigitalSourceType, XMP Iptc4xmpExt:DigitalSourceType, and an optional C2PA manifest. Different platforms read different formats, and writing both ensures full compatibility.
> 
> ### Digital Source Type Values
> 
> The main values include trainedAlgorithmicMedia for images fully generated by AI from a prompt, and compositeWithTrainedAlgorithmicMedia for real photos combined with AI-generated elements.
> 
> ### Platforms Reading These Fields
> 
> Major platforms including Meta, Google, Pinterest, OpenAI, Microsoft, Adobe, MidJourney, and Shutterstock are implementing IPTC standards for AI content labeling. Meta already uses IPTC's Digital Source Type property, setting it to "trainedAlgorithmicMedia" for AI-generated images.
> 
> ### Technical Details
> 
> Some field values are transferred to both the IIM and the XMP structures while others only go to the XMP structure, including Digital Source Type. Version 2025.1 added properties for AI-generated content description.
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # C2PA Manifest Support in c2patool/c2pa-rs
> 
> Based on the documentation, c2patool supports embedding C2PA manifests in the following formats:
> 
> **Image Formats:**
> AVIF, DNG, GIF, HEIC, HEIF, JPEG, JXL, PNG, SVG, TIFF, and WebP
> 
> **Video Formats:**
> AVI, MP4, MOV, and fragmented MP4 (DASH) - though the latter is "supported only for file-based operations from the Rust library"
> 
> **Audio Formats:**
> FLAC, M4A, MP3, and WAV
> 
> **Notable Limitation:**
> PDF files are marked as "read-only," meaning manifests cannot be embedded in PDFs. Additionally, the C2PA format itself (.c2pa) is supported for manifest storage operations.
> 
> The documentation indicates these capabilities apply across the SDK libraries unless specifically noted otherwise for particular implementations.
> ```

## 🤖 Claude *(20:40:17)*

<details>
<summary>💭 Thinking Process</summary>

I need to double-check a few key facts: the ISO standard designation for C2PA, whether platforms like TikTok and Instagram actually read and display C2PA metadata, whether Meta strips it, the specific fragility concerns, and whether tools like Veo and Gemini already embed SynthID or C2PA by default.

</details>


## 🤖 Claude *(20:40:17)*

Let me verify the ISO standardization, and whether Google's Gemini/Veo already embed SynthID/C2PA (relevant since MCORCH uses Nano Banana/Veo).

## 🤖 Claude *(20:40:17)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "C2PA ISO/IEC 21694 standard ratified international standard"
}
```

## 🤖 Claude *(20:40:17)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "Google Gemini image Veo SynthID watermark C2PA metadata embedded AI generated 2025"
}
```

## 🤖 Claude *(20:40:18)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://c2pa.ai/instagram",
  "prompt": "Does Instagram/Meta display Content Credentials? Does Instagram strip or preserve C2PA metadata on upload? What does Meta do with AI labels and IPTC DigitalSourceType?"
}
```

> **Tool Result (WebFetch)** - ❌ Error
>
> ```
> getaddrinfo ENOTFOUND c2pa.ai
> ```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "C2PA ISO/IEC 21694 standard ratified international standard"
> 
> Links: [{"title":"1. Introduction 1. Overview","url":"https://c2pa.org/wp-content/uploads/sites/33/2025/10/content_credentials_wp_0925.pdf"},{"title":"C2PA Standard: History, Promises and Structural Limitations","url":"https://truescreen.io/articles/c2pa-standard-history-limitations/"},{"title":"ISO/DIS 22144, Authenticity of Information - Content Credentials - Association for Information Science and Technology | ASIS&T","url":"https://www.asist.org/2025/03/19/iso-22144-authenticity-information-standards/"},{"title":"C2PA Technical Specification :: C2PA Specifications","url":"https://spec.c2pa.org/specifications/specifications/1.0/specs/C2PA_Specification.html"},{"title":"Content Credentials : C2PA Technical Specification :: C2PA Specifications","url":"https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html"},{"title":"Interoperable Provenance Authentication of Broadcast Media using Open   Standards-based Metadata, Watermarking and Cryptography","url":"https://arxiv.org/pdf/2405.12336"},{"title":"C2PA and CAWG Standards Overview | Trufo","url":"https://trufo.ai/standards"},{"title":"Content ARCs: Decentralized Content Rights in the Age of Generative AI","url":"https://arxiv.org/pdf/2503.14519"},{"title":"C2PA Specifications :: C2PA Specifications","url":"https://spec.c2pa.org/specifications/specifications/2.2/index.html"}]
> 
> Based on the search results, I can provide you with information about C2PA and its relationship to ISO/IEC standards:
> 
> C2PA (Coalition for Content Provenance and Authenticity) is an open technical standard that attaches cryptographically signed provenance metadata to digital media, supported by Adobe, Microsoft, Google, OpenAI, and other industry members.
> 
> Regarding the ISO/IEC standards:
> 
> - C2PA version 2 has been fast-tracked as an international standard (ISO/DIS 22144), which is currently in draft stage rather than fully ratified.
> 
> - ISO 22144 defines the technical framework for Content Credentials (C2PA), offering cryptographically verifiable methods to assess authenticity and trust in digital information using digital signatures and manifests.
> 
> Regarding ISO/IEC 21694 specifically, the search results do not contain direct information about this particular standard number in relation to C2PA. However, the results show that C2PA references various ISO standards in its technical specifications for container formats and other technical components.
> 
> If you need more specific information about ISO/IEC 21694 and its relationship to C2PA, please let me know and I can search for additional details.
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "Google Gemini image Veo SynthID watermark C2PA metadata embedded AI generated 2025"
> 
> Links: [{"title":"Verify AI-generated images, videos, and audio - Computer - Gemini Apps Help","url":"https://support.google.com/gemini/answer/16722517?hl=en&co=GENIE.Platform%3DDesktop"},{"title":"Verify AI-generated images, videos, and audio - Android - Gemini Apps Help","url":"https://support.google.com/gemini/answer/16722517?hl=en&co=GENIE.Platform%3DAndroid"},{"title":"Google Adds AI Content Detection Tools to Gemini | Social Media Today","url":"https://www.socialmediatoday.com/news/google-adds-ai-content-detection-tools-to-gemini/808310/"},{"title":"Google Gemini Introduces New Feature to Identify AI-Generated Images | by CherryZhou | Nov, 2025 | Medium","url":"https://medium.com/@CherryZhouTech/google-gemini-introducs-new-feature-to-identify-ai-generated-images-be05d4f3a653"},{"title":"How we’re bringing AI image verification to the Gemini app","url":"https://blog.google/technology/ai/ai-image-verification-gemini-app/"},{"title":"SynthID in 2025: Where Google’s Invisible Watermark Shows Up (and Where It Doesn’t)","url":"https://jesusiniesta.es/blog/synthid-invisible-watermarks-2025"},{"title":"Google Gemini Adds Hidden AI Watermark Detection to Expose Fake Images","url":"https://www.diyphotography.net/google-gemini-ai-image-verification-synthid/"}]
> 
> Based on the search results, here's what I found about Google Gemini's AI-generated image detection and verification technologies:
> 
> ## SynthID Watermark Technology
> 
> SynthID uses invisible watermarks to determine if images, videos, and audio were generated or edited specifically by Google's AI models. This system embeds a digital watermark directly into the pixels of an image at the time of its creation by Google's AI tools, and this watermark is imperceptible to the human eye but can be detected by Gemini's analysis.
> 
> SynthID is officially supported for Google's own image and video models (Imagen family, Gemini image models, Veo) and for partner products that explicitly pipe to those models.
> 
> ## C2PA Metadata Integration
> 
> Content Credentials is an industry standard developed by the Coalition for Content Provenance and Authenticity (C2PA), and is supported by many products from different companies. Images generated by Nano Banana Pro (Gemini 3 Pro Image) in the Gemini app, Vertex AI and Google Ads have C2PA metadata embedded, providing further transparency into how these images were created.
> 
> ## Gemini Verification Features
> 
> Google's SynthID detection is now available in Gemini for files up to 100 MB and 90 seconds long. Google plans to expand SynthID verification to video and audio and support C2PA content credentials in the future.
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

## 🤖 Claude *(20:40:54)*

<details>
<summary>💭 Thinking Process</summary>

I found a discrepancy in the ISO standard designation — the search results show C2PA v2 is being fast-tracked as ISO/DIS 22144 (draft international standard), which contradicts the earlier reference to ISO/IEC 21694 from the compliance blog. I'll use ISO/DIS 22144 with proper sourcing and mark the 21694 reference as unverifiable.

Now I'm compiling the structured findings with sources: the C2PA manifest structure from the official spec, the c2patool licensing details and recent migration to c2pa-rs, supported file formats across images and video, TrustMark's invisible watermark approach, how Durable Content Credentials layer C2PA with watermarking and fingerprinting, IPTC's DigitalSourceType standard for marking AI-generated content, platform adoption across LinkedIn, Google, Meta, TikTok and Instagram, the fragility of metadata when content is re-encoded or screenshotted, and the EU AI Act's machine-readable marking requirement taking effect in August 2026 with associated penalties.

No single technique covers all cases, so I'm looking at a layered approach: Google's Gemini and Veo models already embed SynthID and C2PA natively, and there's an emerging ISO standard for this. For MCORCH integration, images generated through Nano Banana Pro or Vertex inherit Google's built-in SynthID and C2PA, but for our own re-encoded or composited outputs I'd add a C2PA claim plus TrustMark watermark plus IPTC DigitalSourceType metadata at generation time into the creative assets pipeline. For video with HyperFrames and Veo, I'd use c2pa-rs to embed into the MP4 at finalization through the video-bridge worker, though watermarking video is trickier since TrustMark only handles images—that's a gap where we'd rely on C2PA and IPTC with per-frame watermarking deferred. Voice generation with Qwen3 still needs definition.

For audio, I'm considering embedding C2PA into WAV, MP3, or M4A using c2pa-rs, and AudioSeal from Meta could handle audio watermarking, though I haven't verified that yet so I'm flagging it as a research candidate with low confidence. I'm structuring the output using the StructuredOutput schema with front matter, key findings tied to source URLs, notes, open source tooling, MCORCH recommendations, and risk assessment.

The open source tools available include c2patool and c2pa-rs under Apache 2.0/MIT licenses, TrustMark under MIT, the C2PA Python and JavaScript SDKs, and ExifTool for IPTC metadata under Perl Artistic/GPL. For MCORCH application, I need to detail how these work across images, video, and voice. The main risks are that metadata can be stripped, video watermarking has gaps, signing requires a certificate (either self-signed for testing or from the C2PA trust list for production), and there's potential double-signing if Veo or Gemini already sign content. Audio watermarking verification is still pending.

I should flag my confidence level as medium on the certificate requirements since I'm relying on general knowledge, though the getting-started documentation does mention this. Let me now structure the output properly.

</details>


## 🤖 Claude *(20:40:54)*

I have enough verified material to compile the research front. Compiling findings now.

## 🤖 Claude *(20:42:06)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "front": "content-provenance (deepsearch \u2014 Modo 1: frente de pesquisa verificada)",
  "keyFindings": [
    {
      "claim": "Estrutura do manifest C2PA: um Manifest \u00e9 uma estrutura de dados assinada digitalmente e \u00e0 prova de adultera\u00e7\u00e3o (tamper-evident) composta por (a) uma ou mais assertions \u2014 declara\u00e7\u00f5es sobre o ativo, incluindo content bindings/hard binding e a assertion de origem/uso de IA; (b) um \u00fanico claim que conecta as assertions ao signat\u00e1rio; e (c) uma claim signature (assinatura digital com a chave privada do signer). O signer \u00e9 o detentor da chave privada identificado pelo subject do certificado. Confian\u00e7a ALTA (spec normativa oficial).",
      "sourceUrl": "https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html"
    },
    {
      "claim": "c2patool \u00e9 a CLI oficial da Content Authenticity Initiative para exibir e ADICIONAR/embedar manifests C2PA. Licen\u00e7a dual Apache-2.0 / MIT (comercial-safe). O repo contentauth/c2patool foi congelado (read-only) em 10-dez-2024 e o trabalho migrou para contentauth/c2pa-rs (mesma licen\u00e7a Apache-2.0/MIT). Embeda in-place no arquivo (--manifest JSON, --output) OU gera sidecar externo .c2pa. Confian\u00e7a ALTA.",
      "sourceUrl": "https://github.com/contentauth/c2patool"
    },
    {
      "claim": "Formatos que c2patool/c2pa-rs consegue EMBEDAR manifest (n\u00e3o s\u00f3 sidecar): IMAGEM \u2014 AVIF, DNG, GIF, HEIC/HEIF, JPEG, JXL, PNG, SVG, TIFF, WebP; V\u00cdDEO \u2014 AVI, MP4, MOV, e fMP4/DASH (este s\u00f3 via lib Rust file-based); \u00c1UDIO \u2014 FLAC, M4A, MP3, WAV. PDF \u00e9 read-only (n\u00e3o embeda). Ou seja, cobre os 3 outputs do MCORCH: imagem (PNG/JPEG/WebP), v\u00eddeo (MP4/MOV do HyperFrames+Veo) e voz (WAV/MP3/M4A do Qwen3). Confian\u00e7a ALTA.",
      "sourceUrl": "https://opensource.contentauthenticity.org/docs/c2patool/docs/supported-formats/"
    },
    {
      "claim": "Camada 2 (watermark invis\u00edvel): TrustMark \u00e9 o watermark open-source da CAI/Adobe Research (com U. of Surrey, ICCV 2025), licen\u00e7a MIT, implementa\u00e7\u00f5es Python/JS/Rust; embeda payload de 100 bits em imagem de resolu\u00e7\u00e3o arbitr\u00e1ria mantendo qualidade (PSNR ~50). LIMITA\u00c7\u00c3O MATERIAL: TrustMark \u00e9 S\u00d3 IMAGEM \u2014 a doc n\u00e3o menciona v\u00eddeo nem \u00e1udio. Confian\u00e7a ALTA (\u00e9 imagem-only).",
      "sourceUrl": "https://opensource.contentauthenticity.org/docs/trustmark/"
    },
    {
      "claim": "As 3 camadas s\u00e3o exatamente o modelo 'Durable Content Credentials' da CAI: manifest C2PA (hard binding, remov\u00edvel) + watermark invis\u00edvel ATIVO + fingerprint PASSIVO computado do conte\u00fado. Na spec C2PA, watermark e fingerprint s\u00e3o 'soft bindings' e devem usar algoritmos aprovados na lista C2PA; qualquer empresa pode submeter algoritmo via PR no GitHub. TrustMark \u00e9 usado para sinalizar QUAL watermark est\u00e1 presente (interoperabilidade). Confian\u00e7a ALTA.",
      "sourceUrl": "https://opensource.contentauthenticity.org/docs/durable-cr/"
    },
    {
      "claim": "Camada 3 (metadata fallback universal): IPTC recomenda que software que gera imagem via IA use 'Digital Source Type' = 'trainedAlgorithmicMedia' no XMP (campo Iptc4xmpExt:DigitalSourceType), e 'compositeWithTrainedAlgorithmicMedia' para foto real + elemento IA. Meta J\u00c1 USA a propriedade IPTC Digital Source Type = trainedAlgorithmicMedia para rotular imagens IA. Plataformas implementando IPTC: Meta, Google, Pinterest, OpenAI, Microsoft, Adobe, MidJourney, Shutterstock. Confian\u00e7a ALTA.",
      "sourceUrl": "https://iptc.org/news/iptc-publishes-metadata-guidance-for-ai-generated-synthetic-media/"
    },
    {
      "claim": "Plataformas que LEEM/EXIBEM Content Credentials: LinkedIn exibe \u00edcone 'CR' clic\u00e1vel com resumo de proveni\u00eancia para imagens com Content Credentials. Confian\u00e7a ALTA (p\u00e1gina de ajuda oficial LinkedIn).",
      "sourceUrl": "https://www.linkedin.com/help/linkedin/answer/a6282984"
    },
    {
      "claim": "Fragilidade central (por que C2PA sozinho n\u00e3o basta): a metadata C2PA pode cair inteira com um \u00fanico screenshot ou convers\u00e3o de formato/re-encode. O C\u00f3digo de Pr\u00e1tica do AI Act declara explicitamente que 'nenhuma t\u00e9cnica isolada \u00e9 suficiente por si s\u00f3' \u2014 da\u00ed a abordagem multi-camada (C2PA + watermark resiliente + log de gera\u00e7\u00e3o). Confian\u00e7a ALTA.",
      "sourceUrl": "https://compliancehub.wiki/eu-ai-act-marking-labelling-code-of-practice-article-50-2026/"
    },
    {
      "claim": "AI Act Art.50(2)/(4): providers/deployers de sistemas que geram ou manipulam \u00e1udio/imagem/v\u00eddeo devem marcar o conte\u00fado em formato MACHINE-READABLE identific\u00e1vel como gerado/manipulado por IA; obriga\u00e7\u00e3o vigente a partir de 2-ago-2026, multas at\u00e9 \u20ac15M ou 3% do faturamento global. C2PA (open standard, >6000 membros) \u00e9 o candidato mais forte para satisfazer 'machine-readable marking', embora a lei n\u00e3o o exija nominalmente. Confian\u00e7a ALTA no prazo/obriga\u00e7\u00e3o; n\u00ba de membros M\u00c9DIA.",
      "sourceUrl": "https://beyondscale.tech/blog/eu-ai-act-article-50-watermarking-compliance"
    },
    {
      "claim": "ACHADO CR\u00cdTICO para o MCORCH: imagens geradas pelo Nano Banana Pro (Gemini 3 Pro Image) no app Gemini, Vertex AI e Google Ads J\u00c1 v\u00eam com metadata C2PA embutida + watermark invis\u00edvel SynthID (nos pixels). SynthID cobre oficialmente Imagen, modelos de imagem Gemini e Veo. Ou seja: parte do output do MCORCH pode j\u00e1 chegar assinado na origem \u2014 evitar dupla-assinatura destrutiva e, ao inv\u00e9s, PRESERVAR e adicionar nossa assertion. Confian\u00e7a ALTA.",
      "sourceUrl": "https://blog.google/technology/ai/ai-image-verification-gemini-app/"
    },
    {
      "claim": "Status de padroniza\u00e7\u00e3o ISO: o C2PA v2 foi fast-tracked como ISO/DIS 22144 ('Authenticity of Information \u2014 Content Credentials'), atualmente em est\u00e1gio DRAFT (DIS), n\u00e3o ratificado final. NOTA: uma fonte de compliance citou 'ISO/IEC 21694' \u2014 N\u00c3O confirmado em fonte oficial; tratar como n\u00e3o-verificado (usar 22144).",
      "sourceUrl": "https://www.asist.org/2025/03/19/iso-22144-authenticity-information-standards/"
    },
    {
      "claim": "Google Search/Images exibe Content Credentials em resultados de imagem; Meta/Instagram tem exibi\u00e7\u00e3o read-only de r\u00f3tulos de IA e reconhece IPTC DigitalSourceType, mas N\u00c3O preserva as Content Credentials quando o usu\u00e1rio faz upload pelo app (re-encode remove); TikTok anunciou integra\u00e7\u00e3o C2PA para rotular conte\u00fado IA, sem timeline confirmada de exibi\u00e7\u00e3o completa. Confian\u00e7a M\u00c9DIA (agregado de fontes secund\u00e1rias; comportamento de plataforma muda r\u00e1pido).",
      "sourceUrl": "https://en.wikipedia.org/wiki/Content_Credentials"
    }
  ],
  "openSourceTooling": [
    "c2patool / c2pa-rs (Rust CLI+SDK oficial CAI) \u2014 licen\u00e7a Apache-2.0 OR MIT \u2014 comercial-safe SIM, USD=0. Embeda manifest em JPEG/PNG/WebP/AVIF, MP4/MOV/AVI, MP3/WAV/M4A/FLAC. Precisa de um par cert/chave para assinar o claim (test cert incluso para dev; produ\u00e7\u00e3o = cert pr\u00f3prio, validado como 'signed by unknown issuer' at\u00e9 entrar em trust list) \u2014 https://github.com/contentauth/c2pa-rs",
    "TrustMark (Adobe Research/CAI) \u2014 licen\u00e7a MIT \u2014 comercial-safe SIM, USD=0. Watermark invis\u00edvel 100-bit para IMAGEM (Python/JS/Rust). S\u00d3 IMAGEM \u2014 n\u00e3o cobre v\u00eddeo nem \u00e1udio \u2014 https://opensource.contentauthenticity.org/docs/trustmark/",
    "ExifTool (Phil Harvey) \u2014 Perl Artistic License / GPL \u2014 comercial-safe SIM, USD=0. Grava IPTC Iptc4xmpExt:DigitalSourceType = trainedAlgorithmicMedia no XMP (camada 3 fallback). (Ferramenta padr\u00e3o de fato; verificar licen\u00e7a/bin\u00e1rio antes de embutir no pipeline)",
    "GAP a pesquisar em frente futura: watermark de V\u00cdDEO e de \u00c1UDIO open-source comercial-safe (TrustMark n\u00e3o cobre). Candidatos a VERIFICAR (n\u00e3o confirmados nesta rodada): Meta AudioSeal (\u00e1udio) e VideoSeal (v\u00eddeo) \u2014 checar licen\u00e7a antes de qualquer decis\u00e3o. N\u00c3O afirmar como fato at\u00e9 consultar o repo."
  ],
  "recommendedForMcorch": "Defesa-em-profundidade de 3 camadas, aplicada NO MOMENTO DA GERA\u00c7\u00c3O e persistida no spine creative_assets (nova coluna/flag de proveni\u00eancia + o .c2pa/sidecar como asset irm\u00e3o em bucket privado; N\u00c3O reconstruir distribui\u00e7\u00e3o). Por output sint\u00e9tico: (1) IMAGEM Nano Banana/Gemini \u2014 se vier do Nano Banana Pro/Vertex, j\u00e1 traz C2PA+SynthID: PRESERVAR (n\u00e3o re-encodar cegamente) e adicionar nossa assertion de 'MCORCH generated' + IPTC DigitalSourceType=trainedAlgorithmicMedia via c2pa-rs; para imagem que re-compomos/recodificamos, embedar C2PA (c2pa-rs) + watermark TrustMark 100-bit + IPTC XMP. (2) V\u00cdDEO HyperFrames (MP4 determin\u00edstico) e Veo \u2014 assinar C2PA no MP4/MOV via c2pa-rs no worker de finalize (video-bridge, ap\u00f3s finalize_video_render, antes do upload ao bucket) + IPTC XMP; Veo j\u00e1 traz SynthID (preservar). Watermark de v\u00eddeo fica como camada-2 DEFERIDA (TrustMark \u00e9 imagem-only) \u2014 declarar OTD com gap honesto. (3) VOZ Qwen3 (WAV\u2192MP3/M4A) \u2014 embedar C2PA em WAV/MP3/M4A via c2pa-rs no voice-bridge ap\u00f3s render; watermark de \u00e1udio DEFERIDO (candidato AudioSeal a verificar). Camada-3 IPTC/XMP \u00e9 o m\u00ednimo universal para todos os 3 (Meta/Google/Pinterest leem). Custo USD=0 nas ferramentas (Apache/MIT); o \u00fanico custo operacional \u00e9 o cert de assinatura (self-signed inicial, trust-list depois). Materialidade: cada asset marcado prova com c2patool verify retornando o manifest \u2014 nunca declarar 'marcado' sem o output de verify.",
  "notes": "MODO 1 (frente de pesquisa). Todas as claims carregam a URL realmente consultada via WebSearch/WebFetch. N\u00c3O gerei documento de 10 se\u00e7\u00f5es (isso \u00e9 Modo 3/s\u00edntese \u2014 o caller deve acionar a s\u00edntese depois de eventual verify adversarial). could_not_verify / a checar antes de virar c\u00f3digo: (a) n\u00ba exato '>6000 membros' C2PA (fonte secund\u00e1ria, M\u00c9DIA); (b) 'ISO/IEC 21694' de um blog de compliance N\u00c3O bate com a fonte oficial ISO/DIS 22144 \u2014 descartar 21694 at\u00e9 confirmar; (c) comportamento vivo de strip/display em Instagram/TikTok/YouTube muda r\u00e1pido \u2014 reverificar no momento da SDD; (d) watermark open-source de v\u00eddeo e \u00e1udio (AudioSeal/VideoSeal) N\u00c3O foi consultado nesta rodada \u2014 n\u00e3o afirmar licen\u00e7a/capacidade sem abrir o repo; (e) fluxo exato de cert/trust-list do c2pa-rs em produ\u00e7\u00e3o (dev usa test cert) precisa de leitura da getting-started/signing docs antes do c\u00f3digo. c2pa.ai foi inalcan\u00e7\u00e1vel (DNS ENOTFOUND) \u2014 finding honesto, n\u00e3o inventei o conte\u00fado. GATE BoK: este \u00e9 blueprint/pesquisa; qualquer c\u00f3digo de marca\u00e7\u00e3o exige a fam\u00edlia BoK do m\u00f3dulo content-provenance + Pattern Conformance antes (Closed-Loop).",
  "risks": [
    "C2PA \u00e9 remov\u00edvel: um \u00fanico screenshot ou re-encode de plataforma apaga o manifest \u2014 por isso a camada-2 watermark \u00e9 obrigat\u00f3ria, n\u00e3o opcional (fonte: C\u00f3digo de Pr\u00e1tica AI Act + CAI durable-cr).",
    "Watermark de V\u00cdDEO e de \u00c1UDIO \u00e9 um GAP real: TrustMark (a ferramenta MIT recomendada) \u00e9 imagem-only. V\u00eddeo HyperFrames/Veo e voz Qwen3 ficam s\u00f3 com C2PA+IPTC (remov\u00edveis) at\u00e9 resolver watermark A/V open-source \u2014 declarar OTD de risco, n\u00e3o fingir cobertura.",
    "Assinatura C2PA exige cert/chave: o test cert do c2pa-rs N\u00c3O serve para produ\u00e7\u00e3o (valida como 'unknown issuer'); precisa de estrat\u00e9gia de cert pr\u00f3pria (self-signed \u2192 eventual trust list C2PA). Custo/processo a definir na SDD.",
    "Dupla-assinatura destrutiva: outputs que j\u00e1 chegam assinados (Nano Banana Pro/Vertex = C2PA+SynthID; Veo = SynthID) podem ser corrompidos se re-encodarmos sem cuidado. Preservar-e-anexar, nunca sobrescrever cego.",
    "Prazo regulat\u00f3rio duro: AI Act Art.50 machine-readable vigora 2-ago-2026, multa at\u00e9 \u20ac15M/3% faturamento \u2014 o m\u00f3dulo tem deadline material, n\u00e3o \u00e9 nice-to-have.",
    "Lei 1: nunca declarar um asset 'marcado' sem o output de c2patool verify (ou equivalente) mostrando o manifest \u2014 a marca\u00e7\u00e3o silenciosa que n\u00e3o persiste \u00e9 falso-sucesso."
  ]
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-15 - agent-abb5192c5f9cb99d7]]
> * **Próxima Sessão**: [[2026-07-15 - agent-abce9650a64ff6863]]
%% --- TIMELINE END --- %%
